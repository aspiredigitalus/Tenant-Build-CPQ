# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: Deploy
#   Type: Script
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Script to deploy repository to tenant
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from UtilityScripts.DeployUtilities import DeployUtilities as util
from DeployScripts.GlobalScripts import GlobalScripts
from DeployScripts.CustomTemplates import CustomTemplates
from DeployScripts.UserTypes import UserTypes
from DeployScripts.CustomTables import CustomTables

def deploy():
    """
    Description: This is the driver method that
    calls listed scripts and deploys to CPQ
    via API calls.
    Parameters: None
    """
    deployScripts = populateDeployScripts()

    for script in deployScripts:
        try:
            script().run()
        except Exception as e:
            print("Exception: " + str(e))


def populateDeployScripts():
    """
    Description: Adds listed scripts to List()
    based on .env file True/False decelerations.
    Parameters: None
    """
    deployScripts = []

    if util.transBoolEnv('GlobalScripts_run'):
        deployScripts.append(GlobalScripts)

    if util.transBoolEnv('CustomTemplates_run'):
        deployScripts.append(CustomTemplates)

    if util.transBoolEnv('UserTypes_run'):
        deployScripts.append(UserTypes)

    if util.transBoolEnv('CustomTables_run'):
        deployScripts.append(CustomTables)

    return deployScripts


deploy()
