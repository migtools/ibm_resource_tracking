import datetime

from cluster_infrastructure import delete_cluster

OLD_INSTANCE_THRESHOLD = 30


def get_old_clusters_data(all_instances_sheet, old_instances_sheet):
    instances = all_instances_sheet.read_spreadsheet()
    existing_old_instances = old_instances_sheet.read_spreadsheet(indexField='cluster_id')
    old_instances = []

    for instance in instances:
        launch_time = datetime.datetime.strptime(instance['launchtime'], "%m/%d/%Y")
        now = datetime.datetime.utcnow()
        if (now - launch_time).days > OLD_INSTANCE_THRESHOLD:
            instance['save'] = existing_old_instances.get(instance['cluster_id'], {}).get('save', instance['save'])
            old_instances.append(instance)

    return old_instances


def terminate_instances(old_instances_sheet):
    old_instances = old_instances_sheet.read_spreadsheet()
    deleted_instances = 0
    deleted_clusters_names = []
    for instance in old_instances:
        if 'save' not in instance['save'].lower():
            if delete_cluster(instance['cluster_id']):
                deleted_instances += 1
                deleted_clusters_names.append(instance["name"])

    return deleted_instances, deleted_clusters_names
