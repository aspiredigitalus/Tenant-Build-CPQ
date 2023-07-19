# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: UserTypes
#   Type: Class
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Child Class of DeployScriptInterface, syncs repository
#   and tenant GlobalScripts, with optional delete.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployScriptInterface import DeployScriptInterface
from UtilityScripts.CpqApiHelper import CpqApiHelper
import os, json, sys, glob, copy


class GlobalScripts(DeployScriptInterface):

    def __init__(self, api: CpqApiHelper):
        self.api = api

    def run(self):
        """
        Description: This is the driver method that
        syncs CPQ tenant to repository.
        Parameters: None
        """

        # Get dict for All Global Scripts, save by SystemID

        globalScriptDict = {}
        allGlobalScripts = self.api.getAllGlobalSCripts()
        for script in allGlobalScripts:
            globalScriptDict[script['scriptDefinition']['systemId']] = script

        print(str(globalScriptDict))

        pathToJsonFiles = "Code/GlobalScripts/"

        filter = '*.json'
        if len(sys.argv) > 1:
            filter = f'{sys.argv[1]}.json'

        for file in glob.glob(pathToJsonFiles + filter):
            with open(file) as f:
                mainData = json.load(f)
            scriptSystemId = mainData['scriptDefinition']['systemId']

            # swap location for code
            with open(mainData['scriptDefinition']['script']) as scriptFile:
                mainData['scriptDefinition']['script'] = scriptFile \
                    .read().replace("\r\n", "\n")

            print("\n\n")
            print(str(mainData))
