# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: Custom Tables
#   Type: Class
#   Author: Lucas Yepez
#   Copyright: Aspire Digital
#   Purpose: Child Class of DeployScriptInterface, syncs repository
#   and tenant CustomTables, with optional delete.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployScriptInterface import DeployScriptInterface


class CustomTables(DeployScriptInterface):

    def run(self):
        """
        Description: This is the driver method that
        syncs CPQ tenant to repository.
        Parameters: None
        """
        print("Deploying custom Tables")
