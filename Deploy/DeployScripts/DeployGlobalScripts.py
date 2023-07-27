# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployGlobalScripts
#   Type: Class
#   Author: David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Child Class of DeployScriptInterface, syncs repository
#   and tenant GlobalScripts, with optional delete.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployScriptInterface import DeployScriptInterface
from UtilityScripts.CpqApiHelper import CpqApiHelper
from UtilityScripts.DeployUtilities import DeployUtilities as util
from UtilityScripts.DeployLogger import Log as log
import json
import sys
import glob


class DeployGlobalScripts(DeployScriptInterface):

    def __init__(self, api: CpqApiHelper):
        self.api = api

    def __str__(self):
        return "DeployGlobalScripts"

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
                mainData['scriptDefinition']['script'] = scriptFile.read()\
                    .replace("\r\n", "\n")

            # Check if script shares systemId
            if scriptSystemId in globalScriptDict:

                apiData = globalScriptDict[scriptSystemId]

                # Add product level events to each set()
                apiEvents = set()
                for apiEvent in apiData['events']:
                    if apiEvent['systemEventId'] not in self.api.systemEvenIds:
                        apiEvents.add(apiEvent['systemEventId'])
                mainEvents = set()
                for mainEvent in mainData['events']:
                    if mainEvent['systemEventId'] not in self.api.systemEvenIds:
                        mainEvents.add(mainEvent['systemEventId'])

                # Remove events that exist on GIT but not CPQ.
                # Cannot add an event in this way, will throw error
                onlyInMain = mainEvents - apiEvents
                mainData['events'] = [e for e in mainData['events']
                                      if e['systemEventId'] not in onlyInMain]

                # append events that exist only on CPQ
                onlyInApi = apiEvents - mainEvents
                for apiEvent in apiData['events']:
                    if apiEvent['systemEventId'] in onlyInApi:
                        mainData['events'].append(apiEvent)

                # if the event exists in both environments, do nothing.

                mainData["scriptDefinition"]["id"] = \
                    apiData['scriptDefinition']['id']

                # delete unnecessary fields for comparison
                del (apiData["scriptDefinition"]["modifiedBy"])
                del (apiData["scriptDefinition"]["modifiedOn"])
                del (apiData["scriptDefinition"]["isCSRFProtected"])
                del (apiData["scriptDefinition"]["modifiedByFullName"])

                # Update if the json is different in CPQ
                if self.api.ordered(apiData) != self.api.ordered(mainData):
                    try:
                        self.api.updateGlobalScript(
                            apiData['scriptDefinition']['id'],
                            mainData
                        )
                        print(f">>GlobalScript>>UPDATE: {scriptSystemId}")
                        log.info(f">>GlobalScript>>UPDATE: {scriptSystemId}")
                    except Exception as e:
                        print(str(e))
                        log.error(f">>GlobalScript>>UPDATE: {scriptSystemId}")
                else:
                    print(f">>GLOBALScripts>>IDENTICAL: {scriptSystemId}")
                    log.info(f">>GLOBALScripts>>IDENTICAL: {scriptSystemId}")
                del globalScriptDict[scriptSystemId]

            else:
                # This means that the systemId was not found in CPQ
                # We will add the code to CPQ
                try:
                    # Remove events that are not system level
                    # Cannot create a global script with product level events

                    mainData['events'] = [e for e in mainData['events']
                        if e['systemEventId'] in self.api.systemEventIds]

                    self.api.addGlobalScript(mainData)
                    print(f">>GLOBALScripts>>ADD: {scriptSystemId}")
                    log.info(f">>GLOBALScripts>>ADD: {scriptSystemId}")
                except Exception as e:
                    print(str(e))
                    log.error(f">>GLOBALScripts>>ADD: {scriptSystemId}")

        if util.transBoolEnv('GLOBAL_SCRIPTS_DELETE'):
            # Constrain delete action to .env.deploy boolean
            for record in globalScriptDict.values():
                try:
                    self.api.deleteGlobalScript(
                        record['scriptDefinition']['id']
                    )
                    print(
                        f">>GLOBALScripts>>DELETE:  {record['scriptDefinition']['systemId']}"
                    )
                    log.info(
                        f">>GLOBALScripts>>DELETE:  {record['scriptDefinition']['systemId']}"
                    )
                except Exception as e:
                    print(str(e))
                    log.error(
                        f">>GLOBALScripts>>DELETE:  {record['scriptDefinition']['systemId']}"
                    )
