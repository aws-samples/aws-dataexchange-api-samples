# All Entitled Data Sets

This sample retrieves a list of all subscriber's entitled data sets.

To build the sample, install the [AWS SDK for C++](https://github.com/aws/aws-sdk-cpp#building-the-sdk) and use [CMake](https://cmake.org/).

```
cpp/all-entitled-datasets $ mkdir build
cpp/all-entitled-datasets $ cd build
cpp/all-entitled-datasets/build $ cmake ..
cpp/all-entitled-datasets/build $ make
```

To run the sample, set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN` and `AWS_REGION`.

```
$ ./all-entitled-datasets

prod-zg4u6tpyxud5i/7ae12084f47ea658ab62ee90edd513dd: NYC Property Sales 2014
  Over 80,000 property sales in New York City in 2014
prod-zg4u6tpyxud5i/05964b659bbcb607d43c0d5845838e7f: NYC Property Sales 2015
  Over 80,000 property sales in New York City in 2015
prod-zg4u6tpyxud5i/fc19d00c8780199e4fccd21f4834c905: NYC Property Sales 2018
  A table of 80,000+ New York City property sales occurring in 2018, organized by borough, including sale price and sale date. 
prod-zg4u6tpyxud5i/7d8f73e3c5acdde79fd2874dd98afdcd: NYC Property Sales 2016
  Over 80,000 property sales in New York City in 2016
prod-zg4u6tpyxud5i/50782dc315b94e46fdbd4a12cec6820e: NYC Property Sales 2017
  Records of over 80,000 property sales transactions. 
```
