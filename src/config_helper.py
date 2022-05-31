import configparser

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import UsageReportsV4, UserManagementV1
from ibm_vpc import VpcV1

config = configparser.ConfigParser()
config.read('../config/ibm_config.ini')

# Get IAM API key from config file
iam_apikey = config['IAM']['apikey']
# Create an IAM authenticator.
authenticator = IAMAuthenticator(iam_apikey)


def get_iam_authenticator():
    return authenticator

def get_iam_api_key():
    return iam_apikey


def get_vpc_service():
    service = VpcV1(authenticator=authenticator)
    service.set_service_url(config['VPC']['endpoint_url'])
    return service


def get_usage_report_service():
    service = UsageReportsV4(authenticator=authenticator)
    # service.set_service_url(config['USAGE.REPORT']['endpoint_url'])
    return service


def get_user_management_service():
    service = UserManagementV1(authenticator=authenticator)
    return service


def get_account_id():
    return config['IAM']['account_id']
