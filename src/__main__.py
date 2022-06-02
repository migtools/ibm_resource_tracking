import datetime
from cluster_infrastructure import get_cluster_info
from usage_report import get_all_instances_cost, get_account_summary
from sheet import GoogleSheetEditor
from resource_instances import get_instances
from emailer import send_email

import os
from dotenv import load_dotenv
load_dotenv()


def main(params):
    print(params)

    # Get IBM Account Summary
    if 'bill_month' in params:
        bill_month = params['bill_month']
    else:
        now = datetime.datetime.now()
        bill_month = str(now.year) + "-" + str(now.month)
        
    account_summary = get_account_summary(bill_month)
    instances,cluster_instances = get_instances()
    cost = get_all_instances_cost(bill_month)
    clusters = get_cluster_info()

    print(account_summary)
    
    sheet_id = os.getenv('SHEET_ID')

    allInstancesSheetName = "All Instances"
    allClustersSheetName = "All Clusters"
    allClusterInstancesSheetName = "All Cluster Instances"
    allInstancesCostSheetName = "Instances Cost"
    CostSummarySheetName = "Cost Summary"
    
    
    allInstancesSheet = GoogleSheetEditor(sheet_id, allInstancesSheetName)
    allClustersInstancesSheet = GoogleSheetEditor(sheet_id, allClusterInstancesSheetName)
    allInstancesCostSheet = GoogleSheetEditor(sheet_id, allInstancesCostSheetName)
    allClustersSheet = GoogleSheetEditor(sheet_id, allClustersSheetName)
    allSummarySheet = GoogleSheetEditor(sheet_id, CostSummarySheetName)
    
    print(allInstancesSheet.save_data_to_sheet(instances))
    print(allClustersInstancesSheet.save_data_to_sheet(cluster_instances))
    print(allInstancesCostSheet.save_data_to_sheet(cost))
    print(allSummarySheet.save_data_to_sheet(account_summary))
    print(allClustersSheet.save_data_to_sheet(clusters))

 
    # message = "Test Email"
    # send_email(os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_ACCESS_SECRET'), os.getenv('SMTP_RECIEVERS'), os.getenv('SMTP_SENDER'), message)


main({'bill':'2022-05'})
