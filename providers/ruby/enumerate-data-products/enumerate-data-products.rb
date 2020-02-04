# frozen_string_literal: true

require 'aws-sdk-marketplacecatalog'
require 'aws-sdk-dataexchange'
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

catalog = Aws::MarketplaceCatalog::Client.new
dx = Aws::DataExchange::Client.new

# data products, what you see in https://console.aws.amazon.com/dataexchange/home?region=us-east-1#/owned/products

puts 'Enumerating available data products ...'

entities = catalog.list_entities(
  catalog: catalog_name,
  entity_type: 'DataProduct'
).entity_summary_list

entities.each do |entity|
  puts "#{entity.entity_id}: #{entity.name}"

  # entity details
  described_entity = catalog.describe_entity(catalog: catalog_name, entity_id: entity.entity_id)
  described_entity_details = JSON.parse(described_entity.details)

  described_entity_details['DataSets'].each do |data_set|
    puts "  #{data_set['Name']} updated on #{Time.parse(data_set['LastRevisionAddedDate']).ago_in_words}"
    data_set_arn = Aws::ARNParser.parse(data_set['DataSetArn'])
    # TODO: be region-aware, currently dx client region is set globally
    data_set_id = data_set_arn.resource.split('/').last
    data_set = dx.get_data_set(data_set_id: data_set_id)
    puts "    #{data_set.id}: #{data_set.name}"
  end
end

puts 'Done.'
