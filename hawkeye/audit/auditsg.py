#!/usr/bin/env python

import netaddr


class SecurityGroupAuditer(object):
    def __init__(self, sg):
        self.sg = sg
        self.port = 22  # SSH
        self.public_ip = '74.95.128.128'  # Example public comcast IP

    def audit_ssh(self):
        """Audit a security group to check for a rule allowing inbound traffic
        over port 22 from public internet IP addresses
        """
        result = {'version': 1,
                  'conforming': True}
        for rule in self.sg.rules:
            if int(rule.from_port) <= self.port <= int(rule.to_port):
                for grant in rule.grants:
                    if netaddr.IPAddress(self.public_ip) in netaddr.IPNetwork(
                                                              grant.cidr_ip):
                        result['conforming'] = False
        return result
