# Import CSV asset to pandas

This example imports a CSV asset from Data Exchange into a pandas Data Frame object and `describe()` the result.

### Setup

Install the requirements, preferably in a virtual environment.

```bash
$ pip install -r requirements.txt
```

Set AWS access key and secret.

```
$ export AWS_ACCESS_KEY_ID=<your-access-key-id>
$ export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
```

The following policies are required for this AWS user.

* AmazonS3FullAccess
* AWSDataExchangeFullAccess

Subscribe to a product on [AWS Data Exchange](https://aws.amazon.com/data-exchange), and note the Arn for the CSV asset you would like to test against.

### Execution

This script creates a temporary S3 Bucket in your account to export the assets, and a temporary directory to stage the file locally.

```bash
$ ./pandas-describe-csv.py <asset-arn>
```

Sample output using [Rearc Tax Revenue (% of GDP) from World Bank Open Data](https://console.aws.amazon.com/dataexchange/home?region=us-east-1#/products/prodview-yfrvk7kf66aiy).

```
$ ./pandas-describe-csv.py arn:aws:dataexchange:us-east-1::data-sets/5c8f9ac07883d81d8f25e2b9dd28efce/revisions/40c042c6b24286f1acf36b49e5748b36/assets/770435e0fd1aa970450b1b7c2e6a39f9 

            1972       1973       1974       1975       1976       1977       1978  ...        2011        2012        2013        2014        2015        2016        2017
count  41.000000  50.000000  53.000000  50.000000  51.000000  52.000000  53.000000  ...  168.000000  155.000000  157.000000  156.000000  153.000000  146.000000  130.000000
mean   17.595742  16.770584  16.003546  16.315434  16.817749  17.245061  17.879250  ...   16.783580   17.166849   16.784489   17.162941   17.002521   17.053722   17.775034
std     8.923219   8.116698   6.033629   5.317894   5.675549   6.132574   8.739127  ...    6.262297    6.412270    6.428430    6.374452    6.236064    6.240035    5.857815
min     7.610619   7.091172   5.417791   7.521319   7.562059   4.615802   7.597964  ...    0.321414    0.363786    0.370451    0.355723    0.057734    0.043495    0.066984
25%    12.445223  11.536664  11.810243  12.343971  12.725799  12.954639  12.651562  ...   13.132882   13.438136   13.008075   12.684953   12.723964   13.013613   13.646999
50%    14.872564  14.804852  15.021760  16.429262  16.552555  16.694574  16.511790  ...   16.155646   16.061603   15.668958   16.084710   16.124201   15.847322   17.322809
75%    21.171189  18.763604  18.397341  20.159210  19.795274  20.690760  21.466918  ...   20.248498   20.978581   21.601282   22.033340   21.646466   21.839676   22.202239
max    58.950073  56.281979  32.677682  30.394147  33.768480  35.126715  65.423553  ...   37.562987   36.937839   36.376968   36.500291   33.921623   37.752914   33.323447

[8 rows x 46 columns]
```
