#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import inspect

from ruamel import yaml
from subprocess import check_output

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(DIR, '../')))

from utils.json import jsonify
from utils.version import version
from main import app

def test_version():
    '''
    expect:
        version: git describe
    '''
    expect = dict(version=version)
    client = app.test_client()
    client.testing = True
    result = client.get('/autocert/version')
    assert result.status_code == 200
    actual = jsonify(result.get_data().decode('utf-8'))
    assert expect == actual
