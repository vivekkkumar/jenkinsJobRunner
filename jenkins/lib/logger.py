import logging
import os

class logs:

    def __init__(self):
        file_name = os.path.expanduser("~") + '/jenkins_log'

        # handler in appending mode

        logging.basicConfig(filename=file_name, level=logging.DEBUG)
        self.logger = logging.getLogger('Jenkins Script Tool Logger')
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def returnLogger(self):
        '''

        :return: returns logger object with the above configuration
        '''
        return self.logger
