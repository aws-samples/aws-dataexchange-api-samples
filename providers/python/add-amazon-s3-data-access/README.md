# Add Amazon S3 Data Access (Python)

This example will create a data set with for AWS Data Exchange for Amazon S3 (Preview). The data set will contain an
Amazon S3 Access Point, which enables subscribers to have read-only access to the shared locations specified. Shared
locations can be a combination of Amazon S3 prefixes and specific keys, or an entire Amazon S3 bucket.

### Setup

Install the requirements:

```bash
$ pip3 install -r requirements.txt
```

Set the AWS access key and secret environment variables:

```
$ export AWS_ACCESS_KEY_ID=<your-access-key-id>
$ export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
$ export AWS_SESSION_TOKEN=<your-session-token>
```

The user needs the **AWSDataExchangeProviderFullAccess** IAM policy associated with your role/account. Find out more
about IAM policies on AWS Data Exchange [here](https://docs.aws.amazon.com/data-exchange/latest/userguide/auth-access.html).

The target Amazon S3 bucket must have the bucket owner enforced setting applied. Attach the following bucket policy to grant AWS Data Exchange permissions to
correctly manage S3 Access Points on your behalf, replacing `<Bucket ARN>` with the ARN of the target Amazon S3
bucket:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "<Bucket ARN>",
                "<Bucket ARN>/*"
            ],
            "Condition": {
                "StringEquals": {
                    "s3:DataAccessPointAccount": [
                        "337040091392",
                        "504002150500",
                        "366362662752",
                        "330489627928",
                        "291973504423",
                        "461002523379",
                        "036905324694",
                        "540564263739",
                        "675969394711",
                        "108584782536",
                        "844053218156"
                    ]
                }
            }
        }
    ]
}
```

### Example Usage

Get usage help: `python3 add-amazon-s3-access.py --help`

Share an Amazon S3 bucket: `python3 add-amazon-s3-access.py --data-set-name 'publisher-script-example' --bucket 'example-source-bucket' --region us-east-1`

Share prefixes and keys within an Amazon S3 bucket: `python3 add-amazon-s3-access.py --data-set-name 'publisher-script-example' --bucket 'example-source-bucket' --region 'us-east-1' --key 'createJob.png' --prefix 'Folder1' --prefix 'Folder2'`

Share prefixes and keys within an Amazon S3 bucket encrypted with customer-managed KMS: `python3 add-amazon-s3-access.py --data-set-name 'publisher-script-example-kms' --bucket 'example-source-bucket-kms' --region 'us-east-1' --key 'createJob.png' --prefix 'Folder1' --prefix 'Folder2' --kms-key-arn 'arn:aws:kms:us-east-1:123456789:key/abc-def-ghi-jkl-mno`

**Note**: You may specify a `data-set-id` parameter to add an S3 data access to an existing data set. Any existing
data access will be replaced.
