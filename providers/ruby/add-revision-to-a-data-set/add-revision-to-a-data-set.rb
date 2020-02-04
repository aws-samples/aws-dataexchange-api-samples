# frozen_string_literal: true

require 'aws-sdk-dataexchange'
require 'aws-sdk-marketplacecatalog'
require 'time_ago_in_words'

Aws.config.update(
  region: ENV['AWS_REGION'] || 'us-east-1',
  credentials: Aws::Credentials.new(
    ENV['AWS_ACCESS_KEY_ID'],
    ENV['AWS_SECRET_ACCESS_KEY'],
    ENV['AWS_SESSION_TOKEN']
  )
)

catalog_name = 'AWSMarketplace'
entity_id = ENV['ENTITY_ID'] || raise("missing ENV['ENTITY_ID']")

catalog = Aws::MarketplaceCatalog::Client.new

# describe a specific entity

described_entity = catalog.describe_entity(catalog: catalog_name, entity_id: entity_id)
described_entity_details = JSON.parse(described_entity.details)

# first data set
data_set = described_entity_details['DataSets'].first
raise 'Missing Data Set' unless data_set

data_set_name = data_set['Name']
data_set_arn = data_set['DataSetArn']
data_set_id = Aws::ARNParser.parse(data_set_arn).resource.split('/').last
data_set_last_revision_added_at = DateTime.parse(data_set['LastRevisionAddedDate'])
puts "#{data_set_id}: #{data_set_name} updated #{data_set_last_revision_added_at.to_time.ago_in_words}"

# create a revision and finalize it
dx = Aws::DataExchange::Client.new

revision = dx.create_revision(
  data_set_id: data_set_id,
  comment: 'New revision in the Data Set.'
)

puts "Created revision #{revision.id}"

# import data from S3

s3_bucket_name = 'aws-samples-create-data-set-with-finalized-revision'
s3_data_key = 'data.txt'

STDOUT.write "Importing #{s3_bucket_name}/#{s3_data_key} from S3 ..."

export_job = dx.create_job(
  type: 'IMPORT_ASSETS_FROM_S3',
  details: {
    import_assets_from_s3: {
      asset_sources: [
        bucket: s3_bucket_name,
        key: s3_data_key
      ],
      data_set_id: data_set_id,
      revision_id: revision.id
    }
  }
)

dx.start_job(job_id: export_job.id)

loop do
  sleep 1
  job_in_progress = dx.get_job(job_id: export_job.id)
  STDOUT.write('.')
  state = job_in_progress.state
  next if state == 'IN_PROGRESS' || state == 'WAITING'
  break if state == 'COMPLETED'
  raise job_in_progress.errors.join(&:to_s) if job_in_progress.state == 'ERROR'

  raise job_in_progress.state
end

puts ' done.'

# finalize the revision

dx.update_revision(
  data_set_id: data_set_id,
  revision_id: revision.id,
  finalized: true
)

# get the revision

finalized_revision = dx.get_revision(
  data_set_id: data_set_id,
  revision_id: revision.id
)

puts "The revision #{revision.id} has #{finalized_revision.finalized ? 'been finalized' : 'not been finalized'}."

# add a finalized revision to the data set

start_change_set = catalog.start_change_set(
  catalog: 'AWSMarketplace',
  change_set_name: "Adding revision to #{data_set_name}.",
  change_set: [
    {
      change_type: 'AddRevisions',
      entity: {
        identifier: described_entity.entity_identifier,
        type: described_entity.entity_type
      },
      details: JSON.dump(
        'DataSetArn' => data_set_arn,
        'RevisionArns' => [finalized_revision.arn]
      )
    }
  ]
)

STDOUT.write "Started change set #{start_change_set.change_set_id} ..."

chage_set_id = start_change_set.change_set_id
loop do
  sleep 1

  describe_change_set = catalog.describe_change_set(
    catalog: 'AWSMarketplace',
    change_set_id: chage_set_id
  )

  describe_change_set_status = describe_change_set.status
  break if describe_change_set_status == 'SUCCEEDED'

  if describe_change_set_status == 'FAILED'
    raise "#{describe_change_set.failure_description}\n#{describe_change_set
      .change_set.first.error_detail_list
      .map(&:error_message).join}"
  end

  STDOUT.write('.')
end
puts ' done.'

puts "Change set #{chage_set_id} published."
puts 'Done.'
