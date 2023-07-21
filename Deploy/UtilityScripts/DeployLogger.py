# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployLogger
#   Type: Class
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Custom Logger to produce .txt files (used for CI/CD Pipeline)
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import datetime
import sys
import os


class Log:

    @staticmethod
    def info(message):
        """
        Description: General log messages
        Parameters:
            - (str): log message
        """
        timestamp = str(datetime.datetime.now())
        log_message = timestamp + " ~+~ " + message + "\n"
        with open('Deploy/Deploy_Log.txt', 'a') as f:
            f.write(log_message)
            f.close()

    @staticmethod
    def error(message):
        """
        Description: Placed inside an except block,
        produces stack trace as well as passing through
        message.
        Parameters:
            - (str): log message
        """
        spacer = "                               "
        timestamp = str(datetime.datetime.now())
        log_message = timestamp + " ~+~ " + message + "\n"
        exc_info = sys.exc_info()
        line_num = exc_info[2].tb_lineno
        file = os.path.split(exc_info[2].tb_frame.f_code.co_filename)[1]
        error_msg = exc_info[1]
        with open('Deploy/Deploy_Log.txt', 'a') as f:
            f.write(log_message)
            f.write(spacer + "Line Number: " + str(line_num) + "\n")
            f.write(spacer + "File: " + str(file) + "\n")
            f.write(spacer + "Error: " + str(error_msg) + "\n")
            f.close()

    @staticmethod
    def program_start():
        """
        Description: Identifies start of pipeline
        in the log.
        Parameters: none
        """
        with open('Deploy/Deploy_Log.txt', 'a') as f:
            f.write("\n\n>>>>>>>>>>>       Deploy Pipeline Start       <<<<<<<<<<<<<<<<\n\n")
            f.close()