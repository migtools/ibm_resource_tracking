import json
import os

import boto3
import requests
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import UsageReportsV4, UserManagementV1, ResourceControllerV2, IamIdentityV1
from ibm_vpc import VpcV1


def get_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)
    get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    secret = get_secret_value_response['SecretString']
    secret = json.loads(secret)
    return secret


# Get credentials from AWS Secret Manager
# Region where the secret is stored
region = os.getenv('SECRETS_REGION')
secrets = get_secret(os.getenv('IBM_SECRETS_NAME'), region)
iam_apikey, account_id = secrets['ibm_iam_apikey'], secrets['ibm_account_id']

# Create an IAM authenticator.
authenticator = IAMAuthenticator(iam_apikey)


def get_account_id():
    return account_id


# Get AWS Access Key and Secret Key
def get_aws_access_key_and_secret_key():
    aws_secret = get_secret(os.getenv('AWS_SES_SECRET_NAME'), region)
    return aws_secret['AWS_ACCESS_KEY_ID'], aws_secret['AWS_ACCESS_SECRET_KEY']


# Get IBM VPC service
def get_vpc_service():
    service = VpcV1(authenticator=authenticator)
    service.set_service_url(os.getenv('IBM_VPC_Service_URL'))
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
            "apikey": iam_apikey,
            "uaa_client_id": "cf",
            "uaa_client_secret": "",
            "bss_account": account_id,
        }
    )

    cluster_iam = json.loads(cluster_iam_req.text)
    return cluster_iam['access_token']
