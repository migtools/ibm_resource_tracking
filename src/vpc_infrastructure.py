from ibm_cloud_sdk_core import ApiException


# List all VPCs
def get_all_vpcs(service):
    print("List all VPCs")
    try:
        vpcs = service.list_vpcs().get_result()['vpcs']
        print_resource_details(vpcs)
    except ApiException as e:
        print("List VPCs failed with status code: {0} : {1}".format(e.code, e.message))


# Listing Subnets
def get_all_subnets(service):
    print("Listing Subnets")
    try:
        subnets = service.list_subnets().get_result()['subnets']
        print_resource_details(subnets)
    except ApiException as e:
        print("List Subnets failed with status code: {0} : {1}".format(e.code, e.message))


# Listing Public Gateways
def get_all_public_gateways(service):
    print("Listing Public Gateways")
    try:
        gateways = service.list_public_gateways().get_result()['public_gateways']
        print_resource_details(gateways)
    except ApiException as e:
        print("List Public Gateways failed with status code: {0} : {1}".format(e.code, e.message))


# Listing Instances
def get_all_instances(service):
    print("Listing Instances")
    try:
        instances = service.list_instances().get_result()['instances']
        print_resource_details(instances)
    except ApiException as e:
        print("List Instances failed with status code: {0} : {1}".format(e.code, e.message))


def print_resource_details(resources):
    for resource in resources:
        print(resource['id'], "\t", resource['name'], "\t", resource['created_at'], "\t", resource['status'])
