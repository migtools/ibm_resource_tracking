import boto3

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
                    "Text": {
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
        print("Sending mail failed: {0} : {1}".format(e.code, e.message))
