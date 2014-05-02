class IamPolicyAuditer(object):

    def __init__(self):
        pass

    def check_wildcard(self, haystacks, needle):
        result = False
        if type(haystacks) == str:
            haystacks = [haystacks]
        for haystack in haystacks:
            if '*' in haystack:
                if haystack.index('*') != len(haystack) - 1:
                    # this is an illegal syntax because the wildcard character
                    # is not the last character in the string
                    pass  # maybe raise an exception here
                else:
                    result = (result or
                              needle[:len(haystack) - 1] ==
                              haystack[:len(haystack) - 1])
            else:
                result = result or needle == haystack
        return result

    def audit_s3_read(self, policy):
        """Audit an IAM policy to detect if it allows reading s3 objects from
        multiple buckets
        """
        result = {'version': 1,
                  'conforming': True}
        policy = [policy] if type(policy) == dict else policy
        for statements in [x['Statement'] for x in policy]:
            for statement in statements:
                if (statement['Effect'] == 'Allow' and
                        self.check_wildcard(statement['Action'],
                                            's3:GetObject') and
                        self.check_wildcard(statement['Resource'],
                                            'arn:aws:s3:::')):
                    result['conforming'] = False
        return result
