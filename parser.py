#!/bin/python3
# Please use JSON filename as DB.json and place it in the same directory where this file exists.

import json, smtplib, ssl
from email.mime.text import MIMEText

FROM_EMAIL_ADDRESS = os.environ['FROM_EMAIL_ADDRESS']   # Create env variable on your PC
FROM_EMAIL_PASSWORD = os.environ['FROM_EMAIL_PASSWORD'] # Create env variable on your PC
lines = open('DB.json')
data = json.load(lines)

def send_email(dashboard_name, email):
    print('[+] ' + dashboard_name + ' ---> ' + email + ' >>> EMAIL SENT <<<')
    message = """
    Hi there,\r

    This is to let you know we encountered a system loading issue within our Google Cloud Platform. This has affected your Tableau Dashboard """ + str(dashboard_name.strip()) + """.
    We are currently rectifying the issue and will get back to you once the process has completed loading.
    Sorry for the inconvenience caused.\r
    If you have any questions, please get in touch with me.\r

    Thanks!
    Mini
    """
    msg = MIMEText(message, 'plain')
    msg['Subject'] = dashboard_name + ' - DASHBOARD GOT AFFECTED'   # You can modify this if you wish
    msg['From'] = FROM_EMAIL_ADDRESS
    msg['To'] = email
    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = FROM_EMAIL_ADDRESS, password = FROM_EMAIL_PASSWORD)
    s.sendmail(FROM_EMAIL_PASSWORD, email, msg.as_string())
    s.quit()

def process(data):
    for i in range(0,256):  # Currently checks for upto 256 Dashboard attributes in each dashboard list
        try:
            send_email(data[i]['dashboard_name'], data[i]['alert_email_list'])
        except Exception as e:
            pass

print('\nProcessing the JSON file and sending emails - ')
for data in data:
    if data['is_tableau_affected'] == True and data['is_alert_sent'] == False:  # Main conditions
        process(data['tableau_dashboards'])
print('\nFinished!')

