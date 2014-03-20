#!/usr/bin/env python2
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import boto.ec2
import boto.ec2.elb
import boto.vpc
import boto.iam
import boto.rds
import boto.route53
import boto.s3
from boto.exception import EC2ResponseError,BotoServerError


# Note:  This is a class because it's intended to have some more functionality later.
class HawkeyeScrape:

    def __init__(self,key_id,access_key,logger):
        """ Take our API keys, return ourself """
        self._key_id = key_id
        self._access_key = access_key
        self._logger = logger

    def _query_api(self,region,api,conn,method):
        """ Call boto, and catch known errors! """
        ret = None
        try:
            ret = getattr(conn,method)()

        # ToDo:  Add more granularity to error handling
        # Why were we blocked from quering?
        except EC2ResponseError, e:
            self._logger.debug(str([method, api.__name__, e]))
        except BotoServerError, e:
            self._logger.debug(str([method, api.__name__, e]))
        return ret

    def _get_all_get_all(self, conn):
        """ Return all relevant get_all_* methods, not including what we don't want """
        ret = []
        for  method in dir(conn):
            if method not in self._boto_do_not_query:
                if method.startswith('get_all_'):
                    ret.append(method)
        return ret


    # Iterate through all regions - query all data available
    def fetch_all(self):
        """ Iterate through all regions
            Iterate through all supported API's
            Iterate through all supported get_all calls
            return array of boto objects.
            Profit!"""
        ret = []
        for region in boto.ec2.regions():
            if "name" in dir(region): # some regions are not built-out yet
                for api in self._boto_apis:
                    conn = api.connect_to_region(region.name,aws_access_key_id=self._key_id,aws_secret_access_key=self._access_key)
                    for method in self._get_all_get_all(conn):
                        ret.append(self._query_api(region,api,conn,method))
        return ret

    # Here's the API's we're gonna query
    _boto_apis = [
        boto.ec2,
        boto.ec2.elb,
        boto.vpc,
        boto.rds,
        boto.iam,
        boto.route53,
        boto.s3,
        ]

    # These are the get_all functions we don't want to get right now.
    _boto_do_not_query = [
        # These provide too much information with little value
        # ToDo: use individual queries to get the images/kernels we need
        "get_all_images",
        "get_all_kernels",
        # This might be too much information for now, investigate later
        "get_all_snapshots",
        # These all require additional options
        # Todo:  Write individual queries for them later.
        "get_all_access_keys",
        "get_all_group_policies",
        "get_all_mfa_devices",
        "get_all_user_policies",
        "get_all_dbparameters",
        "get_all_rrsets",
        "get_all_lb_attributes",
        # These are depreciated, do not use.
        "get_all_vmtypes",
        "get_all_logs",
        "get_all_instance_types",
        # This does not work in all regions
        # ToDo: write exception handler so we can use it.
        "get_all_placement_groups",
        ]
