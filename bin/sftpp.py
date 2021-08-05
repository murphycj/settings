#!/usr/local/bin/python3

from __future__ import print_function
import os
import sys


def main(args, username):

    hosts = {}

    fin = open("/Users/{}/.ssh/config".format(username), 'r')
    current_host = ''
    for line in fin.readlines():
        if line.find('Host ') != -1:

            if current_host != '':
                hosts[current_host] = {
                    'hostname': hostname,
                    'user': user,
                    'port': port,
                    'identifyfile': identifyfile
                }

            current_host = line.strip().split(" ")[1]
        elif line.find('Hostname ') != -1:
            hostname = line.strip().split(" ")[1]
        elif line.find('User ') != -1:
            user = line.strip().split(" ")[1]
        elif line.find('Port ') != -1:
            port = line.strip().split(" ")[1]
        elif line.find('IdentityFile ') != -1:
            identifyfile = line.strip().split(" ")[1]
    fin.close()

    hosts[current_host] = {
        'hostname': hostname,
        'user': user,
        'port': port,
        'identifyfile': identifyfile
    }

    if args[2] not in hosts:
        print("Host not in ~/.ssh/config")
        sys.exit()

    if args[1] == 'up':
        cmd = "scp -P {} -i {} {} {}@{}:{}".format(
            hosts[args[2]]['port'],
            hosts[args[2]]['identifyfile'],
            args[3],
            hosts[args[2]]['user'],
            hosts[args[2]]['hostname'],
            args[4])

        print(cmd)
        os.system(cmd)

    elif args[1] == 'down':
        cmd = "scp -P {} -i {} {}@{}:{} {}".format(
            hosts[args[2]]['port'],
            hosts[args[2]]['identifyfile'],
            hosts[args[2]]['user'],
            hosts[args[2]]['hostname'],
            args[3],
            args[4])

        print(cmd)
        os.system(cmd)

    elif args[1] == 'upr':
        cmd = "scp -r -P {} -i {} {} {}@{}:{}".format(
            hosts[args[2]]['port'],
            hosts[args[2]]['identifyfile'],
            args[3],
            hosts[args[2]]['user'],
            hosts[args[2]]['hostname'],
            args[4])

        print(cmd)
        os.system(cmd)

    else:
        cmd = "scp -r -P {} -i {} {}@{}:{} {}".format(
            hosts[args[2]]['port'],
            hosts[args[2]]['identifyfile'],
            hosts[args[2]]['user'],
            hosts[args[2]]['hostname'],
            args[3],
            args[4])

        print(cmd)
        os.system(cmd)

def main_config(args, username):

    if args[1] == 'up':
        cmd = "scp {} {}:{}".format(
            args[3],
            args[2],
            args[4])

        print(cmd)
        os.system(cmd)

    elif args[1] == 'down':
        cmd = "scp {}:{} {}".format(
            args[3],
            args[2],
            args[4])

        print(cmd)
        os.system(cmd)

    elif args[1] == 'upr':
        cmd = "scp -r {} {}:{}".format(
            args[3],
            args[2],
            args[4])

        print(cmd)
        os.system(cmd)

    else:
        cmd = "scp -r {}:{} {}".format(
            args[2],
            args[3],
            args[4])

        print(cmd)
        os.system(cmd)


username = os.environ['USER']

args = sys.argv
if len(args) != 5:
    print('usage: sftppy [method] [host] [source] [destination]')
    sys.exit()

if args[1] not in ['up', 'down', 'upr', 'downr']:
    print('method should be up, down, upr, or downr')
    sys.exit()

if args[3].find('/Users/{}'.format(username)) != -1:
    args[3] = args[3].replace('/Users/{}'.format(username), '~')

if args[4].find('/Users/{}'.format(username)) != -1:
    args[4] = args[4].replace('/Users/{}'.format(username), '~')

#main(args=args, username=username)
main_config(args=args, username=username)
