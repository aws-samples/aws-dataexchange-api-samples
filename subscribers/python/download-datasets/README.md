# Download all Entitled Assets (Python)

This example accepts dataset_id(s),bucket,region, and exports all revisions corresponding to dataset-ids specified into an S3 bucket.

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

You can run following command to execute the script. Note that bucket,region, and dataset-ids are mandatory parameters and region specified must match region datasets and bucket are hosted in.

```bash
$ ./export-dataset.py --bucket 'bucket-name' --dataset-ids 'comma-separated-dataset-id(s)' --region 'region-name'```
