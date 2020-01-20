#!/usr/bin/python
# -*- coding : utf-8 -*-

"""Webotron will deploy a static website to AWS S3."""

"""
Webotron automates deployment of static websites:
-Configure S3 buckets
    -Create them.
    - Set them up for static website hosting.
    -Deploy local files to them
-Configure DNS with AWS Route53
-Configure a cloud delivery network and use SSL with AWS Cloudfront.
"""

import boto3
import click

from bucket import BucketManager


session=None
bucket_manager=None
#s3=session.resource('s3')

@click.group()
@click.option('--profile', default=None, help="Use an AWS Profile")
def cli(profile):
    """Webotron deploys websites to AWS."""
    global session, bucket_manager
    session_cgf = {}
    if profile:
        session_cgf['profile_name'] = profile
    session=boto3.Session(**session_cgf)
    bucket_manager  = BucketManager(session)

    pass

@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)

@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_buckets_objects(bucket):
    """List all objects for a S3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)

@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 Bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)   
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return




@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument("bucket")
def sync(pathname, bucket):
    """Sync contents of PATHNAME to S3 BUCKET."""
    bucket_manager.sync(pathname, bucket)
    print(bucket_manager.get_bucket_url(bucket_manager.s3.Bucket(bucket)))

if __name__ == '__main__':
    cli()

