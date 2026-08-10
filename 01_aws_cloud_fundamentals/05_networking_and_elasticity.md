# Networking & Elasticity
## 1. Networking in the Cloud
Networks reliably carry loads of data around the globe allowing for the delivery of content and applications with high availability. The network is the foundation of your infrastructure.

Cloud networking includes:
* network architecture
* network connectivity
* application delivery
* global performance
* delivery

### 1.1 DNS
The Domain Name System (DNS) is the phonebook of the Internet. It enables humans to go to the internet and browse for a simple user-friendly name which internally then converts it to a unique IP address.

It is one of the foundational internet services that make the internet work.

## 2. Route S3
Amazon Route 53 is a highly available and scalable cloud domain name system (DNS) service that has servers distributed around the globe used to translates human-readable names like www.google.com into the numeric IP addresses like 74.125.21.147.

Features
* scales automatically to manage spikes in DNS queries.
* allows you to register a domain name (or manage an existing).
* routes internet traffic to the resources for your domain.
* checks the health of your resources.

Tips
* Route 53 is found under the Networking & Content Delivery section on the AWS Management Console.
* Route 53 allows you to route users based on the user’s geographic location.

## 3. Purpose of Elasticity in the Cloud
One of the main benefits of the cloud is that it allows you to stop guessing about capacity when you need to run your applications. Sometimes you buy too much or you don't buy enough to support the running of your applications.

With elasticity, your servers, databases, and application resources can automatically scale up or scale down based on load.

## 4. EC2 Auto Scaling
**EC2 Auto Scaling** is a service that monitors your EC2 instances and automatically adjusts by adding or removing EC2 instances based on conditions you define in order to maintain application availability and provide peak performance to your users.

Features:
* Automatically scale in and out based on needs.
* Included automatically with Amazon EC2.
* Automate how your Amazon EC2 instances are managed.

Tips:
* EC2 Auto Scaling is found on the EC2 Dashboard.
* EC2 Auto Scaling adds instances only when needed, optimizing cost savings.
* EC2 predictive scaling removes the need for manual adjustment of auto scaling parameters over time.

A key feature of EC2 Auto Scaling is that it works very well with AWS Messaging Services such as Simple Notification Service (SNS) to help alert you when an EC2 condition occurs which is either when it is launched or terminated.

EC2 Auto Scaling Service vs AWS Auto Scaling Service:
* **Amazon EC2 Auto Scaling** provides the ability to easily increase and decrease capacity to match demand.
* **AWS Auto Scaling Service** offers a common central place to manage configurations for a wider range of scalable resources, such as EC2 instances, Amazon Elastic Container Service (ECS), Amazon DynamoDB tables etc.

## 5. Elastic Load Balancing
Elastic Load Balancing automatically distributes incoming application traffic across multiple servers.

Elastic Load Balancer is a service that:
* Balances load between two or more servers
* Stands in front of a web server
* Provides redundancy and performance

Tips:
* Elastic Load Balancing can be found on the EC2 Dashboard.
* Elastic Load Balancing works with EC2 Instances, containers, IP addresses, and Lambda functions.
* You can configure Amazon EC2 instances to only accept traffic from a load balancer.