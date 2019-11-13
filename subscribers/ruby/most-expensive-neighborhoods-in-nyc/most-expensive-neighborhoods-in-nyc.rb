require 'aws-sdk-dataexchange'
require 'aws-sdk-s3'
require 'smarter_csv'
require 'simple_statistics'
require 'money'
require 'i18n'
require 'monetize'

I18n.enforce_available_locales = false
Money.locale_backend = :i18n

Aws.config.update({
  region: 'us-east-1',
  credentials: Aws::Credentials.new(
    ENV['AWS_ACCESS_KEY_ID'], 
    ENV['AWS_SECRET_ACCESS_KEY'],
    ENV['AWS_SESSION_TOKEN']
  )
})

# data sets provided by Enigma
# https://console.aws.amazon.com/dataexchange/home?region=us-east-1#/products/prodview-27ompcouk2o6i

data_sets = {
  2014 => '7ae12084f47ea658ab62ee90edd513dd',
  2015 => '05964b659bbcb607d43c0d5845838e7f',
  2016 => '7d8f73e3c5acdde79fd2874dd98afdcd',
  2017 => '50782dc315b94e46fdbd4a12cec6820e',
  2018 => 'fc19d00c8780199e4fccd21f4834c905'
}

s3_bucket_name = 'aws-dataexchange-hello-world'

dx = Aws::DataExchange::Client.new

neighborhood_sale_prices = {}

data_sets.each_pair do |year, data_set_id|
  data_set = dx.get_data_set(
    data_set_id: data_set_id
  )

  puts "#{data_set.name}: #{data_set.description}"

  latest_asset = nil

  # fetch revisions for this data set

  revisions = dx.list_data_set_revisions(
    data_set_id: data_set.id
  ).map(&:revisions).flatten

  revisions.each do |revision|
    puts "#{revision.id} (#{revision.comment}) created #{revision.created_at}"

    # fetch assets for this revision

    assets = dx.list_revision_assets(
      data_set_id: data_set.id, 
      revision_id: revision.id
    ).map(&:assets).flatten

    # the first result is the latest asset

    assets.each do |asset|
      puts "#{asset.id} #{asset.name}"
      latest_asset ||= asset
    end
  end

  return unless latest_asset

  # export data to S3

  STDOUT.write "Exporting #{latest_asset.name} to S3 ..."

  export_job = dx.create_job(
    type: 'EXPORT_ASSETS_TO_S3',
    details: {
      export_assets_to_s3: {
        asset_destinations: [
          asset_id: latest_asset.id,
          bucket: s3_bucket_name,
          key: "data/#{latest_asset.name}" 
        ],
        data_set_id: latest_asset.data_set_id,
        revision_id: latest_asset.revision_id
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

  STDOUT.write "Loading #{latest_asset.name} ..."

  s3 = Aws::S3::Client.new

  # load data from S3

  Tempfile.create do |f|
    s3.get_object({
      bucket: s3_bucket_name,
      key: "data/#{latest_asset.name}",
    }, target: f)


    rows = 0
    SmarterCSV.process(f, row_sep: :auto, col_sep: ',', file_encoding: Encoding::UTF_8) do |coll|
      coll.each do |row|
        rows += 1
        STDOUT.write('.') if rows % 10000 == 0
        sale_price = Monetize.parse(row[:sale_price]).to_f
        next unless sale_price > 100_000
        neighborhood_sale_prices[row[:neighborhood]] ||= []
        neighborhood_sale_prices[row[:neighborhood]] << sale_price
      end
    end
    
    puts " done."
  end
end

puts "10 Most Expensive NYC Neighborhoods:"

neighborhood_median_sale_prices = Hash[neighborhood_sale_prices.map do |neighborhood, prices|
  [neighborhood, prices.median]
end]

neighborhood_median_sale_prices
  .sort_by { |neighborhood, median_price| -median_price }
  .take(10)
  .each do |neighborhood_median_price_pair|
    dollars = Money.new(neighborhood_median_price_pair[1] * 100, 'USD')
      .format(thousands_separator: ',', drop_trailing_zeros: true)
    puts "#{neighborhood_median_price_pair[0]}: #{dollars}"
end
