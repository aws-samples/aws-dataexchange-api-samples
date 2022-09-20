#!/usr/bin/env python3

"""
Please see the README.md on the GitHub AWS Data Exchange Samples repository for a more detailed overview with links to relevant AWS documentation.

This sample code will show you how to integrate with the [AWS Data Exchange for APIs (Test Product)][APITestProduct]. This simple test product
echoes the request sent to it, so you can try out different HTTP Methods (GET, POST, etc.), Query String Parameters, Headers, and Body content
as you explore API based data consumption.  By the end of this exercise you'll know how to use the [AWS Data Exchange Client Software Development
Kit (SDK)][Tools] with [Python][AWSDataExchangeSDKForPython] to make a `SendApiAsset` request to an API based AWS Data Exchange product.

This will typically consist of three main stages:
1. Import relevant SDK Clients and Interfaces, establish base Client configuration, and instantiate the Client.
    (This stage will remain consistent across all potential AWS Data Exchange for APIs use cases)
2. Define the relevant Provider / Product specific identities)
    (This stage will remain consistent across all uses of a given Product.
3. Define the request-specific parameters based on your business need.
    (This stage will likely change for every request)

To get started, sign in to the AWS Management Console, browse to AWS Data Exchange, search for the "AWS Data Exchange for APIs (Test product)"
Product, and subscribe.
Copy the relevant DataSetId, RevisionId, and AssetId from the Entitled Data page and paste them into the productInfo constant below
(you will likely find they match the sample contents).  Next, update the sendApiAssetCommandInput constant based on your desired request
parameters.  Again, for test purposes, the provided inputs should work just fine.  Finally, install the necessary dependencies
(@aws-sdk/client-dataexchange) using `npm install`, transpile from TypeScript to Javascript using `tsc`, and then execute the script with `node adx4api`.

To assist with finding the necessary inputs for the productInfo and sendApiAssetCommandInput constants, the Data Exchange console provides
Sample CLI requests as shown below.  The first 3 parameters map to the productInfo constant, and the rest map to sendApiAssetCommandInput
aws dataexchange send-api-asset \
  --data-set-id 8d494cba5e4720e5f6072e280daf70a8 \
  --revision-id 32559097c7d209b02af6de5cad4385fe \
  --asset-id 4e94198cfdb8400793fb3f0411861960 \
  --method POST \
  --path "/" \
  --query-string-parameters 'param1=value1,param2=value2' \
  --request-headers 'header=header_value' \
  --body "{\"body_param\":\"body_param_value\"}"

By default, this code will authenticate against AWS Data Exchange using the configuration of the environment in which it runs.
For local development purposes, this will typically use credentials provided to the AWS CLI by `aws configure`
When running on Amazon EC2 it will typically use the EC2 Instance Profile, and for AWS Lambda it will use the Lambda Execution Role.
"""

import json
import boto3

# Instantiate DataExchange client for us-east-1 region
CLIENT = boto3.client('dataexchange', region_name = 'us-east-1')


# product info from entitled products, this uses AWS Data Exchange API sample product from us-east-1 region
DATA_SET_ID = '8d494cba5e4720e5f6072e280daf70a8'
REVISION_ID = '32559097c7d209b02af6de5cad4385fe'
ASSET_ID    = '4e94198cfdb8400793fb3f0411861960'

# Additional parameters for the send_api_asset call
BODY = json.dumps({'body_param': 'body_param_value'})
METHOD = 'POST'
PATH = '/'
QUERY_STRING_PARAMETERS = {'param1': 'value1', 'param2': 'value2'}


response = CLIENT.send_api_asset(
    DataSetId=DATA_SET_ID,
    RevisionId=REVISION_ID,
    AssetId=ASSET_ID,
    Method=METHOD,
    Path=PATH,
    Body=BODY,
    QueryStringParameters=QUERY_STRING_PARAMETERS
)

print('Response Headers:')
for header in response['ResponseHeaders']:
    value = response['ResponseHeaders'][header]
    print(f' {header}: {value}')

print()
print('Response Body:')
print( response['Body'] )
