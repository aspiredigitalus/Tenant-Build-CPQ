# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployCustomTemplates
#   Type: Class
#   Author: Sufyan Pawaskar, David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Child Class of DeployScriptInterface, syncs repository
#   and tenant CustomTemplates, with optional delete.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployScriptInterface import DeployScriptInterface
from UtilityScripts.CpqApiHelper import CpqApiHelper
from UtilityScripts.DeployUtilities import DeployUtilities as util
from UtilityScripts.DeployLogger import Log as log
import json
import sys
import glob


class DeployCustomTemplates(DeployScriptInterface):

    def __init__(self, api: CpqApiHelper):
        self.api = api

    def __str__(self):
        return "DeployCustomTemplates"

    def run(self):
        """
        Description: This is the driver method that
        syncs CPQ tenant to repository.
        Parameters: None
        """
        customTemplateDict = {}
        allCustomTemplates = self.api.getAllCustomTemplates()

        for template in allCustomTemplates:
            customTemplateDict[template['systemId']] = template

        pathToJsonFiles = "Code/CustomTemplates/JsonFiles"

        filter = '*.json'
        if len(sys.argv) > 1:
            filter = f'{sys.argv[1]}.json'

        for file in glob.glob(pathToJsonFiles + filter):
            with open(file) as f:
                mainData = json.load(f)
            templateSystemId = mainData['systemId']

            # Adding the actual template from the path
            with open(mainData['content']) as templateFile:
                mainData['content'] = templateFile.read()                           
            # checking if the systemid is available in the system.
            if templateSystemId in customTemplateDict:
                apiData = customTemplateDict[templateSystemId]

                mainData["id"] = apiData['id']
                # deleting unnecessary keys.
                del (apiData["modifiedBy"])
                del (apiData["modifiedOn"])

                # update if the content doesn't matches with the CPQ template.
                if self.api.ordered(apiData) != self.api.ordered(mainData):
                    try:
                        self.api.updateCustomTemplate(
                            apiData["id"],
                            mainData
                        )
                        print(f">>CUSTOMTemplate>>UPDATE: {templateSystemId}")
                        log.info(f">>CUSTOMTemplate>>UPDATE:\
                                  {templateSystemId}")
                    except Exception as e:
                        print(str(e))
                        log.error(f">>CUSTOMTemplate>>ERROR: {templateSystemId}")
                else:
                    # This indicates that there is no change.
                    print(f">>CUSTOMTemplates>>IDENTICAL: {templateSystemId}")
                    log.info(f">>CUSTOMTemplates>>IDENTICAL:\
                              {templateSystemId}")
                # deleting the record.
                del customTemplateDict[templateSystemId]
            else:
                # This indicates that the systemId is not available in CPQ.
                # We will now add the custom Template to CPQ.
                try:
                    self.api.addCustomTemplate(mainData)
                    print(f">>CUSTOMTemplate>>ADD: {templateSystemId}")
                    log.info(f">>CUSTOMTemplate>>ADD: {templateSystemId}")
                except Exception as e:
                    print(str(e))
                    log.error(f">>CUSTOMTemplate>>ADD ERROR:\
                               {templateSystemId}")
        if util.transBoolEnv('CUSTOM_TEMPLATES_DELETE'):
            # Constrain delete action to .env.deploy boolean
            for record in customTemplateDict.values():
                try:
                    self.api.deleteCustomTemplate(
                        record['id']
                    )
                    print(
                        f">>CUSTOMTemplate>>DELETE:  {record['systemId']}"
                    )
                    log.info(
                        f">>CUSTOMTemplate>>DELETE:  {record['systemId']}"
                    )
                except Exception as e:
                    print(str(e))
                    log.error(
                        f">>CUSTOMTemplate>>DELETE:  {record['systemId']}"
                    )
