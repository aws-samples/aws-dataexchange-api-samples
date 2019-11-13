require 'aws-sdk-dataexchange'

Aws.config.update({
  region: 'us-east-1',
  credentials: Aws::Credentials.new(
    ENV['AWS_ACCESS_KEY_ID'], 
    ENV['AWS_SECRET_ACCESS_KEY']
  )
})

dx = Aws::DataExchange::Client.new

dx.list_data_sets(origin: 'ENTITLED').each do |response|
  response.data_sets.each do |data_set|
    puts "#{data_set.origin_details.product_id}/#{data_set.id}: #{data_set.name}\n  #{data_set.description}"
  end
end
