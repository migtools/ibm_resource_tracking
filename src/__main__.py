import datetime
from email import message

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
    get_account_summary(bill_month)

    # Get Cluster Info
    print('\n\n\n')
    for cluster in get_cluster_info():
        print(cluster['name'])


if __name__ == '__main__':
    
    instances,clusters = get_instances()
    cost = get_all_instances_cost()

    sheet_id = os.getenv('SHEET_ID')

    allInstancesSheetName = "All Instances"
    allClustersSheetName = "All Clusters"
    CostSummarySheetName = "Cost Summary"
    
    
    allInstancesSheet = GoogleSheetEditor(sheet_id, allInstancesSheetName)
    allClustersSheet = GoogleSheetEditor(sheet_id, allClustersSheetName)
    allSummarySheet = GoogleSheetEditor(sheet_id, CostSummarySheetName)

    
    print(allInstancesSheet.save_data_to_sheet(instances))
    print(allClustersSheet.save_data_to_sheet(clusters))
    print(allSummarySheet.save_data_to_sheet(cost))

 
    message = "Test Email"
    send_email(os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_ACCESS_SECRET'), os.getenv('SMTP_RECIEVERS'), os.getenv('SMTP_SENDER'), message)



