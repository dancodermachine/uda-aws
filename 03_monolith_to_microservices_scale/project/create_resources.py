"""Create and configure the S3 bucket and RDS database used by the Udagram
backend services.

Reads AWS_BUCKET / AWS_REGION / POSTGRES_* from the environment and relies
on boto3's default credential chain (AWS_ACCESS_KEY_ID /
AWS_SECRET_ACCESS_KEY / AWS_SESSION_TOKEN, or AWS_PROFILE) for auth.
"""
import json
import os
import sys

import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = os.environ.get('AWS_BUCKET')
AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')

DB_INSTANCE_IDENTIFIER = os.environ.get('POSTGRES_DB_INSTANCE', 'udagram-postgres')
POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'postgres')
POSTGRES_PORT = 5432


def create_bucket(s3_client, bucket_name, region):
    """Create an S3 bucket with default configuration.

    Parameters
    ----------
    s3_client : botocore.client.S3
        Boto3 S3 client used to issue the request.
    bucket_name : str
        Name of the bucket to create.
    region : str
        AWS region to create the bucket in.
    """
    try:
        if region == 'us-east-1':
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': region},
            )
        print(f'Created bucket "{bucket_name}" in {region}.')
    except ClientError as error:
        code = error.response['Error']['Code']
        if code in ('BucketAlreadyOwnedByYou', 'BucketAlreadyExists'):
            print(f'Bucket "{bucket_name}" already exists, continuing.')
        else:
            raise


def allow_public_access(s3_client, bucket_name):
    """Disable the account-level public access block for this bucket.

    S3 rejects a public bucket policy while any of these block settings
    are on, so they must be turned off before applying the policy.

    Parameters
    ----------
    s3_client : botocore.client.S3
        Boto3 S3 client used to issue the request.
    bucket_name : str
        Name of the bucket to update.
    """
    s3_client.put_public_access_block(
        Bucket=bucket_name,
        PublicAccessBlockConfiguration={
            'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False,
        },
    )
    print(f'Disabled public access block for "{bucket_name}".')


def set_bucket_policy(s3_client, bucket_name):
    """Attach a public bucket policy allowing full object access.

    Parameters
    ----------
    s3_client : botocore.client.S3
        Boto3 S3 client used to issue the request.
    bucket_name : str
        Name of the bucket to update.
    """
    policy = {
        'Version': '2012-10-17',
        'Statement': [
            {
                'Sid': 'PublicReadWriteAccess',
                'Effect': 'Allow',
                'Principal': '*',
                'Action': 's3:*',
                'Resource': [
                    f'arn:aws:s3:::{bucket_name}',
                    f'arn:aws:s3:::{bucket_name}/*',
                ],
            },
        ],
    }
    s3_client.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
    print(f'Applied public bucket policy to "{bucket_name}".')


def set_cors_configuration(s3_client, bucket_name):
    """Attach a permissive CORS configuration for browser clients.

    Parameters
    ----------
    s3_client : botocore.client.S3
        Boto3 S3 client used to issue the request.
    bucket_name : str
        Name of the bucket to update.
    """
    cors_configuration = {
        'CORSRules': [
            {
                'AllowedHeaders': ['*'],
                'AllowedMethods': ['POST', 'GET', 'PUT', 'DELETE', 'HEAD'],
                'AllowedOrigins': ['*'],
                'ExposeHeaders': [],
            },
        ],
    }
    s3_client.put_bucket_cors(
        Bucket=bucket_name,
        CORSConfiguration=cors_configuration,
    )
    print(f'Applied CORS configuration to "{bucket_name}".')


def get_default_security_group_id(ec2_client):
    """Look up the default security group for the account's default VPC.

    Parameters
    ----------
    ec2_client : botocore.client.EC2
        Boto3 EC2 client used to issue the request.

    Returns
    -------
    str
        ID of the default security group.
    """
    vpcs = ec2_client.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
    default_vpc_id = vpcs['Vpcs'][0]['VpcId']

    response = ec2_client.describe_security_groups(
        Filters=[
            {'Name': 'group-name', 'Values': ['default']},
            {'Name': 'vpc-id', 'Values': [default_vpc_id]},
        ],
    )
    return response['SecurityGroups'][0]['GroupId']


