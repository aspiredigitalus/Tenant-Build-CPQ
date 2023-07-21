import datetime
import sys
import os


class Log:

    @staticmethod
    def info(message):
        timestamp = str(datetime.datetime.now())
        log_message = timestamp + " ~+~ " + message + "\n"
        with open('Deploy/Deploy_Log.txt', 'a') as f:
            f.write(log_message)
            f.close()

    @staticmethod
    def error(message):
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
        with open('Deploy/Deploy_Log.txt', 'a') as f:
            f.write("\n\n>>>>>>>>>>>       Deploy Pipeline Start       <<<<<<<<<<<<<<<<\n\n")
            f.close()