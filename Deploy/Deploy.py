# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: Deploy
#   Type: Script
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Script to deploy repository to tenant
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from UtilityScripts.DeployScriptInterface import DeployScriptInterface
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
    load_dotenv('.env.deploy', override=True)
    load_dotenv('.env.secret', override=False)
except Exception:
    print('Environment Files not loaded')


def deploy():
    """
    Description: This is the driver method that
    calls listed scripts and deploys to CPQ
    via API calls.
    Parameters: None
    """
    instClass = None

    try:
        api = CpqApiHelper(
            os.getenv('CPQ_USERNAME'),
            os.getenv('CPQ_PASSWORD'),
            os.getenv('CPQ_HOST')
        )
    except Exception as e:
        print(str(e))
        log.error("Error while loading CpqApiHelper")
        exit()

    deployScripts = populateDeployScripts()

    for script in deployScripts:
        try:
            instClass = script(api)

            # Log Deploy Script Start
            log.info(f"[Pipeline - {instClass}]")
            print(f"[Pipeline - {instClass}]")

            # Run Script Function
            instClass.run()
        except Exception as e:
            if instClass:
                print(f"Exception in {instClass}: " + str(e))
            else:
                print("Exception: " + str(e))


def populateDeployScripts():
    """
    Description: Adds listed scripts to List()
    based on .env file True/False decelerations.
    Parameters: None
    """
    deployScripts = []

    if util.transBoolEnv('GLOBAL_SCRIPTS_RUN'):
        deployScripts.append(DeployGlobalScripts)

    if util.transBoolEnv('CUSTOM_TEMPLATES_RUN'):
        deployScripts.append(DeployCustomTemplates)

    if util.transBoolEnv('USER_TYPES_RUN'):
        deployScripts.append(DeployUserTypes)

    return deployScripts


deploy()
