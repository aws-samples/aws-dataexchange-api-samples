# Download all Entitled Assets

This example will automatically download all assets to which you are entitled to your local machine.

Downloading requires temporarily staging the files in S3. You can provide a bucket to stage the assets,
in which case the assets will remain in the bucket after the script executes. If no S3 bucket is provided, this script will create a temporary S3 bucket in your account, and will delete
this bucket and all exported assets after the script completes.

### Setup
First, install the requirements (preferably in a virtual environment).

```bash
$ pip install -r requirements.txt
```

You'll need an IAM user set up with the following policies attached:
* AmazonS3FullAccess
* AWSDataExchangeFullAccess

You'll need to set up some access keys for this User, and export them in your local environment:

```
$ export AWS_ACCESS_KEY_ID=<your-access-key-id>
$ export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
```
### Execution


Then execute the script, optionally providing an S3 bucket to stage your downloaded assets.

```bash
$ ./download-entitled-assets.py [--s3-bucket=<bucket-name>]
```

