import jenkins
import getpass
from functools import reduce

import lib.logger as log
import lib.SSHconnector as SSH


class creator:

    def __init__(self, jenkins_host, username , stackname, token = None ):
        '''
        :param username: Jenkins Username
        :param password: Jenkins Token file if not entered prompt for password
        :param jenkins_host: Jenkins server
        '''

        self.username = username
        self.token = token
        self.jenkins_host = jenkins_host
        self.stackname = stackname

    def connect(self):

        '''

        Create a connection instance
        '''

        if self.token:
            password = self.token

        else:
            password = getpass.getpass('Jenkins password: ')

        self.server = jenkins.Jenkins(self.jenkins_host, username=self.username,\
                                      password=password)
        try:
            user = self.server.get_whoami()
            log.logs.info('Jenkins Login successful')
        except jenkins.JenkinsException as error_message:
            print(error_message)
            log.logs.error(error_message)

        #logging module
        version = self.server.get_version()


    def build_job(self, job_name, param):

        '''

        :param job_name: name of the jenkins job to build
        :param param: paramters to pass, most of my jobs are parameterized
        :return: returns the build number of that job
        '''

        build_number = self.server.get_job_info(job_name)['nextBuildNumber']

        # Can you this below job, but there will be multiple instance of same job running
        # so better to get the build number first.
        # server.get_job_info('api-test')['lastCompletedBuild']['number']

        log.logs.info('Build number {}'.format(build_number))
        log.logs.info('Starting the job name {}'.format(job_name))

        self.server.build_job(job_name, parameters = param)
        from time import sleep; sleep(60)

        print("Job started: Job name: {} and Build number {}".format(job_name, build_number))

        self.build_info(build_number)

    def build_info(self, build_number):

        '''

        :param build_number: Get the build number from build info job
        print success and failure factor
        '''

        build_info = self.server.get_build_info(build_number)
        job_name = self.dict_lookup(build_info, 'fullDisplayName')
        job_result = self.dict_lookup(build_info, 'result')

        log.logs.info('Job name {} and Job result {}'.format(job_name, job_result))

        if job_result == "Failure":
            print("The job {} failed, build number {}".format(job_name, build_number))
            log.logs.warn("The job {} failed, build number {}".format(job_name, build_number))

        print("Job started: Job name: {} and Job result {}".format(job_name, job_result))
        log.logs.info('Job name {} and Job result {}'.format(job_name, job_result))

    def aws_create_cluster(self):

        '''

        To create a cluster with name and region.
        '''

        job_name = "aws-deploy-cluster"
        param = {'STACKNAME': self.stackname, 'REGION': 'us-west-2', 'TERM': 10}
        self.build_job(job_name=job_name, param=param)

    def add_ssh_keys(self):

        '''

        create SSH keys and add it to the cluster by this job.
        '''

        job_name = "aws-add-keys"
        session = SSH.connector(self.username)
        session.create_keys()
        pub_key = session.create_connection()

        log.logs.info("SSH keys are created and transferred")

        param = {'STACKNAME': self.stackname, 'REGION': 'us-west-2', 'KEY': pub_key}
        self.build_job(job_name=job_name, param=param)

    def aws_terminate_cluster(self):

        '''

        create jenkins job which is to terminate a cluster expects only name of the stack
        '''

        job_name = "aws-terminate-cluster"

        param = {'STACKNAME': self.stackname}

        self.build_job(job_name=job_name, param=param)

    def add_ip(self):

        '''

        finds the public ip of the machine
        '''

        job_name = "aws-add-ip"
        pub_ip = SSH.connector(self.username).add_ip()

        #param = {'STACKNAME':'vivekharmony','IP':'49.205.52.37', 'REGION':'us-west-2'}

        param = {'STACKNAME': self.stackname, 'IP': pub_ip, 'REGION': 'us-west-2'}

        self.build_job(job_name=job_name, param=param)


    def dict_lookup(self, dictionary, *keys):

        '''

        :param dictionary: Nested dictionary
        :param keys: List of keys for lookup
        :return: returns the value looking for, safe method doesn't raise exception
        '''

        # similar to reduce(lambda x, y: x+y, range(1,101)) gives sum of all numbers 1 to 100

        return reduce(lambda dic, key: dic.get(key, None) if isinstance(dic, dict) else None, keys, dictionary)



