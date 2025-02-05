import boto3
import os
from datetime import datetime, timezone
from calendar import monthrange

from rent_scraper import get_latest_rent

# Import roommate names (Ensure login_info.py exists)
try:
    from login_info import ROOMMATE_1_NAME, ROOMMATE_2_NAME, ROOMMATE_3_NAME
except ImportError:
    raise Exception(
        "Error: 'login_info.py' is missing. Please create it with your credentials.")

# If pasting into AWS Lambda, paste everything below this line to EOF.
COST_PER_SQUARE_FOOT = 4.44
TOTAL_SQUARE_FEET = 549.25
NUM_ROOMMATES = 3

# Bedroom square footage and rent calculations
BEDROOMS = {
    "Master Bedroom": {"roommate": ROOMMATE_1_NAME, "squareFeet": 216.25, "baseRent": round(216.25 * COST_PER_SQUARE_FOOT, 2)},
    "Medium Bedroom": {"roommate": ROOMMATE_2_NAME, "squareFeet": 194.25, "baseRent": round(194.25 * COST_PER_SQUARE_FOOT, 2)},
    "Small Bedroom": {"roommate": ROOMMATE_3_NAME, "squareFeet": 138.75, "baseRent": round(138.75 * COST_PER_SQUARE_FOOT, 2)}
}


def is_last_day_of_month():
    now = datetime.now(timezone.utc)
    last_day = monthrange(now.year, now.month)[1]
    return now.day == last_day


def lambda_handler(event, context):
    # Only proceed if today is the last day of the month.
    if not is_last_day_of_month():
        print("Today is not the last day of the month. No action taken.")
        return {
            'statusCode': 200,
            'body': 'Today is not the last day of the month. No action taken.'
        }

    # Create an SES client
    ses_client = boto3.client('ses')

    # Retrieve sender and recipient email addresses from AWS Lambda environment variables.
    sender = os.environ.get('SENDER_EMAIL')
    recipient = os.environ.get('RECIPIENT_EMAIL')

    if not sender or not recipient:
        print("Error: SENDER_EMAIL or RECIPIENT_EMAIL environment variable not set.")
        return {
            'statusCode': 500,
            'body': 'Error: SENDER_EMAIL or RECIPIENT_EMAIL environment variable not set.'
        }

    # Call the Selenium scraper to get the latest rent information.
    rent_data = get_latest_rent()
    current_balance = rent_data.get("current_balance", "N/A")
    total_base_rent = sum(values["baseRent"] for values in BEDROOMS.values())

    # If utilities cost is negative, make positive.
    # This means we either overpaid rent or we were credited.
    total_utilities_cost = (current_balance - total_base_rent)
    if total_utilities_cost < 0:
        total_utilities_cost *= -1

    # All roommates split the utilities cost equally.
    utilities_per_roommate = total_utilities_cost / NUM_ROOMMATES

    # Build the email body.
    lines = ["Monthly Rent Calculation Report",
             "==============================", ""]
    lines.append(f"Current Rent Balance from Portal: ${current_balance}\n")
    lines.append(f"Total Calculated Base Rent: ${total_base_rent:.2f}\n")
    lines.append(
        f"Total utilities cost: ${total_utilities_cost:.2f}"
    )
    lines.append(
        f"Utilities cost per person: ${utilities_per_roommate:.2f}\n"
    )

    for room, values in BEDROOMS.items():
        roommate = values["roommate"]
        rent_amount = values["baseRent"]
        lines.append(
            f"{roommate} ({room}): ${(rent_amount - utilities_per_roommate):.2f}")

    body_text = "\n".join(lines)

    # Create the email subject with the current date.
    current_date = datetime.now().strftime("%Y-%m-%d")
    subject = f"Monthly Rent Calculation Report, {current_date}"

    print(f"\n(6) Sending email now to \"{recipient}\"...\n")

    try:
        # Send the email via SES.
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {'Text': {'Data': body_text, 'Charset': 'UTF-8'}}
            }
        )
        return {
            'statusCode': 200,
            'body': f"Email sent successfully! MessageId: {response.get('MessageId')}"
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f"Error sending email: {str(e)}"
        }


if __name__ == "__main__":
    lambda_handler(None, None)
