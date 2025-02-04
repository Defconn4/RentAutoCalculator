import boto3
import os
from datetime import datetime
from calendar import monthrange


# Import roommate names (Ensure login_info.py exists)
try:
    from login_info import ROOMMATE_1_NAME, ROOMMATE_2_NAME, ROOMMATE_3_NAME
except ImportError:
    raise Exception(
        "Error: 'login_info.py' is missing. Please create it with your credentials.")

# If pasting into AWS Lambda, paste everything below this line to EOF.
COST_PER_SQUARE_FOOT = 4.44
TOTAL_SQUARE_FEET = 549.25

# Bedroom square footage and rent calculations
BEDROOMS = {
    "Master Bedroom": {"roommate": ROOMMATE_1_NAME, "squareFeet": 216.25, "baseRent": round(216.25 * COST_PER_SQUARE_FOOT, 2)},
    "Medium Bedroom": {"roommate": ROOMMATE_2_NAME, "squareFeet": 194.25, "baseRent": round(194.25 * COST_PER_SQUARE_FOOT, 2)},
    "Small Bedroom": {"roommate": ROOMMATE_3_NAME, "squareFeet": 138.75, "baseRent": round(138.75 * COST_PER_SQUARE_FOOT, 2)}
}


def is_last_day_of_month():
    now = datetime.now(datetime.timezone.utc)()
    last_day = monthrange(now.year, now.month)[1]
    return now.day == last_day


def lambda_handler(event, context):
    # Only send the email if today is the last day of the month.
    if not is_last_day_of_month():
        return {
            'statusCode': 200,
            'body': 'Today is not the last day of the month. No action taken.'
        }

    # Create an SES client
    ses_client = boto3.client('ses')

    # Retrieve sender and recipient email addresses from environment variables
    sender = os.environ.get('SENDER_EMAIL')
    recipient = os.environ.get('RECIPIENT_EMAIL')

    if not sender or not recipient:
        return {
            'statusCode': 500,
            'body': 'Error: SENDER_EMAIL or RECIPIENT_EMAIL environment variable not set.'
        }

    # Format the email body
    lines = ["Monthly Rent Calculation Report",
             "==============================", ""]

    # TODO: Need to grab the rent from my rental portal
    total_rent = 0.0

    # total_base_rent = sum(rent_results.values())
    # utils_rent = 0.0 # total_rent - total_base_rent
    # total_rent_with_utils = total_base_rent + utils_rent

    # Check if total_rent from online matches my calculation
    # if total_rent_with_utils != total_rent:
    #     lines.append(f"Warning: Total rent from online ({total_rent}) does not match my calculation ({total_rent_with_utils})")

    lines.append(f"Total Monthly Rent: ${total_rent:.2f}\n\n")
    for room, values in BEDROOMS.items():
        roommate_name = values["roommate"]
        rent_amount = values["baseRent"]
        lines.append(f"{roommate_name} ({room}): ${rent_amount:.2f}")

    body_text = "\n".join(lines)

    # Email subject with current date
    current_date = datetime.utcnow().strftime("%Y-%m-%d")
    subject = f"Monthly Rent Calculation Report, {current_date}"

    try:
        # Send the email via SES
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
