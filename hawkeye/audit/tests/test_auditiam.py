from audit.auditiam import IamPolicyAuditer
import unittest
import boto.iam
import urllib
import json


class IamTestCase(unittest.TestCase):

    def setUp(self):
        self.conn_iam = boto.iam.connect_to_region('universal')

    def get_example_policy(self):
        """Fetch the first policy from the first IAM group and return it in
        a format consumable by the auditers
        http://docs.aws.amazon.com/IAM/latest/UserGuide/PoliciesOverview.html
        """
        group_name = (self.conn_iam.get_all_groups()
                      ['list_groups_response']
                      ['list_groups_result']
                      ['groups']
                      [0]
                      ['group_name'])
        policy_name = (self.conn_iam.get_all_group_policies(group_name)
                       ['list_group_policies_response']
                       ['list_group_policies_result']
                       ['policy_names']
                       [0])
        policy = (self.conn_iam.get_group_policy(group_name, policy_name)
                  ['get_group_policy_response']
                  ['get_group_policy_result']
                  ['policy_document'])
        return json.loads(urllib.unquote(policy))

    def test_audit_s3_read(self):
        violating_obj1 = {"Statement": [{"Effect": "Allow",
                                         "Action": "*",
                                         "Resource": "*"}]}
        violating_obj2 = {"Statement": [{"Effect": "Allow",
                                         "Action": "s3:GetObject",
                                         "Resource": "*"}]}
        violating_obj3 = {"Statement": [{"Effect": "Allow",
                                         "Action": "s3:GetObject",
                                         "Resource": "arn:aws:s3:::*"}]}
        conforming_obj = {"Statement": [{"Effect": "Allow",
                                         "Action": "s3:GetObject",
                                         "Resource": "arn:aws:s3:::mybucket"}]}
        result = IamPolicyAuditer().audit_s3_read(violating_obj1)
        self.assertEqual(result['conforming'],
                         False,
                         "audit_s3_read did not report a policy violation as "
                         "it should have on *.*")

        result = IamPolicyAuditer().audit_s3_read(violating_obj2)
        self.assertEqual(result['conforming'],
                         False,
                         "audit_s3_read did not report a policy violation as "
                         "it should have on s3:GetObject.*")

        result = IamPolicyAuditer().audit_s3_read(violating_obj3)
        self.assertEqual(result['conforming'],
                         False,
                         "audit_s3_read did not report a policy violation as "
                         "it should have on s3:GetObject.arn:aws:s3:::*")

        result = IamPolicyAuditer().audit_s3_read(conforming_obj)
        self.assertEqual(result['conforming'],
                         True,
                         "audit_s3_read reported a policy violation when it "
                         "shouldn't have")


if __name__ == "__main__":
    unittest.main()