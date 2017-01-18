#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
cli.create
'''

import json
import requests

from cli.utils.output import output
from cli.transform import transform
from cli.parsers import verbose_parser

AUTHORITIES = [
    'digicert',
    'letsencrypt',
]

def add_parser(subparsers):
    parser = subparsers.add_parser('create', parents=[verbose_parser])
    parser.add_argument(
        'common_name',
        metavar='common-name',
        help='common name')
    parser.add_argument(
        '-a', '--authority',
        metavar='AUTH',
        default=AUTHORITIES[0],
        choices=AUTHORITIES,
        help='default="%(default)s"; choose which authority to use')
    parser.add_argument(
        '-s', '--sans',
        nargs='+',
        help='default="%(default)s"; add additional sans')

    parser.set_defaults(func=do_create)

def do_create(ns):
    json = {
        'common_name': ns.common_name,
        'authority': ns.authority,
        'sans': ns.sans,
        'verbosity': ns.verbosity,
    }
    response = requests.post(ns.api_url / 'auto-cert', json=json)
    if response.status_code == 201:
        certs = response.json()['certs']
        xformd = transform(certs, ns.verbosity)
        output(xformd)
        return
    else:
        print(response)
        print(response.text)
    raise Exception('wtf do_create')

