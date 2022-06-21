# Setup Redshift Data Shares (Python)

This example will create databases in an Amazon Redshift cluster for data shares in a given AWS Data Exchange data set and revision. The script will create a single database for each asset in the revision, using the asset's `Name` as the database name.

*Note*: Database names are unique within the cluster, so there is potential for collisions if there are existing databases with the same name as one of the assets. Additionally, data shares can only be imported to a Redshift cluster once. So, this script can only be run successfully once without changing input.

For more documentation:
* https://docs.aws.amazon.com/data-exchange/latest/userguide/what-is.html
* https://aws.amazon.com/redshift/features/aws-data-exchange-for-amazon-redshift/

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

The following IAM policy is required for this AWS user.

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "redshift:GetClusterCredentials"
        "redshift-data:DescribeStatement",
        "redshift-data:ExecuteStatement"
      ],
      "Effect": "Allow",
      "Resource": "*"
    },
    {
      "Action": [
        "dataexchange:GetDataSet",
        "dataexchange:ListRevisionAssets"
      ],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

### Execution

```bash
$ python3 setup-redshift-data-shares.py \
  --data-set-id example-data-set-id-1234567890129 \
  --revision-id example-revision-id-2364567812345 \
  --redshift-cluster-id redshift-cluster-1 \
  --redshift-cluster-database dev \
  --redshift-cluster-database-user awsuser
```
