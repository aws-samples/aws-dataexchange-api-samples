require 'aws-sdk-dataexchange'

Aws.config.update({
  region: ENV['AWS_REGION'] || 'us-east-1',
  credentials: Aws::Credentials.new(
    ENV['AWS_ACCESS_KEY_ID'], 
    ENV['AWS_SECRET_ACCESS_KEY']
  )
})

s3_bucket_name = 'bucket'
s3_data_key = 'file.txt'

dx = Aws::DataExchange::Client.new

# create a Data Set

data_set = dx.create_data_set(
  asset_type: 'S3_SNAPSHOT',
  name: 'aws-dataexchange-api-samples test',
  description: 'Test Data Set for aws-dataexchange-api-samples.',
  tags: {
    category: 'demo',
    language: 'ruby'
  }
)

puts "Created a new Data Set #{data_set.id} called \"#{data_set.name}\"."

# create a revision in the Data Set

revision = dx.create_revision(
  data_set_id: data_set.id,
  comment: 'First revision in the Data Set.'
)

puts "Created revision #{revision.id}"

# import data from S3

STDOUT.write "Importing #{s3_bucket_name}/#{s3_data_key} from S3 ..."

export_job = dx.create_job(
  type: 'IMPORT_ASSETS_FROM_S3',
  details: {
    import_assets_from_s3: {
      asset_sources: [
        bucket: s3_bucket_name,
        key: s3_data_key
      ],
      data_set_id: data_set.id,
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
  data_set_id: data_set.id,
  revision_id: revision.id,
  finalized: true
)

# get the revision

finalized_revision = dx.get_revision(
  data_set_id: data_set.id,
  revision_id: revision.id
)

puts "The revision #{revision.id} has #{finalized_revision.finalized ? 'been finalized' : 'not been finalized'}."

# cleanup

dx.delete_data_set(
  data_set_id: data_set.id
)
