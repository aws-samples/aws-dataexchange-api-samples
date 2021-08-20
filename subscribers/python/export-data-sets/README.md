# Export entitled data set assets (Python)

This example accepts dataset_id(s),bucket,region, and exports all revisions within the specified data-set-ids into an S3 bucket.

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
* AWSDataExchangeSubscriberFullAccess

### Execution

You can run following command to execute the script. Note that bucket,region, and data-set-ids are mandatory parameters and region specified must match region data-sets and bucket are hosted in.

```bash
$ ./export-data-sets.py --bucket 'bucket-name' --data-set-ids 'comma-separated-data-set-id(s)' --region 'region-name'```
