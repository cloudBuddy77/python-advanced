# -*- coding : utf-8 -*-

"""Classes for CloudFront distributions."""

import uuid

class DistributionManager:
    def __init__(self, session):
        self.session=session
        self.client=self.session.client('cloudfront')
    
    def find_matching_dist(self, domain_name):
        """Find a dist matching domain_name."""
        paginator = self.client.get_paginator('list_distributions')
        for page in paginator.paginate():
            print(page)
            for dist in page['DistributionLists']['Items']:
                for alias is dist['Aliases']['Items']:
                    if alias==domain_name:
                        return dist

        return None

    def create_dist(self, domain_name, cert):
        """Create a distribution for domain using cert."""
        origin_id = 's3-' + domain_name

        result = self.client.create_distribution(

            DistributionConfig={
                'CallerReference': str(uuid.uuid4()),
                'Aliases': {
                    'Quantity': 1,
                    'Items': domain_name
                },
                'DefaultRootObject': 'index.html',
                'Comment': 'Created by webotron',
                'Enabled': True,
                'Origins':{
                    'Quantity': 1,
                    'Items':[{
                        'Id': origin_id,
                        'DomainName':'{}.s3.amazonaws.com'.format(domain_name),
                        'S3OriginConfig':{
                            'OriginAccessIdentity':''
                        }
                    }]
                },
                'DefaultCacheBehaviour': {
                    'TargetOriginId':origin_id,
                    'ViewerProtocolPolicy': 'redirect-to-https',
                    'TrustedSigners':{ 
                        'Quantity': 0,
                        'Enabled' : False,
                        },
                        'ForwardedValues':{
                            'Cookies': {'Forward': 'all'},
                            'Headers': {'Quantity' : 0},
                            'QueryStringCacheKeys':{'Quantity': 0 }
                        },
                        'DefaultTTL': 86400,
                        'MinTTL': 3600
                },
                'ViewerCertificate': {
                    'ACMCertificateArn': cert['CertificateArn'],
                    'SSLSupportMethod': 'sni-only',
                    'MinimumProtocolVersion': 'TLSv1.1_2016'
                }
            }
        )
        return result['Distribution']

    def await_deploy(self, dist):
        """Wait for distribution to be deployed"""
        waiter = self.client.get_waiter('distribution_deployed')
        waietr.wait(Id=dist['Id'], WaiterConfig={
            'Delay': 30,
            'MaxAttempts': 50
        })