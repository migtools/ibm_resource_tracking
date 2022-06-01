from cluster_infrastructure import get_cluster_info
from usage_report import get_all_instances_cost


if __name__ == '__main__':
    # data = get_vpc_infrastructure_data()
    # print_vpc_infrastructure_data(data)

    # get_account_summary()
    # get_resource_instance_usage()
    # get_instances()

    get_all_instances_cost()

    print(get_cluster_info())
