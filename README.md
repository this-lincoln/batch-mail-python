# README

This is a simple script I created to help me with simple tasks where I need to send a couple emails as a batch, but nothing professional. Feel free to use. Every improvement feedback is welcome, but remember to be nice.

## To start

- Add the recipient emails to the recipients.json file. Add name and email as you can see in the file sample.

- Create a simple html template file under the templates folder. You can always use the default template as a starting point. Right now we can only replace email title and recipient name, but it is easy to expand that in the future.

- Define your credentials on config.py , you will need to add your credentials, be carefull when sharing that. If you want to send emails via GMAIL you should check this tutorial. [How To Set Up Your Gmail SMTP Settings (2023 Guide)](https://mailmeteor.com/blog/gmail-smtp-settings)

- Define the number of emails you want to send at each hour to avoid being blocked or overcharged by your server.

## To send the list of emails:

`python send.py "TEMPLATE.HTML" "EMAIL TITLE" "EMAIL SUBJECT"`