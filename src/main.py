import datetime
import os

from cluster_infrastructure import get_cluster_info, group_cluster_resources
from config_helper import get_aws_access_key_and_secret_key
from emailer import send_email, create_email_body,create_deletedinstances_email_body
from instance_operations import get_old_clusters_data, terminate_instances
from resource_instances import get_instances
from sheet import GoogleSheetEditor, format_sheet
from usage_report import get_all_instances_cost, get_account_summary
from vpc_infrastructure import get_vpc_infrastructure_data


def main(params):
    print(params)
    bill_month = get_bill_month(params)

    sheet_id = os.getenv('GOOGLE_SHEET_ID')
    allInstancesSheetName = os.getenv('SHEET_ALL_INSTANCES')
    allClustersSheetName = os.getenv('SHEET_ALL_CLUSTERS')
    allClusterInstancesSheetName = os.getenv('SHEET_ALL_CLUSTER_INSTANCES')
    allInstancesCostSheetName = os.getenv('SHEET_ALL_INSTANCES_COST')
    CostSummarySheetName = os.getenv('SHEET_COST_SUMMARY')
    oldClustersSheetName = os.getenv('SHEET_OLD_CLUSTERS')
    allVPCsSheetName = os.getenv('SHEET_ALL_VPCS')
    allSubnetsSheetName = os.getenv('SHEET_ALL_SUBNETS')
    allGatewaysSheetName = os.getenv('SHEET_ALL_GATEWAYS')
    historicalDeletionSumamrySheetName = os.getenv('HISTORICAL_DELETION_SUMMARY')

    allInstancesSheet = GoogleSheetEditor(sheet_id, allInstancesSheetName)
    allClustersInstancesSheet = GoogleSheetEditor(sheet_id, allClusterInstancesSheetName)
    allInstancesCostSheet = GoogleSheetEditor(sheet_id, allInstancesCostSheetName)
    allClustersSheet = GoogleSheetEditor(sheet_id, allClustersSheetName)
    allSummarySheet = GoogleSheetEditor(sheet_id, CostSummarySheetName)
    oldClustersSheet = GoogleSheetEditor(sheet_id, oldClustersSheetName)
    allVPCsSheet = GoogleSheetEditor(sheet_id, allVPCsSheetName)
    allSubnetsSheet = GoogleSheetEditor(sheet_id, allSubnetsSheetName)
    allGatewaysSheet = GoogleSheetEditor(sheet_id, allGatewaysSheetName)
    historicalDeletionSheet = GoogleSheetEditor(sheet_id, historicalDeletionSumamrySheetName)

    if params['command'] == 'report':
        account_summary = get_account_summary(bill_month)
        instances, cluster_instances = get_instances()
        cost = get_all_instances_cost(bill_month, instances)
        clusters = get_cluster_info()
        vpc_infrastructure_data = get_vpc_infrastructure_data()

        print(allInstancesSheet.save_data_to_sheet(instances))
        print(allClustersInstancesSheet.save_data_to_sheet(cluster_instances))
        print(allInstancesCostSheet.save_data_to_sheet(cost))
        print(allSummarySheet.save_data_to_sheet(account_summary))
        print(allClustersSheet.save_data_to_sheet(clusters))
        print(allVPCsSheet.save_data_to_sheet(vpc_infrastructure_data['VPCs']))
        print(allSubnetsSheet.save_data_to_sheet(vpc_infrastructure_data['Subnets']))
        print(allGatewaysSheet.save_data_to_sheet(vpc_infrastructure_data['Public Gateways']))
        old_clusters = get_old_clusters_data(allClustersSheet, oldClustersSheet, tdelta=datetime.timedelta(days=0))
        print(oldClustersSheet.save_data_to_sheet(old_clusters))
        format_sheet()

    elif params['command'] == 'generate_termination_email_summary':
        instances, _ = get_instances()
        clusters = get_cluster_info()
        grouped_cluster_instances = group_cluster_resources(clusters, instances)
        deleted_instances_info = historicalDeletionSheet.read_spreadsheet()[-1]
        email_body = create_email_body(grouped_cluster_instances, oldClustersSheet,deleted_instances_info)
        aws_access_key_id, aws_secret_access_key = get_aws_access_key_and_secret_key()
        send_email(aws_access_key_id, aws_secret_access_key, os.getenv('SMTP_RECIEVERS'), os.getenv('SMTP_SENDER'),
                   email_body)
        print(email_body)

    elif params['command'] == 'terminate_instances':
        deleted_instances = terminate_instances(allClustersSheet, oldClustersSheet)
        print("Clusters deleted" + str(deleted_instances))
       
        #append current date and number of terminated instaces to the sheet
        deletion_data = [
        {"date_deleted":  datetime.datetime.now().strftime('%m/%d/%Y'),
         "no_of_deleted_clusters":deleted_instances
        }]

        print(historicalDeletionSheet.append_data_to_sheet(deletion_data))


# Get the bill month from the event parameters
def get_bill_month(params):
    if 'bill_month' in params:
        bill_month = params['bill_month']
    else:
        now = datetime.datetime.now()
        bill_month = str(now.year) + "-" + str(now.month)
    return bill_month
