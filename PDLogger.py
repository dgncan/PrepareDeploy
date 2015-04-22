__author__ = 'dcan'

import logging

""" logger  """

class PDLogger:
    def __init__(self):
        self.log_file_path = "PrepareDeploy.log"

        self.mylogger = logging.getLogger("PrepareDeploy")
        self.mylogger.setLevel(logging.DEBUG)

        self.handler_screen = logging.StreamHandler()
        self.handler_file   = logging.FileHandler(self.log_file_path)

        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

        self.handler_screen.setFormatter(formatter)
        self.handler_file.setFormatter(formatter)


    def write_log_file(self,msg):
        self.mylogger.addHandler(self.handler_file)
        self.mylogger.error(msg)

    def write_log_screen(self,msg):
        self.mylogger.addHandler(self.handler_screen)
        self.mylogger.debug(msg)
