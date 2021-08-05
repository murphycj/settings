#!/usr/bin/env python

from __future__ import print_function

import argparse
import json
import os
import sys

import dateutil.parser
import boto3
from tabulate import tabulate


def main():
    args = read_args()
    homedir = os.path.expanduser('~')

    instances = get_running_instances()
    instances.sort(key=lambda x: x.launch_time, reverse=True)
    table = []
    for k, i in enumerate(instances):
        if i.state.get('Name', '') != 'running':
            continue

        name = 'server{}'.format(k)
        owner = '-'

        if i.tags:
            names = list(filter(lambda x: x['Key']=='Name', i.tags))
            owners = list(filter(lambda x: x['Key']=='Owner', i.tags))

            if names:
                name = names[0].get('Name', 'server{}'.format(k))

            if owners:
                owner = owners[0].get('Owner', '-')

        # print >>sys.stderr, '\t'.join([name, i.instance_type, owner])
        table.append([name, i.instance_type, owner, i.launch_time])
        print('Host', name)
        print('    Hostname', i.public_ip_address)

        if i.image_id == 'ami-20fb4848':
            print('    User ubuntu')
        else:
            print('    User ec2-user')

        print('    Port 22')

        print('    IdentityFile {}/.ssh/{}.pem'.format(homedir, i.key_name))
        print()

    print(tabulate(table, tablefmt='psql'), file=sys.stderr)


def get_running_instances():
    regions = ['us-east-1']
    instances = []
    for region in regions:
        ec2 = boto3.resource('ec2', region)

        result = ec2.instances.filter(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

        for instance in result:
            instances.append(instance)

    return instances


def read_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-m', '--mode', help='')
    parser.add_argument('-c', '--config', help='', default='~/.aws/config.json')
    parser.add_argument('-f', '--full', action='store_true', help='')
    parser.add_argument('-a', '--aws', action='store_true', help='')
    parser.add_argument('-p', '--persistent', help='')

    args = parser.parse_args()

    return args


if __name__ == '__main__':
    main()
