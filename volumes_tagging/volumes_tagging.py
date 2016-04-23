#!/usr/bin/env python

import sys

import boto3


def get_tags(i):
    return dict(map(lambda x: (x['Key'], x['Value']), i.tags or []))

def make_tags(t):
    return map(lambda (k,v): {'Key':k, 'Value':v}, list(t.items()))

def get_volume(v_id):
    return ec2.Volume(v_id)

def get_instance(i_id):
    return ec2.Instance(i_id)

def main(event, context):
    print(event)

    global ec2

    region = event['region']
    i_id = event['detail']['instance-id']

    ec2 = boto3.resource('ec2', region_name=region)
    i = get_instance(i_id)
    t = get_tags(i)
    tags = {
	'Name': t.get('Name', ''),
	'instance_id': i_id,
    }

    volumes = map(lambda x: x['Ebs']['VolumeId'], i.block_device_mappings)
    for v in volumes:
        vol = get_volume(v)
	device = map(lambda x: x['Device'], vol.attachments).pop()
	tags.update({'device': device})
	vol.create_tags(Tags=make_tags(tags))
        print("%s tagged with: %s" % (v, tags))
