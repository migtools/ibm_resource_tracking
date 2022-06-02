from config_helper import get_resource_controller_service
from iam_identity import get_iam_id_from_service_id, get_user_profile


# Get a list of all resource instances
# https://cloud.ibm.com/apidocs/resource-controller/resource-controller?code=python#list-resource-instances
def get_instances():
    print("Getting resource instances...")
    service = get_resource_controller_service()
    resource_instances = []
    clusters = []
    start = None
    # Get all the available resource instances
    while True:
        response = service.list_resource_instances(start=start).get_result()

        for resource in response['resources']:
            created_at = get_formatted_date(resource['created_at'])
            updated_at = get_formatted_date(resource['updated_at'])

            resource_details = {'instance_id': resource['id'], 'name': resource['name'],
                                'region': resource['region_id'],
                                'resource_group_id': resource['resource_group_id'], 'type': resource['type'],
                                'resource_id': resource['resource_id'], 'state': resource['state'],
                                'created_by': get_owner_details(resource['created_by']), 'created_at': created_at,
                                'updated_at': updated_at}
            resource_instances.append(resource_details)

            if resource['type'] == "container_instance":
                clusters.append(resource_details)

        # If there are more pages, get the next page
        if response['next_url'] is None:
            break
        start = response['next_url'].split('start=')[1]

    print("Number of resource instances: " + str(len(resource_instances)))
    resource_instances.sort(key=lambda x: x['resource_id'], reverse=False)
    clusters.sort(key=lambda x: x['resource_id'], reverse=False)
    return resource_instances, clusters


def get_formatted_date(resource):
    created_at_raw = resource.split("T")[0].split("-")
    created_at = created_at_raw[1] + "/" + created_at_raw[2] + "/" + created_at_raw[0]
    return created_at


# Get owner details for a resource instance
def get_owner_details(service_id):
    # If service id starts with 'IBMid-', it is an IAM ID
    if service_id.startswith('IBMid-'):
        return get_user_profile(service_id)
    iam_id = get_iam_id_from_service_id(service_id)
    return get_user_profile(iam_id) if iam_id is not None else service_id
