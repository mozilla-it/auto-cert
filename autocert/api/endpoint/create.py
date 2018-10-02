#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
autocert.create
'''

import os

from pprint import pformat
from attrdict import AttrDict
from datetime import timedelta

from endpoint.base import EndpointBase
from exceptions import AutocertError
from config import CFG
from utils.fmt import *
from utils import pki
from app import app

class UnknownCertificateAuthorityError(AutocertError):
    def __init__(self, authority):
        message = fmt('unknown certificate authority: {authority}')
        super(UnknownCertificateAuthorityError, self).__init__(message)

class CreateEndpoint(EndpointBase):
    def __init__(self, cfg, args):
        super(CreateEndpoint, self).__init__(cfg, args)

    def execute(self):
        status = 201
        modhash, key, csr = pki.create_modhash_key_and_csr(
            self.args.common_name,
            public_exponent=CFG.key.public_exponent,
            key_size=CFG.key.key_size,
            key=self.args.key,
            csr=self.args.csr,
            oids=self.cfg.csr.oids,
            sans=self.args.sans)
        crt, expiry, authority = self.authority.create_certificate(
            self.args.organization_name,
            self.args.common_name,
            self.args.validity_years,
            csr,
            self.args.bug,
            list(self.args.sans),
            self.args.repeat_delta,
            self.args.whois_check)
        cert = self.tardata.create_cert(
            self.args.common_name,
            modhash,
            key,
            csr,
            crt,
            self.args.bug,
            list(self.args.sans),
            expiry,
            authority)
        if self.args.destinations:
            note = 'bug ' + bug
            for name, dests in self.args.destinations.items():
                cert = self.destinations[name].install_certificates(note, [cert], *dests)[0]
        json = self.transform([cert])
        return json, status
