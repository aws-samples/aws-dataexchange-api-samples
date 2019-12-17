# All Entitled Data Sets (Java)

This sample retrieves a list of all subscriber's entitled data sets, in Java.

To run the sample, install Maven, set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.

```
$ mvn exec:java -Dexec.mainClass="com.amazon.aws.dataexchange.App"

prod-zg4u6tpyxud5i/7ae12084f47ea658ab62ee90edd513dd: NYC Property Sales 2014
  Over 80,000 property sales in New York City in 2014
prod-zg4u6tpyxud5i/fc19d00c8780199e4fccd21f4834c905: NYC Property Sales 2018
  A table of 80,000+ New York City property sales occurring in 2018, organized by borough, including sale price and sale date.
prod-zg4u6tpyxud5i/05964b659bbcb607d43c0d5845838e7f: NYC Property Sales 2015
  Over 80,000 property sales in New York City in 2015
prod-zg4u6tpyxud5i/7d8f73e3c5acdde79fd2874dd98afdcd: NYC Property Sales 2016
  Over 80,000 property sales in New York City in 2016
prod-zg4u6tpyxud5i/50782dc315b94e46fdbd4a12cec6820e: NYC Property Sales 2017
  Records of over 80,000 property sales transactions.
```

### Implementation Details

The project was generated with [Maven](https://maven.apache.org/guides/getting-started/maven-in-five-minutes.html).

```
$ mvn -B archetype:generate \
    -DarchetypeGroupId=org.apache.maven.archetypes \
    -DgroupId=com.amazon.aws.dataexchange \
    -DartifactId=all-entitled-datasets
```

A dependency on AWS SDK was added to [pom.xml](pom.xml).

```xml
<dependencyManagement>
 <dependencies>
  <dependency>
    <groupId>com.amazonaws</groupId>
    <artifactId>aws-java-sdk-bom</artifactId>
    <version>1.11.693</version>
    <type>pom</type>
    <scope>import</scope>
  </dependency>
 </dependencies>
</dependencyManagement>
```

Added AWS Data Exchange SDK to [pom.xml](pom.xml).

```
<dependency>
 <groupId>com.amazonaws</groupId>
 <artifactId>aws-java-sdk-dataexchange</artifactId>
</dependency>
```

Upgraded compiler source and target to 1.8 in [pom.xml](pom.xml).

```
<properties>
 <maven.compiler.source>1.8</maven.compiler.source>
 <maven.compiler.target>1.8</maven.compiler.target>
</properties>
```

Compile and run.

```
$ mvn exec:java -Dexec.mainClass="com.amazon.aws.dataexchange.App"
```