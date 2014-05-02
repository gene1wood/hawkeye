from audit.auditsg import SecurityGroupAuditer
import unittest
import boto.ec2.securitygroup
import boto.iam


class SshTestCase(unittest.TestCase):

    def setUp(self):
        self.conn_ec2 = boto.ec2.connect_to_region('us-west-2')
        self.conn_iam = boto.iam.connect_to_region('universal')
        self.account_id = (self.conn_iam.get_user()['get_user_response']
                           ['get_user_result']['user']['arn'].split(':')[4])

    def get_sg(self, port, ip):
        sg = boto.ec2.securitygroup.SecurityGroup(
              connection=self.conn_ec2,
              owner_id=self.account_id,
              name='test-security-group',
              description='Test security group',
              id='sg-12345678'
              )
        sg.add_rule(
            ip_protocol='tcp',
            from_port=port,
            to_port=port,
            src_group_name='groupy',
            src_group_owner_id='12345',
            cidr_ip=ip,
            src_group_group_id='54321',
            dry_run=False
        )
        return sg

    def test_audit_ssh(self):
        sg_allow_inbound_public_ssh = self.get_sg(22, '0.0.0.0/0')
        auditer = SecurityGroupAuditer(sg_allow_inbound_public_ssh)
        result = auditer.audit_ssh()
        self.assertEqual(result['conforming'],
                         False,
                         "audit_ssh did not report a policy violation as it "
                         "should have")

        sg_deny_inbound_public_ssh = self.get_sg(22, '10.0.0.0/8')
        auditer = SecurityGroupAuditer(sg_deny_inbound_public_ssh)
        result = auditer.audit_ssh()
        self.assertEqual(result['conforming'],
                         True,
                         "audit_ssh reported a policy violation when it "
                         "shouldn't have")

    def fetch_security_groups(self):
        return self.conn_ec2.get_all_security_groups()

if __name__ == "__main__":
    unittest.main()