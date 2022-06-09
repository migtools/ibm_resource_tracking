# IBM Cloud Resource Tracking 
Report resource utilization for RedHat Migration Engineering Team on IBM Cloud

## To setup dependencies:
Setup Python [virtual environment](https://docs.python.org/3/library/venv.html)

1. Clone this repository
   ```
      git clone https://github.com/amundra02/ibm_reporting.git
   ```
2. Activate the virtual environment and install the required packages
   ```
      pip install --target ./package -r requirements.txt
   ```
## Obtain credentials
These scripts use Google service account credentials to allow bots to run the scripts.

1. Create a new [Google Service Account](https://support.google.com/a/answer/7378726?hl=en)
2. Create a new key in json format
3. Download the key to `credentials.json` file in the current directory
4. Share the Google Sheet with the Google service account email <abc-do-not-delete@xyz.iam.gserviceaccount.com>.

## Create AWS Lambda Function
[Create a Lambda function with the console](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html#getting-started-create-function)

Lambda creates a function and an execution role that grants the function permission to upload logs. The Lambda function assumes the execution role when you invoke your function, and uses the execution role to create credentials for the AWS SDK and to read data from event sources.

### Create Secret with AWS Secret Manager
- Open the Secrets Manager console at https://console.aws.amazon.com/secretsmanager/.
- Choose Store a new secret.
   - For Secret type, choose Other type of secret.
   - In Key/value pairs, enter your secret (IBM_SECRETS_NAME)
      a. Store ibm_iam_apikey and ibm_account_id
   - Create another secret for AWS SES credentials (AWS_SES_SECRET_NAME)
      a. Store AWS_ACCESS_KEY_ID and AWS_ACCESS_SECRET_KEY
- On the Review page, review your secret details, and then choose Store.

### Add permission to read Secrets From SecretManager to Lambda Function
- Open the [Functions page](https://console.aws.amazon.com/lambda/home#/functions) of the Lambda console.
- Choose your function.
- Choose Configuration and then choose Permissions and you will see the execution role.
- Go to execution role and add an inline policy
```
{
 "Version": "2012-10-17",
 "Statement": [
     {
         "Sid": "VisualEditor0",
         "Effect": "Allow",
         "Action": "secretsmanager:GetSecretValue",
         "Resource": [
             "<arn of ibm secrets created above in secret manager>",
             "<arn of aws_ses secrets created above in secret manager>"
         ]
     }
   ]
}
```

### Set AWS Lambda Function Environment Variables
- Change the value of each key as per your needs

```
AWS_SES_SECRET_NAME=<aws_stored_secret_name>
GOOGLE_SHEET_ID=<sheet_id>
IBM_SECRETS_NAME=<aws_stored_secret_name>
SECRETS_REGION=<region_where_secrets_are_stored_aws>
IBM_VPC_Service_URL=https://us-east.iaas.cloud.ibm.com/v1
SHEET_ALL_CLUSTERS="All Clusters"
SHEET_ALL_CLUSTER_INSTANCES="All Cluster Instances"
SHEET_ALL_GATEWAYS="All Gateways"
SHEET_ALL_SUBNETS="All Subnets"
SHEET_ALL_INSTANCES="All Instances"
SHEET_ALL_INSTANCES_COST="All Instances Cost"
SHEET_ALL_VPCS="ALL VPCs"
SHEET_COST_SUMMARY="Cost Summary"
SHEET_OLD_CLUSTERS="Old Clusters"
SHEET_LINK=<google_sheet_link>
SMTP_RECIEVERS= <receivers> (comma seperated)
SMTP_SENDER= <sender>
```
   
### Schedule Execution of Lambda Function
[Schedule](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/RunLambdaSchedule.html#schedule-create-rule) AWS Lambda Functions Using EventBridge events.
   
### Upload code to Lambda Function
A deployment package is required to create or update a Lambda function. The deployment package acts as the source bundle to run your function's code and dependencies on Lambda.

#### To create the deployment package
- Open a command prompt and navigate to the ibm_reporting project directory.
- Install the required libraries to a new package directory
  ```
    pip install --target ./package -r requirements.txt
   ```
- Create a deployment package with the installed library at the root
   ```
   cd package
   zip -r ../deployment-package.zip .
   ```
- Add all the files to the root of the zip file.
   ```
   cd ../src
   zip -g deployment-package.zip *.py credentials.json 
   ```
   Note: (Credential file downloaded while Obtaining credetials above)

#### Deploy your .zip file to the function 
   To deploy the new code to your function, you upload the new .zip file deployment package. Use the [Lambda console](https://docs.aws.amazon.com/lambda/latest/dg/configuration-function-zip.html#configuration-function-update) to upload a .zip file to the function
