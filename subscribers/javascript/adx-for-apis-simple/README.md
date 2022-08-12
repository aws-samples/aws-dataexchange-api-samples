# README

This sample code will show you how to integrate with the [AWS Data Exchange for APIs (Test Product)][APITestProduct]. This simple test product echoes the request sent to it, so you can try out different HTTP Methods (GET, POST, etc.), Query String Parameters, Headers, and Body content as you explore API based data consumption.  By the end of this exercise you'll know how to use the [AWS Data Exchange Client Software Development Kit (SDK)][Tools] with [JavaScript / Node.JS][AWSDataExchangeSDKForJavaScript] to make a `SendApiAsset` request to an API based AWS Data Exchange product.  

This will typically consist of three main stages:
1. Import relevant SDK Clients and Interfaces, establish base Client configuration, and instantiate the Client. \
_(This stage will remain consistent across all potential AWS Data Exchange for APIs use cases)_
2. Define the relevant Provider / Product specific identities) \
_(This stage will remain consistent across all uses of a given Product)_
3. Define the request-specific parameters based on your business need. \
_(This stage will likely change for every request)_

Both TypeScript and native JavaScript examples are provided in this sample.  The instructions below assume working with the JavaScript file, but the same will work with the TypeScript file subject to it being transpiled after updates as normal.

## Getting Started
To get started, sign in to the AWS Management Console, browse to AWS Data Exchange, search for the ["AWS Data Exchange for APIs (Test product)"][APITestProduct] Product, and subscribe.
Copy the relevant `DataSetId`, `RevisionId`, and `AssetId` from the Entitled Data page and paste them into the `productInfo` constant in the code sample (adx4apis.js) (you will likely find they match the sample contents).  Next, update the `sendApiAssetCommandInput` constant based on your desired request parameters.  Again, for test purposes, the provided inputs should work just fine.  Finally, install the necessary dependencies (@aws-sdk/client-dataexchange) using `npm install` and then execute the script with `node adx4api`.

To assist with finding the necessary inputs for the `productInfo` and `sendApiAssetCommandInput` constants, the Data Exchange console provides Sample CLI requests as shown below.  The first 3 parameters map to the productInfo constant, and the rest map to sendApiAssetCommandInput
```
aws dataexchange send-api-asset \
  --data-set-id 8d494cba5e4720e5f6072e280daf70a8 \
  --revision-id 32559097c7d209b02af6de5cad4385fe \
  --asset-id 4e94198cfdb8400793fb3f0411861960 \
  --method POST \
  --path "/" \
  --query-string-parameters 'param1=value1,param2=value2' \
  --request-headers 'header=header_value' \
  --body "{\"body_param\":\"body_param_value\"}"
```

## Authentication
By default, this code will authenticate against AWS Data Exchange using the configuration of the environment in which it runs. For local development purposes, this will typically use credentials provided to the AWS CLI by [`aws configure`][AWSConfigure]. When running on Amazon EC2 it will typically use the [EC2 Instance Profile][IAMRolesForEC2], and for AWS Lambda it will use the [Lambda Execution Role][LambdaExecutionRole].

[APITestProduct]: https://us-east-1.console.aws.amazon.com/dataexchange/home?region=us-east-1#/products/prodview-pgkxrurxwmp76
[Tools]: https://aws.amazon.com/tools/
[AWSDataExchangeSDKForJavaScript]: https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/clients/client-dataexchange/index.html
[IAMRolesForEC2]: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html
[LambdaExecutionRole]: https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html
[AWSConfigure]: https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html