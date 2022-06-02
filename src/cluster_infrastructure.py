import requests
import json

from config_helper import get_account_id, get_iam_api_key, get_cluster_access_token


# Returns a list of dicts containing information about each cluster from the IBM API.
def get_cluster_info():
    access_token = get_cluster_access_token()

    # --- Clusters ---
    # --- Classic clusters ---
    get_classic_clusters_req = requests.get(
        "https://containers.cloud.ibm.com/global/v2/classic/getClusters",
        headers={"Authorization": "bearer " + access_token}
    )
    get_classic_clusters = json.loads(get_classic_clusters_req.text)

    # --- VPC clusters ---
    get_vpc_clusters_req = requests.get(
        "https://containers.cloud.ibm.com/global/v2/vpc/getClusters?provider=vpc-gen2",
        headers={"Authorization": "bearer " + access_token}
    )
    get_vpc_clusters = json.loads(get_vpc_clusters_req.text)

    all_clusters = get_classic_clusters + get_vpc_clusters

    cluster_info = []

    for cluster in all_clusters:

        created_at_raw = cluster['createdDate'].split("T")[0].split("-")
        created_at = created_at_raw[1] + "/" + created_at_raw[2] + "/" +created_at_raw[0]

        cluster_info.append({
            'cluster_id' : cluster['id'],
            'name':cluster['name'],
            'region':cluster['region'],
            'launchtime': created_at,
            'worker_count': cluster['workerCount'],
            'save':''
        })

    return cluster_info

# Deletes a cluster with the specified id or name. Returns True if successful,
# False otherwise
def delete_cluster(id_or_name):
    all_cluster_info = get_cluster_info()
    this_cluster_info = None

    for info in all_cluster_info:
        if info['cluster_id'] == id_or_name or info['name'] == id_or_name:
            this_cluster_info = info
            break

    if this_cluster_info == None:
        raise Exception('Cluster with id or name "' + id_or_name + '" does not exist!')

    print(json.dumps(this_cluster_info))

    print(this_cluster_info['resourceGroup'])

    # NOTE: Docs state that v1 API doesn't work for vpc-gen2 clusters, but it 
    # seems to work fine for now...
    # https://cloud.ibm.com/apidocs/kubernetes#removecluster
    remove_cluster_req = requests.delete(
        'https://containers.cloud.ibm.com/global/v1/clusters/'
            + info['cluster_id'] + '?deleteResources=true',
        headers={ 
            'Authorization': "bearer " + get_cluster_access_token(), 
            'X-Auth-Resource-Group': this_cluster_info['resourceGroup']
        }
    )

    print(remove_cluster_req.text)

    if remove_cluster_req.status_code == 204:
        print(f'Removed cluster with id or name: "{id_or_name}"')
        return True

    if remove_cluster_req.status_code == 401:
        print('Unauthorized. The IAM token is invalid or expired.')
    elif remove_cluster_req.status_code == 404:
        print('The cluster with the following id or name could not be found: "' 
            + id_or_name + '"')
    elif remove_cluster_req.status_code == 500:
        print('Internal server error')

    return False
