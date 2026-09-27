# Full Stack Apps on AWS Project

You have been hired as a software engineer to develop an application that will help the FBI find missing people.  The application will upload images to the FBI cloud database hosted in AWS. This will allow the FBI to run facial recognition software on the images to detect a match. You will be developing a NodeJS server and deploying it on AWS Elastic Beanstalk. 
You will build upon the application we've developed during the lessons in this course. You'll complete a REST API endpoint in a backend service that processes incoming image URLs.

## Getting Started

You can clone this repo to run the project locally, or navigate to the workspace in the Udacity course.

## Project Instructions

To complete this project, you will need to:

* Set up node environment
* Create a new endpoint in the server.js file
* Deploying your system

## Testing

Successful URL responses should have a 200 code. Ensure that you include error codes for the scenario that someone uploads something other than an image and for other common errors.

## Deploying with the Elastic Beanstalk CLI

### Prerequisites

* An AWS account with an IAM user that has permissions to create Elastic Beanstalk, EC2, and related resources.
* AWS credentials available locally (either an `~/.aws/credentials` file from `aws configure`, or the `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` environment variables).
* The EB CLI installed:
  ```bash
  pip install awsebcli --user
  ```
  Make sure the install location (e.g. `~/.local/bin`) is on your `PATH`.

### 1. Initialize the application

From the project directory (where `package.json` lives):

```bash
eb init
```

You'll be prompted for:

* **Region** — e.g. `us-east-1`
* **Application name** — accept the default or choose your own
* **Platform** — select **Node.js** (pick the version matching your local `node --version`)
* **CodeCommit** — No
* **SSH** — optional, only needed if you want to SSH into the EC2 instance later

### 2. Create the environment (first deploy)

```bash
eb create <environment-name>
```

This provisions the EC2 instance, load balancer, security groups, and auto-scaling group, then deploys your code. It takes several minutes. On success it prints a live URL, e.g.:

```
Application available at <environment-name>.<random-id>.<region>.elasticbeanstalk.com
```

### 3. Verify the deployment

```bash
eb open
```

or test the endpoint directly:

```bash
curl -i "http://<your-eb-url>/filteredimage?image_url=<public-image-url>"
```

### 4. Deploy future changes

Whenever you update the code, push it to the existing environment:

```bash
eb deploy
```

### Useful commands

* `eb status` — show environment health and URL
* `eb logs` — pull server logs from the EC2 instance for debugging
* `eb terminate <environment-name>` — tear down the environment and stop AWS charges when you're done

## License

[License](LICENSE.txt)