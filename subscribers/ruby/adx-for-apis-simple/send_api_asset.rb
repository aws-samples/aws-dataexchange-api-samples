#Please see the README.md on the GitHub AWS Data Exchange Samples repository for a more detailed overview with links to relevant AWS documentation.
#
#This code is provided as a sample of how to use the AWS Data Exchange Client Software Development Kit (SDK) to connect to Data Exchange For APIs
#based Data Sets.  This will typically consist of three main stages:
#1. Import relevant SDK Clients, establish base Client configuration, and instantiate the Client.
#    (This stage will remain consistent across all potential AWS Data Exchange for APIs use cases)
#2. Define the relevant Provider / Product specific identities)
#    (This stage will remain consistent across all uses of a given Product.
#3. Define the request-specific parameters based on your business need.
#    (This stage will likely change for every request)
#
#To get started, sign in to the AWS Management Console, browse to AWS Data Exchange, search for the "AWS Data Exchange for APIs (Test product)"
#Product, and subscribe.
#Copy the relevant DataSetId, RevisionId, and AssetId from the Entitled Data page and paste them into the productInfo constant below
#
#Familiarity with ruby programming language is assumed. For ruby programming language documentation visit: https://www.ruby-lang.org/en/documentation/quickstart/
#
#To assist with finding the necessary inputs for the asset_id, revision_id and data_set_id, the Data Exchange console provides
#Sample CLI requests as shown below.  The first 3 parameters map to the product specific identities, and the rest are additional send_api_asset call parameters
#aws dataexchange send-api-asset \
#  --data-set-id 8d494cba5e4720e5f6072e280daf70a8 \
#  --revision-id 32559097c7d209b02af6de5cad4385fe \
#  --asset-id 4e94198cfdb8400793fb3f0411861960 \
#  --method POST \
#  --path "/" \
#  --query-string-parameters 'param1=value1,param2=value2' \
#  --request-headers 'header=header_value' \
#  --body "{\"body_param\":\"body_param_value\"}"
#
#By default, this code will authenticate against AWS Data Exchange using the configuration of the environment in which it runs.
#For local development purposes, this will typically use credentials provided to the AWS CLI by `aws configure`
#When running on Amazon EC2 it will typically use the EC2 Instance Profile, and for AWS Lambda it will use the Lambda Execution Role.
#
#To execute this code:
#
#bundle install
#ruby send_api_asset.rb

require 'aws-sdk-dataexchange'
require 'json'

#obtain credentials from 'default' profile in shared credentials file
credentials = Aws::SharedCredentials.new

client = Aws::DataExchange::Client::new(region: 'us-east-1', credentials: credentials)

# Product specific identities
asset_id = "4e94198cfdb8400793fb3f0411861960"
revision_id = "32559097c7d209b02af6de5cad4385fe"
data_set_id  = "8d494cba5e4720e5f6072e280daf70a8"

# adjust the send_api_asset call parameters based on your needs.
resp = client.send_api_asset(
    body: {"body_param" => "body_param_value"}.to_json,
    query_string_parameters: {"param1" => "value1", "param2" => "value2"},
    asset_id: asset_id,
    revision_id: revision_id,
    data_set_id: data_set_id,
    method: "POST",
    path: "/"
)

puts "Response Headers:"
puts resp.response_headers
puts
puts "Response Body:"
puts resp.body.string
