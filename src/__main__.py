import datetime
from cluster_infrastructure import get_cluster_info, group_cluster_resources
from usage_report import get_all_instances_cost, get_account_summary
from sheet import GoogleSheetEditor, format_sheet
from resource_instances import get_instances
from emailer import send_email, create_email_body, Emailer
import os
from dotenv import load_dotenv

load_dotenv()

OLD_INSTANCE_THRESHOLD = 30


def get_old_clusters_data(all_instances_sheet, old_instances_sheet, tdelta=datetime.timedelta(days=0)):
    instances = all_instances_sheet.read_spreadsheet()
    # existing_old_instances = old_instances_sheet.read_spreadsheet(indexField='InstanceId')
    old_instances = []
    for instance in instances:
        launch_time = datetime.datetime.strptime(instance['launchtime'], "%m/%d/%Y")
        now = datetime.datetime.utcnow() + tdelta
        if (now - launch_time).days > OLD_INSTANCE_THRESHOLD:
            old_instances.append(instance)

    return old_instances


def main(params):
    print(params)

    # Get IBM Account Summary
    if 'bill_month' in params:
        bill_month = params['bill_month']
    else:
        now = datetime.datetime.now()
        bill_month = str(now.year) + "-" + str(now.month)

    account_summary = get_account_summary(bill_month)
    instances, cluster_instances = get_instances()
    cost = get_all_instances_cost(bill_month, instances)
    clusters = get_cluster_info()
    cluster_instances = group_cluster_resources(clusters, instances)
    print(account_summary)

    sheet_id = os.getenv('SHEET_ID')

    allInstancesSheetName = "All Instances"
    allClustersSheetName = "All Clusters"
    allClusterInstancesSheetName = "All Cluster Instances"
    allInstancesCostSheetName = "Instances Cost"
    CostSummarySheetName = "Cost Summary"
    oldClustersSheetName = "Old Clusters"

    allInstancesSheet = GoogleSheetEditor(sheet_id, allInstancesSheetName)
    allClustersInstancesSheet = GoogleSheetEditor(sheet_id, allClusterInstancesSheetName)
    allInstancesCostSheet = GoogleSheetEditor(sheet_id, allInstancesCostSheetName)
    allClustersSheet = GoogleSheetEditor(sheet_id, allClustersSheetName)
    allSummarySheet = GoogleSheetEditor(sheet_id, CostSummarySheetName)
    oldClustersSheet = GoogleSheetEditor(sheet_id, oldClustersSheetName)

    old_clusters = get_old_clusters_data(allClustersSheet, None, tdelta=datetime.timedelta(days=0))

    print(allInstancesSheet.save_data_to_sheet(instances))
    print(allClustersInstancesSheet.save_data_to_sheet(cluster_instances))
    print(allInstancesCostSheet.save_data_to_sheet(cost))
    print(allSummarySheet.save_data_to_sheet(account_summary))
    print(allClustersSheet.save_data_to_sheet(clusters))
    print(oldClustersSheet.save_data_to_sheet(old_clusters))

    format_sheet()

    email_body = create_email_body(clusters)
    send_email(os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_ACCESS_SECRET'), os.getenv('SMTP_RECIEVERS'),
               os.getenv('SMTP_SENDER'), email_body)


main({'bill': '2022-05'})
