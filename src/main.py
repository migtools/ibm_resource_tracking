import datetime
import os

from cluster_infrastructure import get_cluster_info
from config_helper import get_aws_access_key_and_secret_key
from emailer import send_email, create_email_body, termination_email_body, reminder_email_body
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
    historicalDeletionSummarySheetName = os.getenv('HISTORICAL_DELETION_SUMMARY')

    allInstancesSheet = GoogleSheetEditor(sheet_id, allInstancesSheetName)
    allClustersInstancesSheet = GoogleSheetEditor(sheet_id, allClusterInstancesSheetName)
    allInstancesCostSheet = GoogleSheetEditor(sheet_id, allInstancesCostSheetName)
    allClustersSheet = GoogleSheetEditor(sheet_id, allClustersSheetName)
    allSummarySheet = GoogleSheetEditor(sheet_id, CostSummarySheetName)
    oldClustersSheet = GoogleSheetEditor(sheet_id, oldClustersSheetName)
    allVPCsSheet = GoogleSheetEditor(sheet_id, allVPCsSheetName)
    allSubnetsSheet = GoogleSheetEditor(sheet_id, allSubnetsSheetName)
    allGatewaysSheet = GoogleSheetEditor(sheet_id, allGatewaysSheetName)
    historicalDeletionSheet = GoogleSheetEditor(sheet_id, historicalDeletionSummarySheetName)

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
        format_sheet()

    elif params['command'] == 'generate_termination_email_summary':
        old_clusters = get_old_clusters_data(allClustersSheet, oldClustersSheet)
        print(oldClustersSheet.save_data_to_sheet(old_clusters))
        deleted_instances_info = get_deleted_instances(historicalDeletionSheet)
        email_body = termination_email_body(oldClustersSheet, deleted_instances_info)
        send_out_email(email_body)
        print("Termination Email", email_body)

    elif params['command'] == 'termination_reminder':
        deleted_instances_info = get_deleted_instances(historicalDeletionSheet)
        email_body = reminder_email_body(oldClustersSheet, deleted_instances_info)
        send_out_email(email_body)
        print("Reminder Email", email_body)

    elif params['command'] == 'terminate_instances':
        deleted_instances, deleted_clusters_names = terminate_instances(oldClustersSheet)
        print("Clusters deleted" + str(deleted_instances))

        # append current date and number of terminated instances to the sheet
        deletion_data = [
            {"date_deleted": str(datetime.datetime.now().date()),
             "deleted_clusters": ",".join(deleted_clusters_names),
             "no_of_deleted_clusters": deleted_instances
             }]

        print(historicalDeletionSheet.append_data_to_sheet(deletion_data))


def send_out_email(email_body):
    if len(email_body) > 0:
        aws_access_key_id, aws_secret_access_key = get_aws_access_key_and_secret_key()
        send_email(aws_access_key_id, aws_secret_access_key, os.getenv('SMTP_RECIEVERS'), os.getenv('SMTP_SENDER'),
                   email_body)


def get_deleted_instances(historicalDeletionSheet):
    historical_data = historicalDeletionSheet.read_spreadsheet()
    if len(historical_data) > 0:
        deleted_instances_info = historical_data[-1]
    else:
        deleted_instances_info = {'no_of_deleted_clusters': 0,
                                  'date_deleted': str(datetime.datetime.now().date())}
    return deleted_instances_info


# Get the bill month from the event parameters
def get_bill_month(params):
    if 'bill_month' in params:
        bill_month = params['bill_month']
    else:
        now = datetime.datetime.now()
        bill_month = str(now.year) + "-" + str(now.month)
    return bill_month
