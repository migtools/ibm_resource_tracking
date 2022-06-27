import datetime

from cluster_infrastructure import delete_cluster

OLD_INSTANCE_THRESHOLD = 30


def get_old_clusters_data(all_instances_sheet, old_instances_sheet, tdelta=datetime.timedelta(days=0)):
    instances = all_instances_sheet.read_spreadsheet()
    existing_old_instances = old_instances_sheet.read_spreadsheet(indexField='cluster_id')
    old_instances = []

    for instance in instances:
        launch_time = datetime.datetime.strptime(instance['launchtime'], "%m/%d/%Y")
        now = datetime.datetime.utcnow() + tdelta
        if (now - launch_time).days > OLD_INSTANCE_THRESHOLD:
            instance['save'] = existing_old_instances.get(instance['cluster_id'], {}).get('save', '')
            old_instances.append(instance)

    return old_instances


def terminate_instances(all_instances_sheet, old_instances_sheet):
    old_instances = get_old_clusters_data(all_instances_sheet, old_instances_sheet, datetime.timedelta(days=-4))
    instance_ids = []
    deleted_instances = 0
    for inst in old_instances:
        if 'save' not in inst['save'].lower():
            instance_id = inst['cluster_id']
            instance_region = inst["region"]
            instance_ids.append([instance_id, instance_region])

    for inst in instance_ids:
        successful = delete_cluster(inst[0])
        if successful:
            deleted_instances += 1
    return deleted_instances
