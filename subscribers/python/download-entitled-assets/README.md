# Download all Entitled Assets (Python)

This example will automatically download all assets to which you are entitled to your local machine, in Python.

Downloading requires temporarily staging the files in S3. You can provide a bucket to stage the assets, in which case the assets will remain in the bucket after the script executes. If no S3 bucket is provided, this script will create a temporary S3 bucket in your account, and will delete
this bucket and all exported assets after the script completes.

### Setup

Install the requirements, preferably in a virtual environment.

```bash
$ pip install -r requirements.txt
```

Set AWS access key and secret.

```
$ export AWS_ACCESS_KEY_ID=<your-access-key-id>
$ export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
```

The following policies are required for this AWS user.

* AmazonS3FullAccess
* AWSDataExchangeFullAccess

### Execution

Execute the script, optionally providing an S3 bucket to stage your downloaded assets.

```bash
$ ./download-entitled-assets.py [--s3-bucket=<bucket-name>]
```
