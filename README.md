# AWS Developer

## Mentors

## Projects
* [GitHub Repo](https://github.com/dancodermachine/uda-aws_project_microservices)

## Requirements
Create the following environment variables.
```
AWS_ACCESS_KEY
AWS_BUCKET
AWS_PROFILE
AWS_REGION
AWS_SECRET_ACCESS_KEY
```

### 1. Install AWS CLI in GitHub Codespaces

Open your GitHub Codespace terminal.

Update the package list:

```bash
sudo apt-get update
```

Install the required dependencies:

```bash
sudo apt-get install -y curl unzip
```

Download AWS CLI:

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
```

Extract the installation files:

```bash
unzip awscliv2.zip
```

Install AWS CLI:

```bash
sudo ./aws/install
```

Verify the installation:

```bash
aws --version
```

**Note:** These commands assume your Codespace uses Linux on an x86_64 architecture.

### 2. Configure AWS Credentials

In the [AWS Management Console](https://aws.amazon.com/console/):

1. Navigate to **IAM (Identity and Access Management)**.
2. Create an IAM user with the required permissions.
3. Generate an access key for CLI usage.
4. Store your credentials securely.

In your Codespace terminal, run:

```bash
aws configure --profile developer
```

Enter:

```text
AWS Access Key ID: YOUR_ACCESS_KEY
AWS Secret Access Key: YOUR_SECRET_KEY
Default region name: eu-west-2
Default output format: json
```

Verify the configuration:

```bash
aws sts get-caller-identity --profile developer
```

**Security:** Never commit AWS credentials to your repository. Prefer temporary credentials when available.

## References
