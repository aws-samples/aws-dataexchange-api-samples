/*
Please see the README.md on the GitHub AWS Data Exchange Samples repository for a more detailed overview with links to relevant AWS documentation.

This sample code will show you how to integrate with the [AWS Data Exchange for APIs (Test Product)][APITestProduct]. This simple test product 
echoes the request sent to it, so you can try out different HTTP Methods (GET, POST, etc.), Query String Parameters, Headers, and Body content 
as you explore API based data consumption.  By the end of this exercise you'll know how to use the [AWS Data Exchange Client Software Development 
Kit (SDK)][Tools] with [JavaScript / Node.JS][JavaScript] to make a `SendApiAsset` request to an API based AWS Data Exchange product.  

This will typically consist of three main stages:
1. Import relevant SDK Clients and Interfaces, establish base Client configuration, and instantiate the Client.
    (This stage will remain consistent across all potential AWS Data Exchange for APIs use cases)
2. Define the relevant Provider / Product specific identities)
    (This stage will remain consistent across all uses of a given Product.
3. Define the request-specific parameters based on your business need.
    (This stage will likely change for every request)
Both TypeScript and native JavaScript examples are provided.  The instructions below assume working with the JavaScript file, but the same will work
with the TypeScript file subject to it being transpiled after updates as normal.

To get started, sign in to the AWS Management Console, browse to AWS Data Exchange, search for the "AWS Data Exchange for APIs (Test product)"
Product, and subscribe.
Copy the relevant DataSetId, RevisionId, and AssetId from the Entitled Data page and paste them into the productInfo constant below
(you will likely find they match the sample contents).  Next, update the sendApiAssetCommandInput constant based on your desired request
parameters.  Again, for test purposes, the provided inputs should work just fine.  Finally, install the necessary dependencies
(@aws-sdk/client-dataexchange) using `npm install` and then execute the script with `node adx4api`.

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
*/

//Import all relevant Clients and Interfaces from the @aws-sdk/client-dataexchange SDK
import { DataExchangeClient, DataExchangeClientConfig, SendApiAssetCommand, SendApiAssetCommandInput, SendApiAssetCommandOutput } from "@aws-sdk/client-dataexchange";

//Populate DataExchangeClientConfig with Region and Logger requirements
const dataExchangeClientConfig: DataExchangeClientConfig = {
    region: "us-east-1",
    logger: { 
        debug: console.debug,
        info: console.log,
        warn: console.warn,
        error: console.error
    }
}

//Instantiate DataExchangeClient
const dataExchangeClient = new DataExchangeClient(dataExchangeClientConfig);

//Populate productInfo object based on SendApiAssetCommandInput interface, providing just the mandatory parameters which will be consistent across requests.  The examples below are the AWS Data Exchange for APIs (Test product) in us-east-1
const productInfo: SendApiAssetCommandInput = {
    DataSetId: "8d494cba5e4720e5f6072e280daf70a8",
    RevisionId: "32559097c7d209b02af6de5cad4385fe",
    AssetId: "4e94198cfdb8400793fb3f0411861960"
}

//Populate sendApiAssetCommandInput object based on SendApiAssetCommand interface by merging productInfo object with additional request specific parameters
const sendApiAssetCommandInput: SendApiAssetCommandInput = {
    ...productInfo,
    //This can be GET, PUT, POST, etc. depending on the Provider API
    Method: "POST",
    //This depends on the Provider API and data being requested
    Path: "/",
    //These depend on the Provider API and should be provided as a JSON Object
    QueryStringParameters: {
        param1: "value1",
        param2: "value2"
    },
    //These depend on the Provider API and should be provided as a JSON Object.  Note that the AWS Data Exchange Test API product requires "Content-Type": "application/json"
    RequestHeaders: {
        "Content-Type": "application/json"
    },
    //This depends on the Provider API
    Body: JSON.stringify({
        body_param: "body_param_value"
    })
}

//Create asynchronous function to make an ADX for APIs Subscriber Call
async function makeAdxForApiSubscriberCall (sendApiAssetCommandInput: SendApiAssetCommandInput) {

    //Instantiate SendApiAssetCommand
    const sendApiAssetCommand = new SendApiAssetCommand(sendApiAssetCommandInput);
    
    //Send command using DataExchangeClient
    try {
        const sendApiAssetCommandOutput: SendApiAssetCommandOutput = await dataExchangeClient.send(sendApiAssetCommand);
    } catch (err) {
        //Log errors
        console.log("Error")
        console.error(err);
    }
}

//Invoke function to make ADX for APIs Subscriber Call
makeAdxForApiSubscriberCall(sendApiAssetCommandInput);