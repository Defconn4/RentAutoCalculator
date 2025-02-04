aws ses send-email \
 --from "fcos624@gmail.com" \
 --destination "ToAddresses=fcos624@gmail.com" \
 --message "Subject={Data=Test Email,Charset=utf8},Body={Text={Data=This is a test email from AWS SES.,Charset=utf8}}" \
 --region us-east-1

1. Copy `login_info.example.py` to `login_info.py`
2. Replace placeholders with your actual credentials
3. Run the script
