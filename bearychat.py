#!/usr/bin/env python3

import boto3
from botocore.vendored import requests

BEARYCHAT_WEBHOOK = '<Your BearyChat Webhook>'
BEARYCHAT_CHANNEL = '<Your BearyChat Channel>'


def get_aws_console_domain(region):
    if region.startswith('cn-'):
        return 'console.amazonaws.cn'
    else:
        return 'console.aws.amazon.com'


def get_instance_url(instance_id, region):
    domain = get_aws_console_domain(region)
    return (f'https://{domain}/ec2/v2/home'
            f'?region={region}'
            f'#Instances:instanceId={instance_id}')


def get_instance_name(instance_id, region):
    ec2 = boto3.resource('ec2', region_name=region)
    instance = ec2.Instance(instance_id)
    name = None
    for tags in instance.tags:
        if tags['Key'] == 'Name':
            name = tags['Value']
    return name


def send_bearychat(payload):
    r = requests.post(BEARYCHAT_WEBHOOK, json=payload)
    return r.text


def make_bearychat_payload(event):
    region = event['region']
    state = event['detail']['state']
    instance_id = event['detail']['instance-id']
    instance_url = get_instance_url(instance_id, region)
    name = get_instance_name(instance_id, region)
    name = f' ({name})' if name else ''
    text = f'EC2 ({region}) **{state}**: [{instance_id}]({instance_url}){name}'
    # https://github.com/bearyinnovative/bearychat-docs/blob/master/tutorials/markdown/incoming.md
    payload = dict(
        channel=BEARYCHAT_CHANNEL,
        markdown=True,
        text=text,
    )
    return payload


def lambda_handler(event, context):
    payload = make_bearychat_payload(event)
    return send_bearychat(payload)
