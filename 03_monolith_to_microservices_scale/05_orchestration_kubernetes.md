# Orchestration with Kubernetes
## 1. Why Orchestration?
Orchestration is the automated management of the lifecycle of our application
* With CI/CD, if Travis is our CI tool, then Kubernetes is our CD tool
* Orchestration helps us handle complicated workflows in deploying our application
* Helps us automate our deployment process for continuous deployment
## 2. Kubernetes Fundamentals
**Kubernetes**
* A container orchestration system packed with features for automating our application’s deployment
* Enables us to easily scale our application and ship new code

**Pods**
* Containers often need to communicate with one another. It's not uncommon to see a deployment involving a few containers to be deployed.
* Kubernetes pods are abstractions of multiple containers and are also ephemeral.

**Services**
* Applications are often deployed with multiple replicas. This helps with load balancing and horizontal scaling.
* Services are an abstraction of a set of pods to expose them through a network.

| Term | Description |
|---|---|
| Horizontal Scaling | Handling increased traffic by creating additional replicas so that traffic can be divided across the replicas |
| Kubernetes Service | An abstraction of a set of pods and interface for how to interact with the pods |
| Pods | A set of containers that are deployed together |
| Load Balancing | Handling traffic by distributing it across different endpoints |
| Replica | A redundant copy of a resource often used for backups or load balancing |
| Consumer | An external entity such as a user or program that interfaces with an application |

## 3. Kubernetes on AWS
* AWS EKS is a service that we can use to set up Kubernetes.
* The `deployment.yaml` file is used to specify how our pods should be created.
    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: my-app
    labels:
        app: my-app
    spec:
    replicas: 2
    selector:
        matchLabels:
        app: my-app
    template:
        metadata:
        labels:
            app: my-app
        spec:
        containers:
        - name: simple-node
            image: YOUR_DOCKER_HUB/simple-node
            ports:
            - containerPort: 80
    ```
* The `service.yaml` file is used to specify how our pods are exposed.
    ```yaml
    apiVersion: v1
    kind: Service
    metadata:
    name: my-app
    labels:
        run: my-app
    spec:
    ports:
    - port: 80
        protocol: TCP
    selector:
        run: my-app
    ```
## 4. Kubernetes Cluster
Interacting With Your Cluster:
1. [Install]() `kubectl`
2. [Set up]() `aws-iam-authenticator`
3. [Set up]() `kubeconfig`

Loading YAML files:
- `kubectl apply` - create deployment and service
    ```bash
    kubectl apply -f deployment.yaml
    ```

Best practice for Handling Sensitive Strings:
* We shouldn't manually encrypt our sensitive strings. We don't want to do things that Kubernetes cantake care of.
* We don't want to manually enter sensitive strings because manual intervention defeats the purpose of automation. And for security reasons, we should not have access to an enterprise production environment to manually make changes.
* We don't need to write a script to inject values in the pods because Kubernetes can already do it for us.
* Using Kubernetes secrets is a great way to store sensitive information. When we use deployments in Kubernetes, we can set values as Kubernetes secrets so that they're protected from the end user.

## 5. Other Deployment Strategies
* **AWS ECS** - AWS proprietary solution that predates AWS EKS. It integrates very well with other AWS tools and is a bit more straightforward as it is not as feature-packed as Kubernetes.
* **AWS Fargate** - AWS tool that helps streamline deploying containers to ECS and EKS.
* **Docker** - An option to simply run the container manually with Docker. Sometimes, it's tempting to pick a shiny hot tool that may lead to over-engineered architectures.
## 6. Glossary
| Term | Description |
|---|---|
| Cluster | A group of resources that are connected to act as a single system |
| Horizontal Scaling | Handling increased traffic by creating additional replicas so that traffic can be divided across the replicas |
| Kubernetes Service | An abstraction of a set of pods and interface for how to interact with the pods |
| Pods | A set of containers that are deployed together |
| Load Balancing | Handling traffic by distributing it across different endpoints |
| Replica | A redundant copy of a resource often used for backups or load balancing |
| Consumer | An external entity such as a user or program that interfaces with an application |