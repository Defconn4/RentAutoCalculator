# Copy this file to `login_info.py` and replace the placeholders with your credentials if you are running this locally.

# Alternatively, if using inside of AWS Lambda, set these values as environment variables instead.
# If you're spooked about hardcoding your credentials, you can use AWS Secrets Manager to store them securely
# and retrieve them at runtime. I have not implemented this in the script, but it is a good practice to follow.

# Replace with your own login credentials (DO NOT COMMIT THIS FILE TO GITHUB)

# URL of your property's login page:
LOGIN_URL = "your-login-url"

# Email and password for you rent payment account:
EMAIL = "your-email@example.com"
PASSWORD = "your-secure-password"

# Add the names of your roommates here:
ROOMMATE_1_NAME = "Gamer1"
ROOMMATE_2_NAME = "Gamer2"
ROOMMATE_3_NAME = "Gamer3"

# For running locally, fill in the following constants:
SENDER_EMAIL = "your-secondary-email@example.com"
RECIPIENT_EMAIL = "your-email@example.com"
