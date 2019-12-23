import * as events from '@aws-cdk/aws-events';
import * as targets from '@aws-cdk/aws-events-targets';
import * as lambda from '@aws-cdk/aws-lambda';
import * as iam from '@aws-cdk/aws-iam';
import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';

export class AutoExportToS3Stack extends cdk.Stack {
  constructor(app: cdk.App, id: string) {
    super(app, id);

    const s3Bucket = new s3.Bucket(this, 'DataExchangeAssetsBucket', {
      encryption: s3.BucketEncryption.S3_MANAGED
    });

    const lambdaFunction = new lambda.Function(this, 'AutoExportToS3Lambda', {
      code: new lambda.AssetCode('dist/lambda'),
      handler: 'exportToS3.handler',
      timeout: cdk.Duration.minutes(15),
      runtime: lambda.Runtime.NODEJS_12_X,
      environment: {
        S3_BUCKET: s3Bucket.bucketName
      }
    });

    lambdaFunction.role.addManagedPolicy(iam.ManagedPolicy.fromAwsManagedPolicyName('AWSDataExchangeSubscriberFullAccess'));
    lambdaFunction.addToRolePolicy(new iam.PolicyStatement({
      actions: [ 's3:PutObject', 's3:PutObjectAcl' ],
      resources: [ cdk.Fn.join('', [ s3Bucket.bucketArn, '/*' ]) ]
    }));

    new events.Rule(this, 'DataExchangeRule', {
      description: 'Each time an ENTITLED Data Set is updated with a new Revision, this Rule will be triggered.',
      eventPattern: {
        source: [ 'aws.dataexchange' ],
        detailType: [ 'Revision Published To Data Set' ]
      },
      targets: [ new targets.LambdaFunction(lambdaFunction) ]
    });
  }
}

const app = new cdk.App();
new AutoExportToS3Stack(app, 'AutoExportToS3Stack');
app.synth();