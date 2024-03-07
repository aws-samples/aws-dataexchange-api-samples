# Revoke a Revision and Delete all underlying assets (Python)

This example will show how to revoke a revision and delete all the underlying assets from a dataset that is part of a
published Data Product. This can be used to reduce the size of data stored in AWS Data Exchange managed S3 storage in
case of Data files delivery method

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


### Example Usage

Get usage help: `python3 revision_pruning.py --help`

Revoke a revision and delete underlying assets: `python3 revision_pruning.py --data-set-id '643b9fb3df63ce7bae948a1662fa9888' --revision-id 'c27cb47d1cc98a96f0c317fe268c634a' --region us-east-1`
