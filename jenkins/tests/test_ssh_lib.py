import unittest
import lib.SSHconnector as SSH


# Test cases always should perform
# Arrange - creating = objects and dependencies etc,
# Act - implementing functionality,
# Assert - make claims like pass or fail.

# Note these tests does not test the actual API and is used to test my implementation.

class test_SSH(unittest.TestCase):                      # subclass unittest mandatory

    def setUp(self):
        '''Fixture for creating an instance which will be used by all the methods in this class'''

        username = "Vivek"
        self.testObj = SSH.connector(username)

    def test_add_ip(self):                               # name of the test case
        '''Checking the exception handling in send_message method'''

        #check validaity of the IP

        with self.assertRaises(Exception) as test_message:
            ip_addr = self.tesObj.add_ip()

        self.assertTrue("NameError", test_message.exception)

    def test_create_connection(self):                               # name of the test case
        '''Checking the exception handling in send_message method'''

        # enter wrong password

        with self.assertRaises(Exception) as test_message:
            self.tesObj.create_connection()

        self.assertTrue("Permission denied", test_message.exception)

if __name__ == '__main__':
    unittest.main()

