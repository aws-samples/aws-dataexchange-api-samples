#!/usr/bin/env python
import boto3
import re
import click
import time

ASSET_TYPE = 'REDSHIFT_DATA_SHARE'

# Uses the Asset's Name and Asset's Data Share Arn to get the required parameters for the Redshift
# create database from datashare query.
# Docs: https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_DATABASE.html
def get_create_database_sql_from_asset(asset):
  # Using the Asset's Name as the name of the to-be-created database in the consumer cluster.
  asset_name = asset['Name']
  data_share_arn = asset['AssetDetails']['RedshiftDataShareAsset']['Arn']
  matches = re.search(r'arn:aws:redshift:.+:(\d+):datashare:(.+)/(.+)', data_share_arn)

  # Account which owns the Data Share.
  source_account = matches.group(1)

  # Cluster namespace from which the data is shared.
  source_namespace = matches.group(2)

  # Name of the source Data Share.
  data_share_name = matches.group(3)

  return f'CREATE DATABASE {asset_name} FROM DATASHARE {data_share_name} OF ACCOUNT \'{source_account}\' NAMESPACE \'{source_namespace}\''


def wait_for_statement_to_complete(redshift_data, statement_id):
  while True:
    statement = redshift_data.describe_statement(Id=statement_id)
    status = statement['Status']

    if status in ['ABORTED', 'FAILED']:
      error = statement['Error']
      click.echo(f'Error encountered while executing statement: {error}')
      raise Exception(f'Redshift query failed with status {status}!')
    if status in ['FINISHED']:
      return
    
    # Else, statement is still running.
    time.sleep(2)

def create_databases_from_assets(redshift_data, assets, redshift_cluster_id, redshift_cluster_database, redshift_cluster_database_user):
  for asset in assets:
    sql = get_create_database_sql_from_asset(asset)
    statement = redshift_data.execute_statement(
      ClusterIdentifier=redshift_cluster_id,
      Database=redshift_cluster_database,
      DbUser=redshift_cluster_database_user,
      Sql=sql
    )

    id = statement['Id']

    wait_for_statement_to_complete(redshift_data, id)
    click.echo(f'SQL statement executed successfully: "{sql}"')


def get_assets_from_data_set_and_revision(dataexchange, data_set_id, revision_id):
  data_set = dataexchange.get_data_set(DataSetId=data_set_id)
  data_set_asset_type = data_set['AssetType']

  if data_set_asset_type != ASSET_TYPE:
    raise Exception(f'AssetType must be of type {ASSET_TYPE} but was {data_set_asset_type}!')

  return dataexchange.list_revision_assets(DataSetId=data_set_id, RevisionId=revision_id)['Assets']
  

@click.command()
@click.option('--data-set-id', required=True, help='AWS Data Exchange Data set which contains Redshift data shares to set up. Data set must have AssetType REDSHIFT_DATA_SHARE.')
@click.option('--revision-id', required=True, help='AWS Data Exchange Revision which contains Redshift data shares to set up.')
@click.option('--redshift-cluster-id', required=True, help='Amazon Redshift cluster from which the Redshift data shares will be queried.')
@click.option('--redshift-cluster-database', required=True, help='Amazon Redshift database from which the Redshift data shares will be queried.')
@click.option('--redshift-cluster-database-user', required=True, help='Amazon Redshift database user which can connect to the Redshift cluster and database.')
@click.option('--region', default='us-east-1', help='AWS Region of the Data set.')
def main(data_set_id, revision_id, redshift_cluster_id, redshift_cluster_database, redshift_cluster_database_user, region):
    dataexchange = boto3.client('dataexchange', region_name=region)
    redshift_data = boto3.client('redshift-data', region_name=region)

    assets = get_assets_from_data_set_and_revision(dataexchange, data_set_id, revision_id)
    create_databases_from_assets(redshift_data, assets, redshift_cluster_id, redshift_cluster_database, redshift_cluster_database_user)

if __name__ == '__main__':
    main()
