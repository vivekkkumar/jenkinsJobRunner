# jenkinsJobRunner
I use this tool to create jenkins jobs in my environment but the job creator module can be applied to any jenkins job.
I have 4 jenkins jobs

1. is to create a cluster in my test environment
2. To Add Ip address to the cluster for outside access
3. To Add SSH keys by generating them locally and add it to my test machine. So I can access the cluster from my test machine.
4. To delete the instance.

Usage:

$ python main.py --h
usage: main.py [-h] [-n STACKNAME] [-a {create,delete,addIP,addSSH}] [-u U]
               [-p TOKEN]

Jenkins Job Creator tool

optional arguments:
  -h, --help            show this help message and exit
  -n STACKNAME, --stackname STACKNAME
                        enter the stackname
  -a {create,delete,addIP,addSSH}, --action {create,delete,addIP,addSSH}
                        action to perform on the stack
  -u U                  User name
  -p TOKEN              Token to access jenkins
  
  
To Run the tests:

python tests/test_jenkins_lib.py
python tests/test_ssh_lib.py

But since I had changed the environments the tests would fail. 
