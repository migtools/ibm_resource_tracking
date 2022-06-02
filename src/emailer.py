import boto3
import os
from datetime import datetime, timedelta


from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

class Emailer(object):
    def __init__(self, smtp_addr, username, password):
        self.conn = SMTP(smtp_addr)
        self.username = username
        self.password = password
        self.conn.set_debuglevel(False)

    def send_email(self, sender, receivers, subject, message):
        """ sends message from sender to receivers
        """
        msg = MIMEText(message, 'html')
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ','.join(receivers)
        try:
            self.conn.login(self.username, self.password)
            self.conn.sendmail(sender, receivers, msg.as_string())
            print(sender)
            print(receivers)
        except Exception as e:
            print(str(e))
        finally:
            self.conn.quit()



def send_email(aws_access_key_id, aws_secret_access_key, toaddresses, fromaddress, message):

    toaddresseslist = toaddresses.split(",")

    try:
        ses_client = boto3.client("ses", region_name="us-east-1",
                                aws_access_key_id=aws_access_key_id, 
                                aws_secret_access_key=aws_secret_access_key)
        CHARSET = "UTF-8"

        response = ses_client.send_email(
            Destination={
                "ToAddresses": toaddresseslist,
            },
            Message={
                "Body": {
                    "Html": {
                        "Charset": CHARSET,
                        "Data": message,
                    }
                },
                "Subject": {
                    "Charset": CHARSET,
                    "Data": "IBM Cloud Cleanup Notification",
                },
            },
            Source=fromaddress,
        )
    except Exception as e:
        print("Sending mail failed: {0}".format(e.message))



def create_email_body(clusters):
    sheet_link = os.environ['SHEET_LINK']
    
    scheduled = (datetime.utcnow() + timedelta(days=4)).strftime("%a, %b %d, %y")

    summary_email = ""

    for data in clusters:
        summary_email += data['name'] + "<br>"

    message = """
    All,<br>
    <br>            
    This is a reminder to let you know that the IBM cleanup automation script will terminate some of the long running instances.<br>
    <br>
    You can save your instances from automatic deletion by writing 'Save' in the 'Saved' column in 'All Clusters' spreadsheet below:
    <br>
    <br>
    <a href="{}">{}</a>
    <br>
    <br>
    Next cleanup is scheduled on <b>{}</b>.
    <br><br>
    Here's the summary of instances scheduled for termination:
    <br><br>
    {}
    <br><br>
    Thank you.<br>
            """
        
    return message.format(sheet_link, sheet_link, scheduled,summary_email)