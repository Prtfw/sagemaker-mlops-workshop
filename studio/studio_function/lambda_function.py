import json
import logging

import boto3
import botocore
from botocore.exceptions import ClientError

from crhelper import CfnResource

logger = logging.getLogger(__name__)
sm = boto3.client("sagemaker")
#ec2 = boto3.client("ec2")

# cfnhelper makes it easier to implement a CloudFormation custom resource
helper = CfnResource()

# CFN Handlers


def handler(event, context):
    helper(event, context)

@helper.delete
def no_op(_, __):
    pass

@helper.create
@helper.update
def create_handler(event, context):
    print("create_handler")
    create_studio_domain(event, context)


def create_studio_domain(event, context):
  
    print("create_studio_domain")
    props = event["ResourceProperties"]

    domain_response = sm.create_domain(
        DomainName=props["DomainName"],
        AuthMode='IAM',
        DefaultUserSettings={
        'ExecutionRole': props["SMExecutionRoleArn"],
        'SharingSettings': {
            'NotebookOutputOption': 'Allowed'
            }
        },
        SubnetIds=[props["SubnetId"]],
        VpcId=props["VpcId"]
    )

   