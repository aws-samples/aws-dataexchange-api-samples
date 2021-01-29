#
# AWS Data Exchange automated revision export to S3 upon published Cloudwatch event 
#

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.25.0"
    }
  }
}

# Configure AWS Provider account & target region
provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

# Require dataset ID and initial revision ID to be input before the deployment can take place (the dataset must be subscribed to manually in the AWS Console)
variable "datasetID" {
  type = string
  description = "REQUIRED: the ID for the data set"
}

variable "revisionID" {
  type = string
  description = "REQUIRED: the ID for an initial Revision to download immediately."
}

# Create S3 bucket to store exported data in
resource "aws_s3_bucket" "DataS3Bucket" {
  bucket_prefix = "datas3bucket"
}

# Apply all Public Access Block controls by default
resource "aws_s3_bucket_public_access_block" "DataS3BucketPublicAccessBlock" {
  bucket = aws_s3_bucket.DataS3Bucket.id
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

# Create Lambda function using Python code included in lambda_code.zip
resource "aws_lambda_function" "FunctionGetNewRevision" {
  function_name = "FunctionGetNewRevision"
  filename = "lambda_code.zip"
  source_code_hash = filebase64sha256("lambda_code.zip")
  handler = "index.handler"
  environment {
    variables = {
      S3_BUCKET = aws_s3_bucket.DataS3Bucket.bucket
    }
  }
  role = aws_iam_role.RoleGetNewRevision.arn
  runtime = "python3.7"
  timeout = 180
}

# Create new EventBridge rule to trigger on the Revision Published To Data Set event
resource "aws_cloudwatch_event_rule" "NewRevisionEventRule" {
  name = "NewRevisionEventRule"
  description = "New Revision Event"
  event_pattern = jsonencode({
    source = ["aws.dataexchange"],
    detail-type = ["Revision Published To Data Set"],
    resources = [var.datasetID]
  })
}

# Create trigger for EventBRidge rule to Lambda function
resource "aws_cloudwatch_event_target" "TargetGetNewRevision" {
  rule = aws_cloudwatch_event_rule.NewRevisionEventRule.name
  target_id = "TargetGetNewRevision"
  arn = aws_lambda_function.FunctionGetNewRevision.arn
}

# Create Lambda Execution Role
resource "aws_iam_role" "RoleGetNewRevision" {
  name = "RoleGetNewRevision"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

# Add Required Policies to Lambda Execution Role
resource "aws_iam_role_policy" "RoleGetNewRevisionPolicy" {
  name = "RoleGetNewRevisionPolicy"
  role = aws_iam_role.RoleGetNewRevision.id
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dataexchange:StartJob",
          "dataexchange:CreateJob",
          "dataexchange:GetJob",
          "dataexchange:ListRevisionAssets",
          "dataexchange:GetAsset"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = "s3:GetObject",
        Resource = "arn:aws:s3:::*aws-data-exchange*"
        Condition = {
          "ForAnyValue:StringEquals" = {
            "aws:CalledVia" = [
              "dataexchange.amazonaws.com"
            ]
          }
        }
      },
      {
        Effect = "Allow",
        Action = "s3:PutObject",
        Resource = [
          aws_s3_bucket.DataS3Bucket.arn,
          join("",[aws_s3_bucket.DataS3Bucket.arn,"/*"])
        ]
      }
    ]
  })
}

# Attach LambdaBasicExecutionRole AWS Managed Policy to Lambda Execution Role
resource "aws_iam_role_policy_attachment" "RoleGetNewRevisionAttachment" {
  role = aws_iam_role.RoleGetNewRevision.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Provide permission for EventBridge to invoke Lambda function
resource "aws_lambda_permission" "LambdaInvokePermission" {
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.FunctionGetNewRevision.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.NewRevisionEventRule.arn
}

# Invoke Lambda function for initial data export
data "aws_lambda_invocation" "FistRevision" {
  function_name = aws_lambda_function.FunctionGetNewRevision.function_name
  input = jsonencode(
    {
      InitialInit = {
        data_set_id = var.datasetID,
        RevisionIds = var.revisionID
      }
    }
  )
}