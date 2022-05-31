import configparser

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_vpc import VpcV1

from vpc_infrastructure import get_all_vpcs, get_all_subnets, get_all_instances, get_all_public_gateways
from cluster_infrastructure import get_cluster_info

config = configparser.ConfigParser()
config.read('../config/ibm_config.ini')

# Get IAM API key from config file
iam_apikey = config['IAM']['apikey']
# Create an IAM authenticator.
authenticator = IAMAuthenticator(iam_apikey)

if __name__ == '__main__':
    print(get_cluster_info(iam_apikey))
    # service = VpcV1(authenticator=authenticator)
    # service.set_service_url(config['VPC']['endpoint_url'])
    # get_all_vpcs(service)
    # get_all_subnets(service)
    # get_all_instances(service)
    # get_all_public_gateways(service)
