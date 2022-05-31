import requests
import json

from config_helper import get_account_id, get_iam_api_key

# Returns a list of dicts containing information about each cluster from the IBM API.
def get_cluster_info():
  cluster_iam_req = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": "Basic Yng6Yng="
    },
    data={
      "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
      "response_type": "cloud_iam uaa",
      "apikey": get_iam_api_key(),
      "uaa_client_id": "cf",
      "uaa_client_secret": "",
      "bss_account": get_account_id()
    }
  )

  cluster_iam = json.loads(cluster_iam_req.text)

  # --- Clusters ---
  # --- Classic clusters ---
  get_classic_clusters_req = requests.get(
    "https://containers.cloud.ibm.com/global/v2/classic/getClusters",
    headers={ "Authorization": "bearer " + cluster_iam['access_token'] }
  )
  get_classic_clusters = json.loads(get_classic_clusters_req.text)

  # --- VPC clusters ---
  get_vpc_clusters_req = requests.get(
    "https://containers.cloud.ibm.com/global/v2/vpc/getClusters?provider=vpc-gen2",
    headers={ "Authorization": "bearer " + cluster_iam['access_token'] }
  )
  get_vpc_clusters = json.loads(get_vpc_clusters_req.text)

  return get_classic_clusters + get_vpc_clusters