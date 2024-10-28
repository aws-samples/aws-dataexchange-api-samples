# Create file-based data grant on AWS Data Exchange (Python)

This script automates the process of creating and populating an AWS Data Exchange dataset with files from an S3 bucket. It creates a new dataset, adds specified S3 objects as assets to a new revision within that dataset, and finalizes the revision. Finally, it creates a data grant for the dataset, allowing a specified AWS account to access the data, optionally with an expiration date.

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

The user needs to list and read objects from the specified S3 bucket. You'll need the following S3 permissions:
- s3:GetObject
- s3:ListBucket

Here's a sample IAM policy that includes the necessary permissions:
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket",
                "s3:GetObject"
            ],
            "Resource": [
                "arn:aws:s3:::your-bucket-name",
                "arn:aws:s3:::your-bucket-name/*"
            ]
        }
    ]
}
```
### Example Usage

Get usage help: `python3 create-data-grant.py --help`

Create data grant for Amazon S3 Bucket: `python3 create-data-grant.py --dataset-name example_dataset --bucket s3://example-bucket --grant-name example_bucket_grant --grant-end-date 2024-12-01 --target-account-id 123456789012`

Create data grant for prefix(s) within Amazon S3 Bucket: `python3 create-data-grant.py --dataset-name example_prefix_dataset --bucket example-bucket --prefix data/ --grant-name example_prefix_grant --grant-end-date 2024-12-01 --target-account-id 123456789012`

Create data grant for specific key(s) within an Amazon S3 bucket: `python3 create-data-grant.py --dataset-name example_file_dataset --bucket example-bucket --key data/example.parquet --grant-name example_file_grant --grant-end-date 2024-12-01 --target-account-id 123456789012`

**Note**: `grant-end-date` is an optional parameter. If not provided, the grant will not expire.