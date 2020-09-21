# Add a New Data Set to a Published Product

This sample creates and publishes a new data set by combining the [AWS Marketplace Catalog API](https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/welcome.html)'s [AddDataSets](https://docs.aws.amazon.com/es_es/data-exchange/latest/userguide/add-data-sets.html) change set, and the [AWS Data Exchange API](https://docs.aws.amazon.com/data-exchange/latest/apireference/welcome.html).

To run the sample, set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_REGION` and `ENTITY_ID` that identifies the product in which to publish a data set. You can enumerate [owned data products](https://console.aws.amazon.com/dataexchange/home?region=us-east-1#/owned/products) using the [enumerate-data-products sample](../enumerate-data-products) to get this ID.

```
$ ENTITY_ID=prod-... bundle exec ruby add-data-set.rb

Created a new Data Set 97267ce8224e3cae6286075d703f9e7f called "aws-dataexchange-api-samples test".
Adding Data Set arn:aws:dataexchange:us-east-1:147854383891:data-sets/97267ce8224e3cae6286075d703f9e7f to "prod-jrcarqhoeypfs@11".
Started change set a0z6l4wsl7jn5azcsjzy86zcl ................ done.
Change set a0z6l4wsl7jn5azcsjzy86zcl published.
Done.
```