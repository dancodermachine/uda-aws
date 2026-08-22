# Deploy a static website to AWS

Deploy a static website to AWS by performing the following steps:

- You will create a public S3 bucket and upload the website files to your bucket.
- You will configure the bucket for website hosting and secure it using IAM policies.
- You will speed up content delivery using AWS's content distribution network service, CloudFront.
- You will access your website in a browser using the unique CloudFront endpoint.

## Folder structure

```
project/
├── deploy_static_website.py   # Deployment script (see below)
├── bucket_policy.json          # Public-read bucket policy template
├── requirements.txt            # Python dependencies
├── README.md
└── starter_website/            # Static site files to be uploaded to S3
    ├── index.html
    ├── css/
    ├── img/
    └── vendor/
```

## What `deploy_static_website.py` does

The script exposes one function per deployment step, all using `boto3` against the `us-east-2` (Ohio) region:

| Function | Purpose |
|---|---|
| `create_s3_bucket(bucket_name)` | Creates the S3 bucket (or reuses it if it already exists and is owned by you), disables "Block all public access", and attaches a public-read bucket policy. |
| `upload_folder_to_s3(folder_path, bucket_name)` | Recursively uploads every file in a local folder to the bucket, preserving the folder structure and setting the correct content type per file. |
| `apply_bucket_policy(bucket_name, policy_path)` | Applies the policy from `bucket_policy.json` to the bucket. Not called by default, since `create_s3_bucket` already applies an equivalent policy inline — kept as a standalone utility if you'd rather manage the policy as an external file. |
| `enable_static_website_hosting(bucket_name)` | Enables static website hosting on the bucket with `index.html` as both the index and error document, and returns the website endpoint URL. |
| `create_cloudfront_distribution(bucket_name)` | Creates a CloudFront distribution in front of the bucket's static website endpoint (using the AWS-managed "CachingOptimized" cache policy) and returns the distribution's domain name. |

Running the script directly (`python deploy_static_website.py`) executes the full pipeline in order: create the bucket → upload `starter_website/` → enable website hosting → create the CloudFront distribution.

## Prerequisites

- Python 3 and the dependencies in `requirements.txt`:
  ```
  pip install -r requirements.txt
  ```
- AWS credentials for an account with permissions to manage S3 and CloudFront, exported as environment variables:
  ```
  export AWS_ACCESS_KEY=your_access_key_id
  export AWS_SECRET_ACCESS_KEY=your_secret_access_key
  ```
- A globally unique S3 bucket name set in `deploy_static_website.py` (see `bucket_name` in the `if __name__ == "__main__":` block).

## Running it

```
python deploy_static_website.py
```

The bucket, uploaded files, and website endpoint are created within seconds. The CloudFront distribution can take up to 10 minutes to finish deploying before the printed domain name becomes reachable.