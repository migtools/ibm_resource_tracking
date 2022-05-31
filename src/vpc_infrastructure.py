from ibm_cloud_sdk_core import ApiException
from config_helper import get_vpc_service

vpc_infrastructure_data = {'VPCs': [], 'Subnets': [], 'Instances': [], 'Public Gateways': []}


def get_all_vpcs():
    try:
        service = get_vpc_service()
        vpcs = service.list_vpcs().get_result()['vpcs']
        add_resource_details(vpcs, 'VPCs')
    except ApiException as e:
        print("List VPCs failed with status code: {0} : {1}".format(e.code, e.message))


# Listing Subnets
def get_all_subnets():
    try:
        service = get_vpc_service()
        subnets = service.list_subnets().get_result()['subnets']
        add_resource_details(subnets, 'Subnets')
    except ApiException as e:
        print("List Subnets failed with status code: {0} : {1}".format(e.code, e.message))


# Listing Public Gateways
def get_all_public_gateways():
    try:
        service = get_vpc_service()
        gateways = service.list_public_gateways().get_result()['public_gateways']
        add_resource_details(gateways, 'Public Gateways')
    except ApiException as e:
        print("List Public Gateways failed with status code: {0} : {1}".format(e.code, e.message))


# Listing Instances
def get_all_instances():
    try:
        service = get_vpc_service()
        instances = service.list_instances().get_result()['instances']
        add_resource_details(instances, 'Instances')
    except ApiException as e:
        print("List Instances failed with status code: {0} : {1}".format(e.code, e.message))


def add_resource_details(resources, resource_type):
    for resource in resources:
        # Create a dictionary of resource details
        resource_details = {'id': resource['id'], 'name': resource['name'],
                            'status': resource['status'], 'created_at': resource['created_at']}
        # Add the resource details to the global dictionary
        vpc_infrastructure_data[resource_type].append(resource_details)


def print_vpc_infrastructure_data(data):
    for resource_type, resources in data.items():
        print('Listing', resource_type)
        for resource in resources:
            print(resource)
        print('\n')


def get_vpc_infrastructure_data():
    get_all_vpcs()
    get_all_subnets()
    get_all_instances()
    get_all_public_gateways()
    print('Data retrieved successfully')
    return vpc_infrastructure_data
