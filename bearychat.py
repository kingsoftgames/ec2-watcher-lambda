#!/usr/bin/env python3

import boto3
from botocore.vendored import requests

BEARYCHAT_WEBHOOK = '<Your BearyChat Webhook>'
BEARYCHAT_CHANNEL = '<Your BearyChat Channel>'

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
    instance_id = event['detail']['instance-id']
    instance_url = f'https://console.amazonaws.cn/ec2/v2/home?region={region}#Instances:instanceId={instance_id}'
    state = event['detail']['state']
    name = get_instance_name(instance_id, region)
    name = f' ({name})' if name else ''
    text = f'EC2 ({region}) **{state}**: [{instance_id}]({instance_url}){name}'
    # See https://github.com/bearyinnovative/bearychat-docs/blob/master/tutorials/markdown/incoming.md
    payload = dict(
        channel=BEARYCHAT_CHANNEL,
        markdown=True,
        text=text,
    )
    return payload

def lambda_handler(event, context):
    payload = make_bearychat_payload(event)
    return send_bearychat(payload)
