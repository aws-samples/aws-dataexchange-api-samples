# Add Amazon S3 Files Dataset (Python)

This script automates the process of creating and populating AWS Data Exchange datasets using content from Amazon S3 buckets. It creates a new dataset, generates a revision, and imports specified assets (either entire buckets, prefixes, or individual objects) into the revision. The script provides a simple command-line interface, allowing users to easily specify the source S3 bucket, dataset name, and desired assets, streamlining the process of preparing data for distribution through AWS Data Exchange.

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

Get usage help: `python3 add-amazon-s3-files.py --help`

Create dataset and import all files from an Amazon S3 Bucket: `python3 add-amazon-s3-files.py --dataset-name example_dataset --bucket example_bucket`

Create dataset and import files from specific prefix(es) within an Amazon S3 Bucket:`python3 add-amazon-s3-files.py --dataset-name example_prefix_dataset --bucket example_bucket --prefix data/`

Create dataset and import specific file(s) from an Amazon S3 bucket: `python3 add-amazon-s3-files.py --dataset-name example_file_dataset --bucket example_bucket --key data/titanic.parquet`