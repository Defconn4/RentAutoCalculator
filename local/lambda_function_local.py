import os
import sys
import boto3
from datetime import datetime, timezone
from calendar import monthrange

from rent_scraper_local import get_latest_rent

COST_PER_SQUARE_FOOT = 4.44
TOTAL_SQUARE_FEET = 549.25
NUM_ROOMMATES = 3

# Add the parent directory to sys.path (for importing login_info.py constants)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)


# Import roommate names (Ensure login_info.py exists)
try:
    from login_info import SENDER_EMAIL, RECIPIENT_EMAIL, ROOMMATE_1_NAME, ROOMMATE_2_NAME, ROOMMATE_3_NAME
except ImportError:
    raise Exception(
        "Error: 'login_info.py' is missing. Please create it with your credentials.")


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
    # NOTE: Commented out for local execution.
    # if not is_last_day_of_month():
    #     print("Today is not the last day of the month. No action taken.")

    # Create an SES client
    ses_client = boto3.client('ses')

    # Call the Selenium scraper to get the latest rent information.
    rent_data = get_latest_rent()
    current_balance = rent_data.get("current_balance", "N/A")
    total_base_rent = sum(values["baseRent"] for values in BEDROOMS.values())

    # If utilities cost is negative, make positive.
    # This means we either overpaid rent or we were credited.
    total_utilities_cost = (current_balance - total_base_rent)
    if total_utilities_cost <= 0:
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

    print(f"\n(6) Sending email now to \"{RECIPIENT_EMAIL}\"...\n")

    try:
        # Send the email via SES.
        response = ses_client.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [RECIPIENT_EMAIL]},
            Message={
                'Subject': {'Data': subject, 'Charset': 'UTF-8'},
                'Body': {'Text': {'Data': body_text, 'Charset': 'UTF-8'}}
            }
        )
        print(
            f"Email sent successfully! MessageId: {response.get('MessageId')}")

    except Exception as e:
        print(f"Error sending email: {str(e)}")


if __name__ == "__main__":
    lambda_handler(None, None)
