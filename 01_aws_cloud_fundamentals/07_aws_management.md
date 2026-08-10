# AWS Management
## 1. Logging & Auditing in the Cloud
Logging in the cloud provides visibility into your cloud resources and applications. For applications that run in the cloud, you will need access to logging and auditing services to help you proactively monitor your resources and applications.

Logging allows you to answer important questions like:
* How is this server performing?
* What is the current load on the server?
* What is the root cause of an application error that a user is seeing?
* What is the path that leads to this error?

## 2. CloudTrail
CloudTrail allows you to audit (or review) everything that occurs in your AWS account. CloudTrail does this by recording all the AWS API calls occurring in your account and delivering a log file to you.

CloudTrail provides event history of your AWS account activity, including:
* who has logged in
* services that were accessed
* actions performed
* parameters for the actions
* responses returned

This includes actions taken through the AWS Management Console, AWS SDKs, command line tools, and other AWS services.

Tips:
* CloudTrail is found under the Management & Governance section on the AWS Management Console.
* CloudTrail shows results for the last 90 days.
* You can create up to five trails in an AWS region.

## 3. CloudWatch
CloudWatch is a service that monitors resources and applications that run on AWS by collecting data in the form of logs, metrics, and events.

There are several useful features:
* Collect and track metrics.
* Collect and monitor log files.
* Set alarms and create triggers to run your AWS resources.
* React to changes in your AWS resources.

Tips:
* CloudWatch is found under the Management & Governance section on the AWS Management Console.
* Metrics are provided automatically for a number of AWS products and services.

## 4. Infrastructure as a Code
Infrastructure as Code allows you to describe and provision all the infrastructure resources in your cloud environment. You can stand up servers, databases, runtime parameters, resources, etc. based on scripts that you write. Infrastructure as Code is a time-saving feature because it allows you to provision (or stand up) resources in a reproducible way.

## 5. CloudFormation
AWS CloudFormation allows you to model your entire infrastructure in a text file template allowing you to provision AWS resources based on the scripts you write.

Tips:
* CloudFormation is found under the Management & Governance section on the AWS Management Console.
* CloudFormation templates are written using JSON or YAML.
* You can still individually manage AWS resources that are part of a CloudFormation stack.

## 6. Command Line
List all instances running in the account.
```bash
aws ec2 describe-instances
```