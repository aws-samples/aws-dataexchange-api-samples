import boto3
import time
import click
from botocore.exceptions import ClientError

def create_dataset(dataexchange, dataset_name):
    """
    Create a data files delivery method dataset
    """
    try:
        dataset_params = {
            'AssetType': 'S3_SNAPSHOT',
            'Description': f'Dataset for {dataset_name}',
            'Name': dataset_name,
            'Tags': {
                'Source': 'S3'
            }
        }

        response = dataexchange.create_data_set(**dataset_params)
        return response['Id']
    except ClientError as e:
        click.echo(f"An error occurred while creating the dataset: {e}", err=True)
        raise

def create_revision(dataexchange, dataset_id):
    """
    Create a new revision for the dataset
    """
    try:
        response = dataexchange.create_revision(DataSetId=dataset_id)
        return response['Id']
    except ClientError as e:
        click.echo(f"An error occurred while creating the revision: {e}", err=True)
        raise

def add_asset_to_revision(dataexchange, dataset_id, revision_id, bucket, prefixes, keys):
    """
    Add assets to the revision based on prefixes and keys, or entire bucket if none specified
    """
    try:
        s3 = boto3.client('s3')
        asset_sources = []
        
        if not prefixes and not keys:
            # If no prefixes or keys specified, include entire bucket
            response = s3.list_objects_v2(Bucket=bucket)
            for obj in response.get('Contents', []):
                asset_sources.append({
                    'Bucket': bucket,
                    'Key': obj['Key']
                })
        else:
            # Process prefixes
            for prefix in prefixes:
                if prefix:
                    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)
                    for obj in response.get('Contents', []):
                        asset_sources.append({
                            'Bucket': bucket,
                            'Key': obj['Key']
                        })
            
            # Add individual keys
            for key in keys:
                asset_sources.append({
                    'Bucket': bucket,
                    'Key': key
                })

        # Print assets being added
        for asset in asset_sources:
            print(f"Adding asset: s3://{asset['Bucket']}/{asset['Key']}")

        # Create a single job for all assets
        job_details = {
            'ImportAssetsFromS3': {
                'AssetSources': asset_sources,
                'DataSetId': dataset_id,
                'RevisionId': revision_id
            }
        }

        response = dataexchange.create_job(Type='IMPORT_ASSETS_FROM_S3', Details=job_details)
        job_id = response['Id']
        
        # Wait for job completion
        job_state = wait_for_job_completion(dataexchange, job_id)
        if job_state != 'COMPLETED':
            raise click.ClickException(f"Job failed with state: {job_state}")

        return "All assets added successfully"
    except ClientError as e:
        click.echo(f"An error occurred while adding the assets: {e}", err=True)
        raise

def wait_for_job_completion(dataexchange, job_id):
    """
    Wait for a job to complete
    """
    dataexchange.start_job(JobId=job_id)

    while True:
        job_response = dataexchange.get_job(JobId=job_id)
        job_state = job_response['State']

        if job_state in ['COMPLETED', 'ERROR', 'CANCELLED']:
            if job_state == 'ERROR':
                error_details = job_response.get('Errors', [])
                click.echo(f"Job failed with errors: {error_details}")
            return job_state

        click.echo(f"Job {job_id} is in {job_state} state. Waiting...")
        time.sleep(5)

def finalize_revision(dataexchange, dataset_id, revision_id):
    """
    Finalize the revision
    """
    try:
        dataexchange.update_revision(DataSetId=dataset_id, RevisionId=revision_id, Finalized=True)
    except ClientError as e:
        click.echo(f"An error occurred while finalizing the revision: {e}", err=True)
        raise

@click.command()
@click.option('--bucket', required=True, help='S3 bucket name or full S3 URI')
@click.option('--prefix', multiple=True, help='S3 prefix to include (can be used multiple times)')
@click.option('--key', multiple=True, help='S3 object key to include (can be used multiple times)')
@click.option('--dataset-name', required=True, help='Name of the dataset')
@click.option('--region', default='us-east-1', help='AWS region')
def main(bucket, prefix, key, dataset_name, region):
    """
    Create a dataset and import assets from S3.
    """
    # Parse bucket and initial prefix from the provided bucket parameter
    if bucket.startswith('s3://'):
        parts = bucket.replace('s3://', '').split('/', 1)
        bucket_name = parts[0]
        initial_prefix = parts[1] if len(parts) > 1 else ''
    else:
        bucket_name = bucket
        initial_prefix = ''

    # Combine initial_prefix with provided prefixes
    all_prefixes = [initial_prefix] if initial_prefix else []
    all_prefixes.extend(prefix)

    dataexchange = boto3.client('dataexchange', region_name=region)
    
    try:
        # Create dataset
        dataset_id = create_dataset(dataexchange, dataset_name)
        click.echo(f"Dataset created successfully. Dataset ID: {dataset_id}")

        # Create revision
        revision_id = create_revision(dataexchange, dataset_id)
        click.echo(f"Revision created successfully. Revision ID: {revision_id}")

        # Add assets to revision
        result = add_asset_to_revision(dataexchange, dataset_id, revision_id, bucket_name, all_prefixes, key)
        click.echo(result)

        # Finalize revision
        finalize_revision(dataexchange, dataset_id, revision_id)
        click.echo("Revision finalized successfully.")

    except Exception as e:
        click.echo(f"An error occurred: {str(e)}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    main()