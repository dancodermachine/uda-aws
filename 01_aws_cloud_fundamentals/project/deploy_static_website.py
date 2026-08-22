import mimetypes
import os
import json
import uuid
import boto3
from botocore.exceptions import ClientError


def create_s3_bucket(bucket_name: str) -> str:
    """
    Creates and configures a public S3 bucket in us-east-2 (Ohio).

    If the bucket already exists and is owned by this account,
    it will reuse and configure it.

    Parameters
    ----------
    bucket_name : str
        Name of the S3 bucket.

    Returns
    -------
    str
        Bucket name.
    """

    region = "us-east-2"

    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    # Create the bucket
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={
                "LocationConstraint": region
            }
        )

        print(f"Created S3 bucket: {bucket_name}")

    except ClientError as e:
        error_code = e.response["Error"]["Code"]

        if error_code == "BucketAlreadyOwnedByYou":
            print(f"Bucket already exists: {bucket_name}")
            print("Reusing existing bucket.")

        elif error_code == "BucketAlreadyExists":
            raise RuntimeError(
                f"Bucket name '{bucket_name}' is already taken "
                "by another AWS account."
            ) from e

        else:
            raise

    # Disable "Block all public access"
    s3.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False,
        }
    )

    # Allow anyone to READ objects
    bucket_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/*",
            }
        ],
    }

    s3.put_bucket_policy(
        Bucket=bucket_name,
        Policy=json.dumps(bucket_policy),
    )

    print(f"Configured public access for: {bucket_name}")

    return bucket_name


def upload_folder_to_s3(folder_path: str, bucket_name: str) -> int:
    """
    Uploads every file in a local folder (recursively) to an S3 bucket.

    Each file's key is set to its path relative to `folder_path`, so the
    folder structure is preserved in the bucket. Content types are guessed
    from file extensions so browsers render uploaded files correctly.

    Parameters
    ----------
    folder_path : str
        Path to the local folder whose contents will be uploaded.
    bucket_name : str
        Name of the destination S3 bucket.

    Returns
    -------
    int
        Number of files uploaded.
    """

    region = "us-east-2"

    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    uploaded_count = 0

    for root, _, files in os.walk(folder_path):
        for file_name in files:
            local_path = os.path.join(root, file_name)
            relative_path = os.path.relpath(local_path, folder_path)
            s3_key = relative_path.replace(os.sep, "/")

            content_type, _ = mimetypes.guess_type(local_path)

            extra_args = {"ContentType": content_type} if content_type else {}

            s3.upload_file(
                Filename=local_path,
                Bucket=bucket_name,
                Key=s3_key,
                ExtraArgs=extra_args,
            )

            print(f"Uploaded: {s3_key}")
            uploaded_count += 1

    print(f"Uploaded {uploaded_count} file(s) to bucket: {bucket_name}")

    return uploaded_count


def apply_bucket_policy(bucket_name: str, policy_path: str) -> None:
    """
    Applies a public-read bucket policy, loaded from a JSON file, to an S3 bucket.

    The JSON file's `Resource` field must contain a `{bucket_name}` placeholder,
    which is substituted with `bucket_name` before the policy is applied.

    Parameters
    ----------
    bucket_name : str
        Name of the S3 bucket to apply the policy to.
    policy_path : str, default="bucket_policy.json"
        Path to the JSON file containing the bucket policy template.
    """

    region = "us-east-2"

    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    with open(policy_path, "r") as f:
        policy_template = f.read()

    policy = policy_template.replace("{bucket_name}", bucket_name)

    s3.put_bucket_policy(
        Bucket=bucket_name,
        Policy=policy,
    )

    print(f"Applied bucket policy from {policy_path} to: {bucket_name}")


def enable_static_website_hosting(bucket_name: str) -> str:
    """
    Enables static website hosting on an S3 bucket.

    Sets both the index document and the error document to `index.html`,
    equivalent to editing the "Static website hosting" section under the
    bucket's Properties tab in the AWS console.

    Parameters
    ----------
    bucket_name : str
        Name of the S3 bucket to configure.

    Returns
    -------
    str
        The bucket's website endpoint URL.
    """

    region = "us-east-2"

    s3 = boto3.client(
        "s3",
        region_name=region,
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    s3.put_bucket_website(
        Bucket=bucket_name,
        WebsiteConfiguration={
            "IndexDocument": {"Suffix": "index.html"},
            "ErrorDocument": {"Key": "index.html"},
        },
    )

    website_endpoint = f"http://{bucket_name}.s3-website.{region}.amazonaws.com"

    print(f"Static website hosting enabled: {website_endpoint}")

    return website_endpoint


def create_cloudfront_distribution(bucket_name: str) -> str:
    """
    Creates a CloudFront distribution in front of an S3 static website.

    Uses the bucket's static website hosting endpoint (not the S3 REST
    endpoint) as the origin, with the AWS-managed "CachingOptimized" cache
    policy and all other settings left at their defaults, equivalent to
    clicking "Create Distribution" in the CloudFront console.

    Parameters
    ----------
    bucket_name : str
        Name of the S3 bucket, already configured for static website
        hosting, to serve through CloudFront.

    Returns
    -------
    str
        The distribution's domain name.
    """

    region = "us-east-2"
    caching_optimized_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
    origin_id = bucket_name

    cloudfront = boto3.client(
        "cloudfront",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    )

    response = cloudfront.create_distribution(
        DistributionConfig={
            "CallerReference": str(uuid.uuid4()),
            "Comment": f"Distribution for {bucket_name}",
            "Enabled": True,
            "Origins": {
                "Quantity": 1,
                "Items": [
                    {
                        "Id": origin_id,
                        "DomainName": f"{bucket_name}.s3-website.{region}.amazonaws.com",
                        "CustomOriginConfig": {
                            "HTTPPort": 80,
                            "HTTPSPort": 443,
                            "OriginProtocolPolicy": "http-only",
                        },
                    }
                ],
            },
            "DefaultCacheBehavior": {
                "TargetOriginId": origin_id,
                "ViewerProtocolPolicy": "redirect-to-https",
                "AllowedMethods": {
                    "Quantity": 2,
                    "Items": ["GET", "HEAD"],
                },
                "CachePolicyId": caching_optimized_policy_id,
            },
        }
    )

    domain_name = response["Distribution"]["DomainName"]

    print(f"Domain Name: {domain_name}")
    print("It may take up to 10 minutes for the distribution to deploy.")

    return domain_name


if __name__ == "__main__":
    bucket_name = "clean-blog-1234567890"
    folder_path = os.path.join(os.path.dirname(__file__), "starter_website")

    create_s3_bucket(bucket_name)
    upload_folder_to_s3(folder_path, bucket_name)
    # Not called: create_s3_bucket already applies an equivalent public-read
    # policy inline (see its bucket_policy dict above), so calling this too
    # would just overwrite the bucket policy with the same effective rules.
    # apply_bucket_policy(bucket_name, "bucket_policy.json")
    enable_static_website_hosting(bucket_name)
    create_cloudfront_distribution(bucket_name)
