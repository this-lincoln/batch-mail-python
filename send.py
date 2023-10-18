import os
import sys
import json
import datetime
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (
    max_emails_per_hour,
    mail_password,
    mail_ssl_port,
    mail_sender,
    mail_host
)

def _send_email(recipient, subject, content):

    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = mail_sender
    message["To"] = recipient
    message.attach(
        MIMEText(content, "html")
    )

    with smtplib.SMTP_SSL(mail_host, mail_ssl_port, context=context) as server:

        server.login(mail_sender, mail_password)

        server.sendmail(
            mail_sender, recipient, message.as_string()
        )

# Getting arguments
try:
    template = sys.argv[1]
    email_title = sys.argv[2]
    email_subject = sys.argv[3]
except IndexError:
    sys.exit("Required arguments not defined. Template file, email title and email subject.")

# Defining paths
template_full_path = os.path.join("templates", template)
default_template_full_path = os.path.join("templates", "default.html")

# Checking if files exists
if not os.path.exists("templates/"):
    sys.exit("Templates folder not found.")

if not os.path.exists("recipients.json"):
    sys.exit("Recipients file not found.")

if not os.path.exists(template_full_path):

    use_default = int(input("Template not found. Use the default template? 1 = True, 2 = False \n"))

    if use_default == 1:

        if not os.path.exists(default_template_full_path):
            sys.exit("Template file not found and no default file defined.")

        template_full_path = default_template_full_path
    
    if use_default == 2:
        sys.exit("Aborting.")

# Getting content
content = open(template_full_path, "r")
content = content.read()
content = content.replace("{{ email_title }}", email_title)

# Getting recipients list
recipients_file = open("recipients.json", "r")
recipients = json.load(recipients_file)

responses = []

for recipient in recipients:
    content = content.replace(
        "{{ recipient_name }}",
        recipient["name"]
    )

    try:
        _send_email(recipient["email"], email_subject, content)
        responses.append(
            {"recipient": recipient["email"], "status": "success", "delivery_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
        )
    except Exception as err:
        print(err)
        responses.append(
            {"recipient": recipient["email"], "status": "failure", "delivery_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
        )

response_file_name = f"{ email_subject }_{ datetime.datetime.now().strftime('%Y_%m_%d_%H_%M') }.json"
response_file_name_full_path = os.path.join("responses", response_file_name)

with open(response_file_name_full_path, "w") as response_file:   
    json.dump(responses, response_file)