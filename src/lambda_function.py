import json
import main


def lambda_handler(event, context):
    status_code = 200
    msg = "Success!"
    try:
        main.main(event)
    except Exception as e:
        status_code = 404
        msg = str(e)
        print(str(e))

    return {
        'statusCode': status_code,
        'body': json.dumps(msg)
    }
