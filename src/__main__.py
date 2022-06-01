import datetime

from cluster_infrastructure import get_cluster_info
from usage_report import get_all_instances_cost, get_account_summary


def main(params):
    print(params)

    # Get IBM Account Summary
    if 'bill_month' in params:
        bill_month = params['bill_month']
    else:
        now = datetime.datetime.now()
        bill_month = str(now.year) + "-" + str(now.month)
    get_account_summary(bill_month)

    # Get Cluster Info
    print('\n\n\n')
    for cluster in get_cluster_info():
        print(cluster['name'])


# if __name__ == '__main__':
#     # data = get_vpc_infrastructure_data()
#     # print_vpc_infrastructure_data(data)
#
#     # get_account_summary()
#     # get_resource_instance_usage()
#     # get_instances()
#
#     get_all_instances_cost()
#
#     print(get_cluster_info())
