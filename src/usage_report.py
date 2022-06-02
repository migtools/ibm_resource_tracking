import json

from ibm_cloud_sdk_core import ApiException
from config_helper import get_usage_report_service, get_account_id


# Get IBM Account Summary
# https://cloud.ibm.com/apidocs/metering-reporting?code=python#get-account-summary
def get_account_summary(bill_month):
    print("Get IBM Account Summary")
    try:
        cost_summary = []
        service = get_usage_report_service()
        account_summary = service.get_account_summary(account_id=get_account_id(), billingmonth=bill_month).get_result()

        # Print resources billable_cost
        print("\nAccount Summary")
        print("Total Billable Cost: " + str(account_summary['resources']['billable_cost']))

        for resource in account_summary['account_resources']:
            cost_summary.append({
                "Resource": resource['resource_name'],
                "Billable Cost": str(resource['billable_cost'])
            })
        return cost_summary
    except ApiException as e:
        print("Get IBM Account Summary failed with status code: {0} : {1}".format(e.code, e.message))


# Get IBM Resource Usage
# https://cloud.ibm.com/apidocs/metering-reporting?code=python#get-resource-usage-account
def get_all_resource_instance_usage(bill_month):
    print("Get IBM All Resource Instance Usage")
    resource_instance_usage_dict = {}
    try:
        service = get_usage_report_service()
        start = None
        # Get all available resource instances usage
        while True:
            usage_response = service.get_resource_usage_account(account_id=get_account_id(),
                                                                billingmonth=bill_month,
                                                                start=start).get_result()
            # Extract all resource instances usage and its cost
            for resource in usage_response['resources']:
                cost = 0
                for usage in resource['usage']:
                    cost += usage['cost']

                instance_usage = {'consumer_id': resource['consumer_id'] if 'consumer_id' in resource else '',
                                  'cost': round(cost, 2)}
                if resource['resource_instance_id'] in resource_instance_usage_dict:
                    resource_instance_usage_dict[resource['resource_instance_id']].append(instance_usage)
                else:
                    resource_instance_usage_dict[resource['resource_instance_id']] = [instance_usage]

            # Check if there are more pages
            if 'next' not in usage_response:
                break
            start = usage_response['next']['offset']

        print("\nResource Usage", len(resource_instance_usage_dict))
        # print(json.dumps(resource_instance_usage_dict, indent=2))
    except ApiException as e:
        print("Get All IBM Resource Instance Usage failed with status code: {0} : {1}".format(e.code, e.message))
    return resource_instance_usage_dict


# Get resource instance usage in an account for a specific resource instance
# https://cloud.ibm.com/apidocs/metering-reporting?code=python#get-resource-usage-account
def get_resource_instance_usage(bill_month, instances):
    print("Get IBM Resource Instance Usage")
    try:
        resource_instance_usage_list = list()
        service = get_usage_report_service()
        # For each instance, get the instance id and get its usage
        for instance in instances:
            instance_id = instance['instance_id']
            instance_usage = service.get_resource_usage_account(account_id=get_account_id(),
                                                                billingmonth=bill_month,
                                                                resource_instance_id=instance_id).get_result()['resources']
            # print(json.dumps(instance_usage, indent=2))
            for resource in instance_usage:
                cost = 0
                for usage in resource['usage']:
                    cost += usage['cost']
                instance['cost'] = round(cost, 2)
                resource_instance_usage_list.append(instance)
        # Print instance usage
        print("\nResource Instance Usage", len(resource_instance_usage_list))
        print(json.dumps(resource_instance_usage_list, indent=2))
    except ApiException as e:
        print("Get IBM Resource Instance Usage failed with status code: {0} : {1}".format(e.code, e.message))


# Associate cost with resource instance
def get_all_instances_cost(bill_month, all_instances):
    all_instances_usage = get_all_resource_instance_usage(bill_month)

    all_instances_cost = []
    for instance in all_instances:
        if instance['instance_id'] in all_instances_usage:
            for instance_usage in all_instances_usage[instance['instance_id']]:
                instance.update(instance_usage)
                all_instances_cost.append(instance)

    return all_instances_cost
