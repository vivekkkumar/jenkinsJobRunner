import argparse

import lib.JenkinsJobCreator as Jenkins

# create an argument parser with the below method call"

parser = argparse.ArgumentParser(description='Jenkins Job Creator tool')

# Adding required arguments

parser.add_argument("-n", "--stackname", type=str,
                    help="enter the stackname")

parser.add_argument("-a", "--action", type=str, choices=["create", "delete", "addIP", "addSSH"],
                    help="action to perform on the stack")

parser.add_argument('-u', type=str,
                    help='User name')

# since token is optional arguments.

parser.add_argument('-p', type=str,
                    action='store',
                    dest='token',
                    help='Token to access jenkins')

# creating an object to parse the arguments.

arguments = parser.parse_args()

stack_name = arguments.stackname

# Jenkins URL
jenkins_host = "https://Jenkins-host"

# Calling the implementation depending on token supplied.
if arguments.p:
    JenkObj = Jenkins.creator(jenkins_host, username=arguments.u, token=arguments.p, stackname=stack_name)

else:
    JenkObj = Jenkins.creator(jenkins_host, username=arguments.u, stackname=stack_name)

# Creating a connection object
JenkObj.connect()

# Creating appropriate objects depending on actions

if arguments.action == "create":
    JenkObj.aws_create_cluster()

if arguments.action == "delete":
    JenkObj.aws_terminate_cluster()

if arguments.action == "addIP":
    JenkObj.add_ip()

if arguments.action == "addSSH":
    JenkObj.add_ssh_keys()

# Calling the implementation.

