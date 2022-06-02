import configparser

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import UsageReportsV4, UserManagementV1, ResourceControllerV2, IamIdentityV1
from ibm_vpc import VpcV1
import os

config = configparser.ConfigParser()
config.read(os.getcwd() + '/../config/ibm_config.ini')

# Get IAM API key from config file
iam_apikey = config['IAM']['apikey']
# Create an IAM authenticator.
authenticator = IAMAuthenticator(iam_apikey)


def get_iam_authenticator():
    return authenticator


def get_iam_api_key():
    return iam_apikey


# Get IBM VPC service
def get_vpc_service():
    service = VpcV1(authenticator=authenticator)
    service.set_service_url(config['VPC']['endpoint_url'])
    return service


# Get IBM Usage Reports service
def get_usage_report_service():
    service = UsageReportsV4(authenticator=authenticator)
    return service


# Get IBM User Management service
def get_user_management_service():
    service = UserManagementV1(authenticator=authenticator)
    return service


# Get IBM Resource Controller service
def get_resource_controller_service():
    service = ResourceControllerV2(authenticator=authenticator)
    return service


# Get IBM IAM Identity service
def get_iam_identity_service():
    service = IamIdentityV1(authenticator=authenticator)
    return service


def get_account_id():
    return config['IAM']['account_id']
