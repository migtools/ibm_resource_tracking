import configparser
import os
import requests
import json

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import UsageReportsV4, UserManagementV1, ResourceControllerV2, IamIdentityV1
from ibm_vpc import VpcV1

config = configparser.ConfigParser()
config.read(os.getcwd() + '/../config/ibm_config.ini')

# Get IAM API key from config file
iam_apikey = config['IAM']['apikey']

# Create an IAM authenticator.
authenticator = IAMAuthenticator(iam_apikey)

# Returns the IAM Authenticator
def get_iam_authenticator():
    return authenticator


# Returns the raw API key
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

# Returns the current account ID
def get_account_id():
    return config['IAM']['account_id']

# Returns the access token used for clusters
def get_cluster_access_token():
    cluster_iam_req = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic Yng6Yng="
        },
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "response_type": "cloud_iam uaa",
            "apikey": get_iam_api_key(),
            "uaa_client_id": "cf",
            "uaa_client_secret": "",
            "bss_account": get_account_id(),
        }
    )

    cluster_iam = json.loads(cluster_iam_req.text)

    return cluster_iam['access_token']