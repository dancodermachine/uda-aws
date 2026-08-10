# Messaging & Containers
## 1. Simple Notification Service (SNS)
**Amazon Simple Notification Service (SNS)** is a cloud service that allows you to send notifications to the users of your applications. SNS allows you to decouple the notification logic from being embedded in your applications and allows notifications to be published to a large number of subscribers.

## 2. AWS EventBridge
As the developer, you would put targets in your code, and use AWS CloudWatch to connect your targets to an AWS EventBridge rule. Viewing the rules in the AWS EventBridge console lets you see what errors have occurred in your code.

EventBridge allows you to build event-driven architectures, which are loosely coupled and distributed. It helps improve developer flexibility in addition to increasing application resiliency. It enables you to decouple your architectures to make it faster to build and innovate by using routing rules to deliver events to selected targets. It is free to leverage AWS Evenbridge for all AWS Services.

AWS EventBridge Pipes allow you to connect multiple AWS services and send data between them. You may find this advanced feature to be useful if you are connecting the data from events in one service to an action you want to be done in another service.

Use Cases for AWS EventBridge:
* **Increase developer agility**: Support microservice architecture by removing the need to coordinate across service teams.
* **Monitor and audit applications**: React to alerts in real-time monitoring capabilities
* **Extend functionality with SaaS integrations**: Ability to connect to your applications to other SAAS providers.
* **Customize SaaS with AI/ML**: Load data from SAAS and apply Machine Learning Techniques

## 3. Queues
A queue is a data structure that holds requests called messages. Messages in a queue are commonly processed in order, first in, first out (or FIFO).

Messaging queues improve:
* performance
* scalability
* user experience

### 3.1 Amazon Simple Queue Service (SQS)
SQS is a fully managed message queuing service that allows you to integrate queuing functionality into your application. SQS offers two types of message queues: standard and FIFO.

Features:
* send messages
* store messages
* receive messages

Tips:
* The Simple Queue Service (SQS) is found under the Application Integration on the AWS Management Console.
* FIFO queues support up to 3,000 messages per second with batching or up to 300 messages per second without batching.
* FIFO queues guarantee the ordering of messages.
* Standard queues offer best-effort ordering but no guarantees.
* Standard queues deliver a message at least once, but occasionally more than one copy of a message is delivered.

## 4. Containers
### 4.1 What is a Container?
OS level virtualization allows us to run multiple isolated processes in parallel. A container is an isolated process that consists of the following items, all bundled into one package:
* the application code,
* the required dependencies (e.g. libraries, utilities, configuration files), and
* the necessary runtime environment to run the application.

Each container is an independent component that can run on its own and be moved from environment to environment.

### 4.2 Benefits of a Container
* Containers make it easier for developers to create, deploy, and run applications on different hardware and platforms, quickly and easily.
* Containers share a single kernel and share application libraries.
* Containers cause a lower system overhead as compared to Virtual Machines.

### 4.3 How to create containers?
Several platforms (called Container runtime/engines) allow us to create containers. A few such platforms are:
* Docker
* CRI-O
* OpenVZ
* Containerd

### 4.4 Docker Containers versus Virtual Machines
There are several benefits of using Containers over VMs:
* Size: Containers are much smaller than Virtual Machines (VM) and run as isolated processes versus virtualized hardware. VMs can be in GBs while containers are in MBs.
* Speed: Virtual Machines can be slow to boot and take minutes to launch. A container can spawn much more quickly typically in seconds.
* Composability: Containers are designed to be programmatically built and are defined as source code. Virtual Machines are often replicas of a conventional computer system.

### 4.5 Docker
Docker is a (container runtime) tool that helps to build, test, and run containers. You can build containers locally using a command-line utility, Docker Desktop. If there are multiple containers running individual services of an application, you will need to use Docker Compose utility to specify dependent relationships between containers.

### 4.6 Docker Image
An image (or Docker image) is a portable auto-generated template that contains a set of instructions to create a container. An image can be instantiated multiple numbers of times to create multiple containers.

### 4.7 Dockerfile
A text file containing commands to create an image. In other words, Docker generates images by reading the commands from a Dockerfile.

### 4.8 What is Elastic Container Service (ECS)?
ECS is an orchestration service used for automating deployment, scaling, and managing of your containerized applications. ECS works well with Docker containers by:
* launching and stopping Docker containers
* scaling your applications
* querying the state of your applications

Tips:
* ECS falls under the Compute section on the AWS Management Console.
* You can schedule long-running applications, services, and batch processes using ECS.
* Docker is the only container-runtime platform supported by Amazon ECS. Other container-runtime tools available in the industry are Openshift from RedHat, Rocket, LXD, OpenVZ, and a few more.