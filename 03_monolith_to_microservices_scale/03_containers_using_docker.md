# Containers using Docker
## 1. Intro Containers
* Containers are self-contained applications with all the dependencies needed to run.
* Containers can be treated as one unit of deployment.
* Rolling back code with containers is simply re-deploying an older snapshot.
* **Containers are Ephemeral**: Containers should be stateless and are expected to be destroyed.
* **Containers Help Manage Dependencies**: Each container can be running its own versioned software. We resolve the issue where different applications may have different dependencies.
* **Simplify Deployment**: Containers are self-contained so deployment is simply swapping out an existing container with a new one.

## 2. Docker
Docker is a platform that helps us manage the process of creating and managing our containers.
* **Docker Image**: When we have an application that we want to deploy, we can package it into a Docker Image. The image contains all of your code and dependencies.
* **Docker Container**: A Docker Container is an ephemeral running instance of a Docker Image.
* **Dockerfile**: A Dockerfile defines the steps to create a Docker Image.

| Action | Command |
|---|---|
| Create Docker image | `docker build -t <IMAGE_NAME> .` |
| Show Docker images | `docker images` |
| Run Docker image | `docker run <IMAGE_ID>` |
| Show running Docker containers | `docker ps` |
| Show all Docker containers, including stopped containers | `docker ps -a` |
| Terminate a Docker container | `docker kill <CONTAINER_ID>` |
| Show logs | `docker logs` |
| Inspect detailed information about a Docker container or image | `docker inspect <CONTAINER_ID_OR_IMAGE_ID>` |

| Term | Definition |
|---|---|
| Base Image | A set of common dependencies built into a Docker image that acts as a starting point to build an application's Docker images to reduce build times |
| Container | Grouped software dependencies and packages that make it easier and more reliable to deploy software |
| Container Registry | A centralized place to store container images |
| Docker-compose | A tool used to run multiple Docker containers at once; often used to specify dependent relationships between containers |
| Dockerfile | A file containing instructions on how to translate an application into an image that can be run in containers |
| Ephemeral | Software property where an application is expected to be short-lived |
| Image | A snapshot of dependencies and code used by Docker containers to run an application |

```
Dockerfile
    │
    │ docker build
    ▼
Docker Image
    │
    │ docker run
    ▼
Container
```

Further reading:
* [Best Practices for writing Dockerfiles](https://docs.docker.com/build/building/best-practices/)
* [Docker Command-line Reference](https://docs.docker.com/reference/cli/docker/)

## 3. Debug Container
Why might a container work in a local environment but not in a deployed environment?
* Docker is programming language agnostic so it doesn't matter which programming language you use.
* Security restrictions can cause problems because we often have to interface with other resources and the permission we use locally, may be different than in the deployed environment.
* System resouces are also important to ensure we have all of the resources that an application needs to run.
* Credentials can also be problematic as you deploy code from a local environment to a deployed environment.

## 4. Container Registries
A container registry serves as a centralized place to store and version images.

[DockerHub](https://hub.docker.com/) is a popular container registry run by the same organization that created Docker.

### 4.1 Creating and Using a Docker Hub Repository:
1. In Docker Hub, create a new repository and set it to **Public**.
2. In your terminal, log in to Docker Hub:
    ```bash
    docker login --username={YOUR_USERNAME}
    ```
3. Tag your local image with the repository name:
    ```bash
    docker tag {LOCAL_IMAGE_NAME} {USERNAME}/{REPOSITORY_NAME}
    ```
4. Push the image to Docker Hub:
    ```bash
    docker push {TAGGED_IMAGE}
    ```

**Why Do We Need a Unique ID?**

We often reference Docker images by specifying the latest image, but having a unique identifier helps a lot with Docker images.
* We can reference a specific build
* Can revert to an older version

### 4.2 Pushing an Image to Docker Hub
1. Create a **Docker Hub** account.
2. Create a new repository on Docker Hub.
3. Build a Docker image (or use the one from the previous exercise).
4. Tag the image:
    ```bash
    docker tag simple-node {YOUR_USERNAME}/{YOUR_REPOSITORY_NAME}
    ```
5. Log in to Docker Hub:
    ```bash
    docker login --username={YOUR_USERNAME}
    ```
6. Push the tagged image to Docker Hub:
    ```bash
    docker push {TAGGED_IMAGE}
    ```
7. Return to Docker Hub and confirm that the image has been pushed to the repository.
8. Pull the image back to your local machine:
    ```bash
    docker pull {TAGGED_IMAGE}
    ```

## 5. Modifying Containers
Best Practices for Modifying Containers:
* Docker images should be considered a single unit of deployment.
* You shouldn't be editing code or making changes to the system at all in a container.
* If something is broken, you build a new image and deploy that to a new container.