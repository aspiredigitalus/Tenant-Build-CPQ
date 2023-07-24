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
from DeployScripts.DeployGlobalScripts import DeployGlobalScripts
from DeployScripts.DeployCustomTemplates import DeployCustomTemplates
from DeployScripts.DeployUserTypes import DeployUserTypes
from UtilityScripts.CpqApiHelper import CpqApiHelper
from dotenv import load_dotenv
from UtilityScripts.DeployLogger import Log as log
import os


log.program_start()

try:
    load_dotenv('.env.deploy')
    load_dotenv('.env.secret')
except Exception:
    print('Environment Files not loaded')


def deploy():
    """
    Description: This is the driver method that
    calls listed scripts and deploys to CPQ
    via API calls.
    Parameters: None
    """

    try:
        api = CpqApiHelper(
            os.getenv('Cpq_Username'),
            os.getenv('Cpq_Password'),
            os.getenv('Cpq_Host')
        )
    except Exception as e:
        print(str(e))
        log.error("Error while loading CpqApiHelper")
        exit()

    deployScripts = populateDeployScripts()

    for script in deployScripts:
        try:
            script(api).run()
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
        deployScripts.append(DeployGlobalScripts)

    if util.transBoolEnv('CustomTemplates_run'):
        deployScripts.append(DeployCustomTemplates)

    if util.transBoolEnv('UserTypes_run'):
        deployScripts.append(DeployUserTypes)

    return deployScripts


deploy()