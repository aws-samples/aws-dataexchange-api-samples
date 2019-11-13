# Most Expensive Neighborhoods in NYC

This sample uses [New York City Property Sales (2014-2018)](https://console.aws.amazon.com/dataexchange/home?region=us-east-1#/products/prodview-27ompcouk2o6i) provided by [Enigma](https://aws.amazon.com/marketplace/seller-profile?id=46c64acb-20c1-41fe-a495-a364f64d0083) with a free subscription. 

The code retrieves data sets between 2014 and 2018, enumerates data set revisions, exports latest CSV assets to S3, downloads the files to a local temporary location, imports the CSVs, calculates the median sale price in each neighborhood for all sales over $100,000, and displays the 10 most expensive neighborhoods.

To run the sample, set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`, subscribe to the product on AWS Data Exchange and replace the data set IDs and the S3 bucket name in the code.

```
$ bundle exec ruby most-expensive-neighborhoods-in-nyc.rb

NYC Property Sales 2017: Records of over 80,000 property sales transactions. 
96023397ee826914fefcef392b218c7b (Oct-17-2019) created 2019-10-28 16:01:46 UTC
e591f6f30d29c5d566c34a7436be701a 2017_NYC_Property_Sales__10172019 .csv
Exporting 2017_NYC_Property_Sales__10172019 .csv to S3 ......... done.
Loading 2017_NYC_Property_Sales__10172019 .csv ........... done.

NYC Property Sales 2018: A table of 80,000+ New York City property sales occurring in 2018, organized by borough, including sale price and sale date. 
b0457c8b3c201115daa0f6ca8f2c4140 (2018 Property Sales from 10172019) created 2019-10-28 16:01:47 UTC
01535eb11937b7f6ee825c512cb58582 2018_NYC_Property_Sales__10172019.csv
Exporting 2018_NYC_Property_Sales__10172019.csv to S3 ......... done.
Loading 2018_NYC_Property_Sales__10172019.csv ........... done.

10 Most Expensive NYC Neighborhoods:

EAST RIVER: $11,200,000
CIVIC CENTER: $4,737,500
LITTLE ITALY: $3,709,377
SOHO: $2,983,750
TRIBECA: $2,797,500
FLATIRON: $2,450,000
FASHION: $2,394,614
NAVY YARD: $2,050,000
ROSSVILLE-PORT MOBIL: $1,950,000
RED HOOK: $1,910,000
```
