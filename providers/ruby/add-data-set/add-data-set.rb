# frozen_string_literal: true

require 'aws-sdk-dataexchange'
require 'aws-sdk-marketplacecatalog'

Aws.config.update(
  region: ENV['AWS_REGION'] || 'us-east-1',
  credentials: Aws::Credentials.new(
    ENV['AWS_ACCESS_KEY_ID'],
    ENV['AWS_SECRET_ACCESS_KEY'],
    ENV['AWS_SESSION_TOKEN']
  )
)

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

catalog_name = 'AWSMarketplace'
entity_id = ENV['ENTITY_ID'] || raise("missing ENV['ENTITY_ID']")

catalog = Aws::MarketplaceCatalog::Client.new

# describe the product entity in the AWS Marketplace catalog

described_entity = catalog.describe_entity(catalog: catalog_name, entity_id: entity_id)
described_entity_details = JSON.parse(described_entity.details)

# add the new data set to the product
puts "Adding Data Set #{data_set.arn} to \"#{described_entity.entity_identifier}\"."

start_change_set = catalog.start_change_set(
  catalog: 'AWSMarketplace',
  change_set_name: "Publishing data set to #{entity_id}.",
  change_set: [
    {
      change_type: 'AddDataSets',
      entity: {
        identifier: described_entity.entity_identifier,
        type: described_entity.entity_type
      },
      details: JSON.dump(
        'DataSets' => [
          { 'Arn' => data_set.arn }
        ]
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
