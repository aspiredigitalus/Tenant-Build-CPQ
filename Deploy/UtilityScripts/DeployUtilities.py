# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployUtilities
#   Type: Script
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Collection of Static Methods that contain
#   useful and repeated code.
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from decouple import config
import os


class DeployUtilities:

    @staticmethod
    def transBoolEnv(envKey: str):
        """
        Description: Access .env file Keys and
        converts the string to boolean returns.
        Parameters:
            - (str): .env key
        """
        try:
            envInput = os.getenv(envKey)
        except Exception:
            print('Error accessing key: {}'.format(envKey))
            envInput = None
        return True if envInput == "True" else False