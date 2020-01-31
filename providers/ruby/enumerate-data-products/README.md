# Enumerate Data Products

This sample uses the [AWS Marketplace Catalog API](https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/welcome.html) to enumerate data products, examines each product's data sets, parses each data set's Arn and fetches the data set using the [AWS Data Exchange API](https://docs.aws.amazon.com/data-exchange/latest/apireference/welcome.html).

To run the sample, set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

```
$ bundle exec ruby enumerate-data-products.rb 

Enumerating available data products ...
78aa8ff8-3eaf-4996-bcf8-67c7a1910528: AWS Data Exchange Heartbeat (Test product)
  Junto Heartbeat updated on 9 minutes and 55 seconds ago
    c4750301bac97b6bcf7fa3571a5761f3: Heartbeat
prod-jrcarqhoeypfs: Junto Heartbeat Test
  Junto Heartbeat updated on 1 hour and 58 minutes ago
    6c6becda6a8fb086b945bbf1dca4e1f5: Junto Heartbeat Test
prod-pi7x52bjwfa3m: AWS Data Exchange Subscription Verification (Test Product)
  Subscription Verification Test updated on 113 days and 2 hours ago
    97baee13810ff94ea80c95325c6f7bce: Subscription Verification Test
Done.
```
