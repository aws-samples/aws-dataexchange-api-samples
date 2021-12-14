# [Deprecated] Auto Export To S3 (JavaScript)

> This sample is deprecated in favor of using the official AWS Data Exchange feature for auto exporting S3 revisions: https://aws.amazon.com/about-aws/whats-new/2021/09/aws-data-exchange-export-third-party-data-updates/

This sample shows how to set up an AWS Lambda function which will automatically export all newly published revisions to S3. All infrastructure is setup using the [AWS CDK](https://docs.aws.amazon.com/cdk/latest/guide/home.html).

To run the sample, set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_SESSION_TOKEN`.


### First Time CDK User

```
$ npm install -g cdk
$ cdk bootstrap
```

### Build and Deploy
```
$ npm run-script deploy
```

The CloudFormation will create the following resources:

1. S3 Bucket
1. Lambda Function (with necessary IAM permissions)
1. CloudWatch Rule

Each time a new Revision is added to a DataSet to which your account is subscribed, the Assets will be automatically exported to S3 as a response to the CloudWatch Event sent by AWS Data Exchange.