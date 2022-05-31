import json

from ibm_cloud_sdk_core import ApiException

from src.config_helper import get_user_management_service, get_account_id
from usage_report import get_account_summary, get_resource_usage
from vpc_infrastructure import get_vpc_infrastructure_data, print_vpc_infrastructure_data


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
    data = get_vpc_infrastructure_data()
    print_vpc_infrastructure_data(data)

    get_account_summary()
    get_resource_usage()
    # get_all_users()
