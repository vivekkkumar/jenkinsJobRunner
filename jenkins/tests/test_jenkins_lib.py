import unittest
import lib.JenkinsJobCreator as Jenkins


# Test cases always should perform
# Arrange - creating = objects and dependencies etc,
# Act - implementing functionality,
# Assert - make claims like pass or fail.

# Note these tests does not test the actual API and is used to test my implementation.

class test_jenkins(unittest.TestCase):           # subclass unittest mandatory

    def setUp(self):
        '''Fixture for creating an instance which will be used by all the methods in this class'''
                                                    # if setup fails tear down will not be called. This case doesn't need tear down
                                                    # since all the objects are destroyed by python anyway
        url = "https://localhost:8080"
        username = 'vivekkumar'
        password="token"
        stack_name = "test"
        self.testObj = Jenkins.creator(url, username, stack_name, password)

    def test_connect_url(self):                                        # name of the test case
        '''Connect method input inavlid URL'''

        self.testObj.url = "http://unreacheable"
        with self.assertRaises(Exception) as test_message:
            self.testObj.connect()

        self.assertTrue("Host unreachable", test_message.exception)

    def test_connect_usr(self):
        '''Connect method input invalid credentials'''

        self.testObj.username = "invalid"
        with self.assertRaises(Exception) as test_message:
            self.testObj.connect()

        self.assertTrue("Permission denied", test_message.exception)

    def test_connect_pass(self):
        '''Connect method input invalid password'''

        self.testObj.token = None
        with self.assertRaises(Exception) as test_message:
            self.testObj.connect()

        self.assertTrue("Permission denied", test_message.exception)

    def test_jobs(self):
        '''Connect method input invalid params'''

        self.testObj.job_name = "aws-create-cluster"
        self.testObj.param = {'STACKNAME': self.stackname, 'REGION': 'us-west-2'}       # Missing term param here.
        self.build_job(job_name=self.testObj.job_name, param=self.testObj.param)
        with self.assertRaises(Exception) as test_message:
            self.testObj.aws_create_cluster()

        self.assertTrue('Find da', test_message.exception)

if __name__ == '__main__':
    unittest.main()
