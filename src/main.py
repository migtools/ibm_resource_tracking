import json

from ibm_cloud_sdk_core import ApiException

<<<<<<< HEAD
from vpc_infrastructure import get_all_vpcs, get_all_subnets, get_all_instances, get_all_public_gateways
from cluster_infrastructure import get_cluster_info

import json

# Not necessary, just nice to have for debugging
def pretty_print_json(x):
  print(json.dumps(x, indent=2))
=======
from src.config_helper import get_user_management_service, get_account_id
from usage_report import get_account_summary, get_resource_usage
from vpc_infrastructure import get_vpc_infrastructure_data, print_vpc_infrastructure_data
>>>>>>> origin/main


# List users
def get_all_users():
    print("Listing Users")
    try:
        service = get_user_management_service()
        users = service.list_users(account_id=get_account_id()).get_result()['resources']
        print(json.dumps(users, indent=2))
    except ApiException as e:
        print("List Users failed with status code: {0} : {1}".format(e.code, e.message))




if __name__ == '__main__':
<<<<<<< HEAD
    service = VpcV1(authenticator=authenticator)
    service.set_service_url(config['VPC']['endpoint_url'])
    get_all_vpcs(service)
    get_all_subnets(service)
    get_all_instances(service)
    get_all_public_gateways(service)

    print(get_cluster_info(iam_apikey))
=======
    data = get_vpc_infrastructure_data()
    print_vpc_infrastructure_data(data)

    get_account_summary()
    get_resource_usage()
    # get_all_users()
>>>>>>> origin/main
