# Auto Export To S3 (Python)

This sample shows how to set up an AWS Lambda function which will automatically export all newly published revisions for a given Data Set to S3. All infrastructure is setup using Terraform.

Logical Prerequisites:
* Data Set ID for an active subscription to a Data Set on AWS Data Exchange
* Revision ID for the target first revision to export

Technical Prerequisites:
* Terraform is installed
* AWS CLI is installed and has a profile configured with access to create IAM, S3, and Lambda resources and issue permissions to CloudWatch, S3, and DataExchange

> The deployment will target us-east-1 and use the "default" AWS CLI profile by default.  Update the "profile" and "region" configuration in the "provider"
section of the terraform template to modify these defaults.

**Please note that this sample is provided for demonstration and learning purposes only, and should be reviewed for alignment with organisational policies and best practices before any production use.**


### First Time Terraform Deployment

```
$ terraform init
```

### Build and Deploy
```
$ terraform plan
$ terraform apply
```

Terraform will create the following resources:

1. S3 Bucket to store exported Data Exchange assets (files)
1. Lambda Function to perform the export (with necessary IAM permissions)
1. EventBridge (CloudWatch Events) Rule to trigger Lambda

Each time a new Revision is added to the DataSet you provide on deployment, the Assets will be automatically exported to S3 as a response to the CloudWatch Event sent by AWS Data Exchange.