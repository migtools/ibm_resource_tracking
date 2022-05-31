import requests
import json

def get_cluster_info(ibm_cloud_api_key):
  account_iam_req = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": "Basic Yng6Yng="
    },
    data={
      "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
      "response_type": "cloud_iam uaa",
      "apikey": ibm_cloud_api_key,
      "uaa_client_id": "cf",
      "uaa_client_secret": ""
    }
  )

  account_iam = json.loads(account_iam_req.text)

  accounts_req = requests.get(
    "https://accounts.cloud.ibm.com/coe/v2/accounts",
    headers={
      "Content-Type": "application/json",
      "Authorization": "bearer " + account_iam["access_token"],
      "Accept": "application/json"
    }
  )

  accounts = json.loads(accounts_req.text)

  if accounts["total_results"] > 1:
    print("Handle more than one account!")

  account_guid = accounts['resources'][0]['metadata']['guid']


  cluster_iam_req = requests.post(
    "https://iam.cloud.ibm.com/identity/token",
    headers={
      "Content-Type": "application/x-www-form-urlencoded",
      "Authorization": "Basic Yng6Yng="
    },
    data={
      "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
      "response_type": "cloud_iam uaa",
      "apikey": ibm_cloud_api_key,
      "uaa_client_id": "cf",
      "uaa_client_secret": "",
      "bss_account": account_guid
    }
  )

  cluster_iam = json.loads(cluster_iam_req.text)

  output = { "clusters": [] }
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

def extract_relevant_cluster_info(clusters):
  output = []
  for cluster in clusters:
    pass

  return output