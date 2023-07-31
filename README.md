![Data Exchange logo](logo.png)

# AWS Data Exchange Samples

[AWS Data Exchange](https://aws.amazon.com/data-exchange/) is a service that makes it easy for millions of AWS customers to securely find, subscribe to, and use third-party data in the cloud. This repository contains a collection of samples that interact with the AWS Data Exchange API.


## Subscriber Samples

Examples of interacting with the AWS Data Exchange API from the data subscriber side can be found in [/subscribers](subscribers).

### Java

* [all-entitled-datasets](subscribers/java/all-entitled-datasets): Lists all data sets one is subscribed to.

### Ruby

* [all-entitled-datasets](subscribers/ruby/all-entitled-datasets): Lists all data sets one is subscribed to.
* [most-expensive-neighborhoods-in-nyc](subscribers/ruby/most-expensive-neighborhoods-in-nyc): Most expensive neighborhoods in NYC by median price.

### JavaScript

* [all-entitled-datasets](subscribers/javascript/all-entitled-datasets): Lists all data sets one is subscribed to.
* [auto-export-to-s3](subscribers/javascript/auto-export-to-s3): Automatically exports newly published revisions to S3 using a CloudWatch Rule and Lambda Function.

### Go

* [all-entitled-datasets](subscribers/go/all-entitled-datasets): Lists all data sets one is subscribed to.

### Python

* [export-data-sets](subscribers/python/export-data-sets): Exports data sets specified into an Amazon S3 bucket.
* [download-entitled-assets](subscribers/python/download-entitled-assets): Download all assets to which you've subscribed.
* [pandas-describe-csv](subscribers/python/pandas-describe-csv): Download a CSV asset by Arn, import it into a Pandas data frame, and `describe()` the result.
* [auto-export-to-s3](subscribers/python/tf-auto-export-to-s3): Terraform based deployment to automatically export newly published revisions to S3 using a CloudWatch Rule and Lambda.
* [setup-redshift-data-shares](subscribers/python/setup-redshift-data-shares): Sets up AWS Data Exchange datashares for querying in Amazon Redshift.

### DotNet

* [all-entitled-datasets](subscribers/dotnet/all-entitled-datasets): Lists all data sets one is subscribed to.

### C++

* [all-entitled-datasets](subscribers/cpp/all-entitled-datasets): Lists all data sets one is subscribed to.

### PHP

* [all-entitled-datasets](subscribers/php/all-entitled-datasets): Lists all data sets one is subscribed to.

## Provider Samples

Examples of interacting with the AWS Data Exchange API from the data provider side can be found in [/providers](providers).

### Usage Metrics
* [Monitor Subscriber usage of AWS Data Exchange For Amazon S3 data sets](providers/usage-metrics): Deploy infrastructure to report and visualize subscriber usage on AWS Data Exchange for Amazon S3 data sets.

### Python
* [create-data-set-with-amazon-s3-access-points](providers/python/add-amazon-s3-data-access): Create a data set that will contain an Amazon S3 Access Point Asset.

### Ruby

* [create-data-set-with-finalized-revision](providers/ruby/create-data-set-with-finalized-revision): Create a data set with a finalized revision.
* [enumerate-data-products](providers/ruby/enumerate-data-products): Enumerate data products, examine each product's data sets, and fetch a data set.
* [add-data-set](providers/ruby/add-data-set): Create and publish a data set into an existing product.
* [add-revision-to-a-data-set](providers/ruby/add-revision-to-a-data-set): Add a new revision to a data set using data in S3.

## Other Samples

* [awslabs/aws-data-exchange-publisher-coordinator](https://github.com/awslabs/aws-data-exchange-publisher-coordinator): Coordinate the publishing steps for a dataset revision based on an S3 manifest file being uploaded to the specified S3 bucket.

## API References

* [AWS Data Exchange API](https://docs.aws.amazon.com/data-exchange/latest/apireference/welcome.html)
* [AWS Marketplace Catalog API](https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/welcome.html)

## License

This library is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file.
