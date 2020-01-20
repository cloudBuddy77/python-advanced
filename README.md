# python-advanced
This will use advanced python concepts
This will automate AWS.

# 01-webotron:
This project will automatically sync local directory with amazon s3 bucket.

# Features
This will list buckets:
    '''python webotron.py list-buckets'''
Objects of a bucket can be listed by:
    '''python webotron.py list-bucket-objects <bucket_name>'''
This will create a new bucket:
    '''python webotron.py setup-bucket <bucket_name>'''
This will sync a local directory to S3 bucket:
    '''python webotron.py sync <pathname> <bucket_name>'''
Set AWS profile with --profile optional parameter.