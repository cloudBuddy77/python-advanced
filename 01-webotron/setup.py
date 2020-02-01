from setuptools import setup

setup(
    name='webotron-80',
    version='0.1',
    author='Avinash Singh',
    description='Webotron*80 is a tool to deploy static websites in S3',
    license='GPLv3+',
    packages=['webotron'],
    url='git_hub_url',
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        webotron=webotron.webotron:cli
    '''
)