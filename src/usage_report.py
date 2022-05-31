import datetime
import json

from ibm_cloud_sdk_core import ApiException

from config_helper import get_usage_report_service, get_account_id


# Get IBM Account Summary
# https://cloud.ibm.com/apidocs/usage-reports?code=python#get-account-summary
def get_account_summary():
    print("Get IBM Account Summary")
    try:
        now = datetime.datetime.now()
        billMonth = str(now.year) + "-" + str(now.month)
        service = get_usage_report_service()
        account_summary = service.get_account_summary(account_id=get_account_id(), billingmonth=billMonth).get_result()

        # Print resources billable_cost
        print("\nAccount Summary")
        print("Total Billable Cost: " + str(account_summary['resources']['billable_cost']))
        # Display resources and their billable_cost
        print("\nResources and their billable_cost")
        for resource in account_summary['account_resources']:
            print("Resource: " + resource['resource_name'] + " Billable Cost: " + str(resource['billable_cost']))
    except ApiException as e:
        print("Get IBM Account Summary failed with status code: {0} : {1}".format(e.code, e.message))


# Get IBM Resource Usage
# https://cloud.ibm.com/apidocs/usage-reports?code=python#get-resource-usage
def get_resource_usage():
    print("Get IBM Resource Usage")
    try:
        resource_usage_list = list()
        now = datetime.datetime.now()
        billMonth = str(now.year) + "-" + str(now.month)
        service = get_usage_report_service()
        resource_usage = service.get_resource_usage_account(account_id=get_account_id(),
                                                            billingmonth=billMonth,
                                                            resource_id='containers-kubernetes').get_result()

        # Print resources cost
        print("\nResource Usage")
        # print(json.dumps(resource_usage, indent=2))
        count = 0
        for resource in resource_usage['resources']:
            count += 1
            cost = 0
            for usage in resource['usage']:
                cost += usage['cost']

            # Create a dictionary of resource details
            resource_details = {'resource_instance_id': resource['resource_instance_id'],
                                'resource_group_id': resource['resource_group_id'],
                                'resource_id': resource['resource_id'],
                                'region': resource['region'],
                                'cost': cost}
            resource_usage_list.append(resource_details)
            print(json.dumps(resource_details, indent=2))
            # print("\n")
        print("Total Resources: " + str(count))
    except ApiException as e:
        print("Get IBM Resource Usage failed with status code: {0} : {1}".format(e.code, e.message))
