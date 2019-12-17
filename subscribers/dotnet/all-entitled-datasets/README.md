# All Entitled Data Sets (DotNet)

This sample retrieves a list of all subscriber's entitled data sets, in .NET.

To run the sample, install .NET, set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

```
$ dotnet run Program.cs

prod-zg4u6tpyxud5i/7d8f73e3c5acdde79fd2874dd98afdcd: NYC Property Sales 2016
  Over 80,000 property sales in New York City in 2016
prod-zg4u6tpyxud5i/7ae12084f47ea658ab62ee90edd513dd: NYC Property Sales 2014
  Over 80,000 property sales in New York City in 2014
prod-zg4u6tpyxud5i/05964b659bbcb607d43c0d5845838e7f: NYC Property Sales 2015
  Over 80,000 property sales in New York City in 2015
prod-zg4u6tpyxud5i/fc19d00c8780199e4fccd21f4834c905: NYC Property Sales 2018
  A table of 80,000+ New York City property sales occurring in 2018, organized by borough, including sale price and sale date. 
prod-zg4u6tpyxud5i/50782dc315b94e46fdbd4a12cec6820e: NYC Property Sales 2017
  Records of over 80,000 property sales transactions. 
```

### Implementation Details

This project was built on a Mac.

Download and install .NET SDK using the [install script](https://docs.microsoft.com/en-us/dotnet/core/tools/dotnet-install-script).

```
$ wget https://dot.net/v1/dotnet-install.sh
$ chmod 700 dotnet-install.sh
$ ./dotnet-install.sh --install-dir ~/Library/DotNet

dotnet-install: Downloading link: https://dotnetcli.azureedge.net/dotnet/Sdk/3.1.100/dotnet-sdk-3.1.100-osx-x64.tar.gz
dotnet-install: Extracting zip from https://dotnetcli.azureedge.net/dotnet/Sdk/3.1.100/dotnet-sdk-3.1.100-osx-x64.tar.gz
dotnet-install: Installation finished successfully.
```

Add .NET to `PATH`, edit `~/.bash_profile`.

```
# Add .NET to PATH
export PATH="$PATH:$HOME/Library/DotNet"
```

Create a new console app.

```
$ dotnet new console --name AwsDataExchangeSample
$ cd AwsDataExchangeSample
```

Add the AWS Data Exchange SDK from [Nuget](https://www.nuget.org/packages/AWSSDK.DataExchange/).

```
$ dotnet add package AWSSDK.DataExchange --version 3.3.100.15
```

Modify the code, run the app.

```
$ dotnet run Program.cs
```
