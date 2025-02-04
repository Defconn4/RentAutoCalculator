aws ses send-email \
 --from "fcos624@gmail.com" \
 --destination "ToAddresses=fcos624@gmail.com" \
 --message "Subject={Data=Test Email,Charset=utf8},Body={Text={Data=This is a test email from AWS SES.,Charset=utf8}}" \
 --region us-east-1

- Download the Chrome Labs Chromium Binary to run Selenium (here)[https://googlechromelabs.github.io/chrome-for-testing/#stable].
- If you don't want to peruse the versions, here is version (1.33.0.6943.53 for Win64)[https://storage.googleapis.com/chrome-for-testing-public/133.0.6943.53/win64/chrome-win64.zip]
- - Extract the .zip file into the directory of this project.

1. Copy `login_info.example.py` to `login_info.py`
2. Replace placeholders with your actual credentials
3. Run the script
