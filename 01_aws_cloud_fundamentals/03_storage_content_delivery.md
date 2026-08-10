# Storage & Content Delivery
## 1. Storage in the Cloud
Storage & Database Services:
* Amazon Simple Storage Service (Amazon S3)
* Amazon Simple Storage Service (Amazon S3) Glacier
* DynamoDB
* Relational Database Service (RDS)
* Redshift
* ElastiCache
* Neptune
* Amazon DocumentDB

Benefits:
* Durability: guarantees that you will not lose the data that you upload to the cloud
* Availability: addresses how quickly you can access your data
* Scalability: allows applications running in your environment to always meet demand seamlessly
    - Vertical scaling (scaling up): modifies a single server to meet demand, such as adding more memory or capacity.
    - Horizontal scaling (scaling out): adds or removes servers to meet demand, such as increasing from two servers to six.
    - Diagonal scaling: combines horizontal and vertical scaling to offer maximum flexibility.

## 2. S3 & Glacier

* S3 Standard
* S3 Glacier
* S3 Glacier Deep Archive
* S3 Intelligent-Tiering
* S3 Standard Infrequent Access
* S3 One Zone-Infrequent Access

## 3. DynamoDB
DynamoDB is a NoSQL document database service that is fully managed. Unlike traditional databases, NoSQL databases, are schema-less. Schema-less simply means that the database doesn't contain a fixed (or rigid) data structure.

* DynamoDB can handle more than 10 trillion requests per day.
* DynamoDB is serverless as there are no servers to provision, patch, or manage.
* DynamoDB supports key-value and document data models.
* DynamoDB synchronously replicates data across three AZs in an AWS Region.
* DynamoDB supports GET/PUT operations using a primary key.

## 4. Relational Database Service (RDS)
RDS (or Relational Database Service) is a service that aids in the administration and management of databases. RDS assists with database administrative tasks that include upgrades, patching, installs, backups, monitoring, performance checks, security, etc.

Database Engine Support:
* Oracle
* PostgreSQL
* MySQL
* MariaDB
* SQL Server
* Aurora
* IBM DB2

Features:
* failover
* backups
* restore
* encryption
* security
* monitoring
* data replication
* scalability

## 5. Redshift
**Redshift** is a cloud data warehousing service to help companies manage big data.

Redshift allows you to run fast queries against your data using SQL, ETL, and BI tools. Redshift stores data in a column format to aid in fast querying.

* Redshift delivers great performance by using machine learning.
* Redshift Spectrum is a feature that enables you to run queries against data in Amazon S3.
* Redshift encrypts and keeps your data secure in transit and at rest.
* Redshift clusters can be isolated using Amazon Virtual Private Cloud (VPC).

## 6. Content Delivery in the Cloud
A Content Delivery Network (or CDN) speeds up delivery of your static and dynamic web content by caching content in an Edge Location close to your user base.

The benefits of a CDN include:
* low latency
* decreased server load
* better user experience

### 6.1 CloudFront
CloudFront is used as a global content delivery network (CDN). CloudFront speeds up the delivery of your content through Amazon's worldwide network of mini-data centers called Edge Locations.

CloudFront works with other AWS services, as shown below, as an origin source for your application:
* Amazon S3
* Elastic Load Balancing
* Amazon EC2
* Lambda@Edge
* AWS Shield

Tips:
* Amazon continously adds new Edge Locations.
* CloudFront ensures that end-user requests are served from the closest edge location.
* CloudFront works with non-AWS origin sources.
* You can use GeoIP blocking to serve content (or not serve content) to specific countries.
* Cache control headers determine how frequently CloudFront needs to check the origin for an updated version of your file.
* The maximum size of a single file that can be delivered through Amazon CloudFront is 20 GB.
