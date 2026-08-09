# Cloud Computing

Cloud computing is the delivery of IT resources over the Internet. The cloud is like a virtual data center accessible via the Internet that allows you to manage:
* Storage services like databases.
* Servers, compute power, networking.
* Analytics, artificial intelligence, augmented reality.
* Security services for data and applications.

## 1. Characteristics of Cloud Computing
* **Pay as you go** - You pay only for what you use and only when your code runs.
* **Autoscaling** - The number of active servers can grow or shrink based on demand.
* **Serverless** - Allows you to write and deploy code without having to worry about the underlying infrastructure, like a server.

## 2. Types of Cloud Computing
* **Infrastructure-as-a-Service (IaaS)**
The provider supplies virtual server instances, storage, and mechanisms for you to manage servers.
* **Platform-as-a-Service (PaaS)**
A platform of development tools hosted on a provider's infrastructure.
* **Software-as-a-Service (SaaS)**
A software application that runs over the Internet and is managed by the service provider.

## 3. Cloud Deployment Models
* **Public Cloud**: A public cloud makes resources available over the Internet to the general public.
* **Private Cloud**: A private cloud is a proprietary network that supplies services to a limited number of people.
* **Hybrid Cloud**: A hybrid model contains a combination of both a public and a private cloud. The hybrid model is a growing trend in the industry for those organizations that have been slow to adopt the cloud due to being in a heavily regulated industry. The hybrid model gives organizations the flexibility to slowly migrate to the cloud.

## 4. Cloud Benefits
* Stop guessing about capacity.
* Avoid huge capital investments up front.
* Pay for only what you use.
* Scale globally in minutes.
* Deliver faster.

## 5. AWS Services
Compute services:
* Amazon EC2
* Amazon Elastic Container Service
* AWS Lambda

Storage:
* Amazon EBS (Amazon Elastic Block Store)
* Amazon EFS (Amazon Elastic File Service)

Analytics:
* Quick Sight
* Athena
* Redshift

Application integration:
* Simple Queue Service (SQS)
* Simple Notification Service (SNS)

Cost management:
* AWS Budgets

Database management services:
* MySQL
* Oracle
* SQLServer
* DynamoDB
* MongoDB

Developer tools:
* Cloud 9
* Code Pipeline

Security services:
* Key Management Service (KMS)
* Shield
* Identity and Access Management (IAM)

Additional Services:
* Blockchain
* Machine Learning
* Computer Vision
* Internet of Things (IoT)
* AR/VR

## 6. Global Infrastructure
* **Region**: A region is considered a geographic location or an area on a map.
* **Availability Zone (AZ)**: An availability zone is an isolated location within a geographic region and is a physical data center within a specific region.
* **Edge Location**: An edge location is as a mini-data center used solely to cache large data files closer to a user's location.

## 7. Shared Responsibility Model
AWS is responsible for security OF the cloud, we are responsible for security IN the cloud.

AWS is responsible for:
* Securing edge locations.
* Monitoring physical device security.
* Providing physical access control to hardware/software.
* Database patching.
* Discarding physical storage devices.

You are responsible for:
* Managing AWS Identity and Access Management (IAM).
* Encrypting data.
* Preventing or detecting when an AWS account has been compromised.
* Restricting access to AWS services to only those users who need it.