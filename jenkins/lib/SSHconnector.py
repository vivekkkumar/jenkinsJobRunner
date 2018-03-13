import paramiko
import subprocess
import time


import lib.logger as log


class connector:

    def __init__(self, username):

        '''
        :param username: needs a username to initialize
        '''

        self.username = username

    def add_ip(self):

        '''
        gets the public Ip address fromthe system

        :return: public ipaddress as string
        '''

        import shlex

        command = 'dig +short myip.opendns.com @resolver1.opendns.com'
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        output, error = process.communicate()
        try:

            ip_addr = output.strip().decode("utf-8")
        except NameError:

            print("Could not get the public IP address by dig command")
            log.logs.error("Could not get the public IP address by dig command")

        log.logs.info("Public IP created successfully")
        return ip_addr

    def create_keys(self):

        '''
        creates ssh keys and sends the keys to the test server I use. (This is my usecase)

        :return: [Public key , private key]
        '''

        from os import chmod
        from Crypto.PublicKey import RSA

        # https://stackoverflow.com/questions/2466401/how-to-generate-ssh-key-pairs-with-python

        # appending timestamp to get a unique name for each key pair file

        timestamp = time.time()
        self.private_key_file = "tmp/{}_private.key".format(timestamp)
        self.public_key_file = "tmp/{}_public.key".format(timestamp)

        key = RSA.generate(4096)
        with open(self.private_key_file, 'w') as content_file:
            chmod(self.private_key_file, 0o0600)                   # python 3.6 needs '0o' prefix for octal numbers.
            content_file.write(key.exportKey('PEM'))
        pubkey = key.publickey()
        with open(self.public_key_file, 'w') as content_file:
            content_file.write(pubkey.exportKey('OpenSSH'))

    def create_connection(self):

        '''
        put the ssh keys to the server to access the cluster from.
        :return: ssh public key path
        '''

        import getpass

        ssh = paramiko.SSHClient()

        # creating a ssh client
        # paramiko.ssh_exception.SSHException unknown host
        # setting this policy since we dont have a host key for connecting to this server.

        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # connect to the machine, getpass is like echo -e
            host = "Your host name"
            ssh.connect(host, username=self.username, password=getpass.getpass('password: '))

        except paramiko.ssh_exception.AuthenticationException:
            print ("SSH credentials authentication failed.")
            log.logs.error("SSH credentials authentication failed.")

        stdin, stdout, stderr = ssh.exec_command("pwd")
        user_dir = stdout.readlines().strip()                  # /home/vivekkumar\n

        sftp = ssh.open_sftp()

        if not sftp.stat(user_dir + "/keys_test/"):

            stdin, stdout, stderr = ssh.exec_command("mkdir keys_test")

            if stderr:
                log.logs.error("Could not create keys_test directory in the test machine")

            # sftp.chdir("keys_test")

        destination = user_dir + "/keys_test/"
        try:
            sftp.put(self.private_key_file, destination)
        except ImportError:
            log.logs.error("Could not access the Private SSH file")

        try:
            sftp.put(self.private_key_file, destination)
        except ImportError:
            log.logs.error("Could not access the Public SSH file")

        return self.private_key_file


