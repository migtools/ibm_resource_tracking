from ibm_cloud_sdk_core import ApiException

from config_helper import get_iam_identity_service, get_user_management_service, get_account_id


# Get details of a IAM ID using Service ID
# https://cloud.ibm.com/apidocs/iam-identity-token-api?code=python#get-service-id
def get_iam_id_from_service_id(service_id):
    try:
        service = get_iam_identity_service()
        service_id = service_id.replace('iam-', '')
        service_id_details = service.get_service_id(id=service_id).get_result()
        return service_id_details['created_by']
    except ApiException as e:
        if e.code != 403:
            print("Get Service Id Details failed with status code: {0} : {1}".format(e.code, e.message))


# Get User profile by user's IAM ID
# https://cloud.ibm.com/apidocs/user-management?code=python#get-user-profile
def get_user_profile(iam_id):
    try:
        service = get_user_management_service()
        user_profile = service.get_user_profile(account_id=get_account_id(),
                                                iam_id=iam_id).get_result()
        return '{0} {1} <{2}>'.format(user_profile['firstname'], user_profile['lastname'], user_profile['email'])
    except ApiException as e:
        print("Get User Profile failed with status code: {0} : {1}".format(e.code, e.message))