def allow_postgres_ingress(ec2_client, security_group_id, port):
    """Open the security group's inbound rule to allow connections from anywhere.

    This lets a local PostgreSQL client (or an app running outside AWS)
    reach the database, per the project setup instructions.

    Parameters
    ----------
    ec2_client : botocore.client.EC2
        Boto3 EC2 client used to issue the request.
    security_group_id : str
        ID of the security group to update.
    port : int
        TCP port to open (5432 for PostgreSQL).
    """
    try:
        ec2_client.authorize_security_group_ingress(
            GroupId=security_group_id,
            IpPermissions=[
                {
                    'IpProtocol': 'tcp',
                    'FromPort': port,
                    'ToPort': port,
                    'IpRanges': [
                        {
                            'CidrIp': '0.0.0.0/0',
                            'Description': 'Allow PostgreSQL access from anywhere',
                        },
                    ],
                },
            ],
        )
        print(f'Opened port {port} to 0.0.0.0/0 on security group "{security_group_id}".')
    except ClientError as error:
        if error.response['Error']['Code'] == 'InvalidPermission.Duplicate':
            print(f'Port {port} is already open to 0.0.0.0/0 on security group "{security_group_id}".')
        else:
            raise


def create_db_instance(rds_client, db_instance_identifier, db_name, username, password, port, security_group_ids):
    """Create a free-tier, publicly accessible PostgreSQL RDS instance.

    Parameters
    ----------
    rds_client : botocore.client.RDS
        Boto3 RDS client used to issue the request.
    db_instance_identifier : str
        Identifier for the DB instance.
    db_name : str
        Name of the initial database to create.
    username : str
        Master username for the database.
    password : str
        Master password for the database.
    port : int
        Port the database should listen on.
    security_group_ids : list of str
        VPC security group IDs to associate with the instance.
    """
    try:
        rds_client.create_db_instance(
            DBInstanceIdentifier=db_instance_identifier,
            DBName=db_name,
            Engine='postgres',
            MasterUsername=username,
            MasterUserPassword=password,
            Port=port,
            DBInstanceClass='db.t3.micro',
            AllocatedStorage=20,
            VpcSecurityGroupIds=security_group_ids,
            PubliclyAccessible=True,
            BackupRetentionPeriod=0,
        )
        print(f'Creating database instance "{db_instance_identifier}"...')
    except ClientError as error:
        if error.response['Error']['Code'] == 'DBInstanceAlreadyExists':
            print(f'Database instance "{db_instance_identifier}" already exists, continuing.')
        else:
            raise


def wait_for_db_instance(rds_client, db_instance_identifier):
    """Block until the DB instance is available.

    Parameters
    ----------
    rds_client : botocore.client.RDS
        Boto3 RDS client used to issue the request.
    db_instance_identifier : str
        Identifier of the DB instance to wait on.
    """
    print('Waiting for the database to become available (this can take several minutes)...')
    waiter = rds_client.get_waiter('db_instance_available')
    waiter.wait(DBInstanceIdentifier=db_instance_identifier)


def get_db_endpoint(rds_client, db_instance_identifier):
    """Fetch the connection endpoint for a DB instance.

    Parameters
    ----------
    rds_client : botocore.client.RDS
        Boto3 RDS client used to issue the request.
    db_instance_identifier : str
        Identifier of the DB instance to look up.

    Returns
    -------
    str
        Hostname the database can be reached at.
    """
    response = rds_client.describe_db_instances(DBInstanceIdentifier=db_instance_identifier)
    return response['DBInstances'][0]['Endpoint']['Address']


def main():
    if not BUCKET_NAME:
        sys.exit('AWS_BUCKET is not set.')
    if not (POSTGRES_USERNAME and POSTGRES_PASSWORD):
        sys.exit('POSTGRES_USERNAME / POSTGRES_PASSWORD are not set.')

    s3_client = boto3.client('s3', region_name=AWS_REGION)
    ec2_client = boto3.client('ec2', region_name=AWS_REGION)
    rds_client = boto3.client('rds', region_name=AWS_REGION)

    create_bucket(s3_client, BUCKET_NAME, AWS_REGION)
    allow_public_access(s3_client, BUCKET_NAME)
    set_bucket_policy(s3_client, BUCKET_NAME)
    set_cors_configuration(s3_client, BUCKET_NAME)

    security_group_id = get_default_security_group_id(ec2_client)
    allow_postgres_ingress(ec2_client, security_group_id, POSTGRES_PORT)
    create_db_instance(
        rds_client,
        DB_INSTANCE_IDENTIFIER,
        POSTGRES_DB,
        POSTGRES_USERNAME,
        POSTGRES_PASSWORD,
        POSTGRES_PORT,
        [security_group_id],
    )
    wait_for_db_instance(rds_client, DB_INSTANCE_IDENTIFIER)
    endpoint = get_db_endpoint(rds_client, DB_INSTANCE_IDENTIFIER)

    print(f'\nDatabase is available at: {endpoint}:{POSTGRES_PORT}')
    print(f'Set POSTGRES_HOST={endpoint} in set_env.sh, then test the connection with:')
    print(f'  psql -h {endpoint} -U {POSTGRES_USERNAME} {POSTGRES_DB}')


if __name__ == '__main__':
    main()
