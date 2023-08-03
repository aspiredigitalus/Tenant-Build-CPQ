# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployCustomTables
#   Type: Class
#   Author: Lucas Yepez & David Mehoves
#   Copyright: Aspire Digital
#   Purpose: Child Class of DeployScriptInterface, syncs repository
#   and tenant CustomTable, with optional delete.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployScriptInterface import DeployScriptInterface
from UtilityScripts.CpqApiHelper import CpqApiHelper
from UtilityScripts.DeployUtilities import DeployUtilities as util
from UtilityScripts.DeployLogger import Log as log
import json
import sys
import glob


class DeployCustomTables(DeployScriptInterface):

    def __init__(self, api: CpqApiHelper):
        self.api = api

    def __str__(self):
        return "DeployCustomTables"

    def run(self):
        """
        Description: This is the driver method that
        syncs CPQ tenant to repository.
        Parameters: None
        """

        # Get dict for All Custom Tables, save by SystemID

        customTableDict = {}
        allcustomTables = self.api.getAllCustomTables()
        for table in allcustomTables:
            customTableDict[table['scriptDefinition']['systemId']] = table

        pathToJsonFiles = "Code/CustomTables/"

        filter = '*.json'
        if len(sys.argv) > 1:
            filter = f'{sys.argv[1]}.json'

        for file in glob.glob(pathToJsonFiles + filter):
            with open(file) as f:
                mainData = json.load(f)
            tableSystemId = mainData['scriptDefinition']['systemId']

            # swap location for code
            with open(mainData['scriptDefinition']['script']) as tableFile:
                mainData['scriptDefinition']['script'] = tableFile.read()\
                    .replace("\r\n", "\n")

            # Check if script shares systemId
            if tableSystemId in customTableDict:

                apiData = customTableDict[tableSystemId]

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
                        self.api.updateCustomTables(
                            apiData['scriptDefinition']['id'],
                            mainData
                        )
                        print(f">>CustomTable>>UPDATE: {tableSystemId}")
                        log.info(f">>CustomTable>>UPDATE: {tableSystemId}")
                    except Exception as e:
                        print(str(e))
                        log.error(f">>CustomTable>>UPDATE: {tableSystemId}")
                else:
                    print(f">>CustomTables>>IDENTICAL: {tableSystemId}")
                    log.info(f">>CustomTables>>IDENTICAL: {tableSystemId}")
                del customTableDict[tableSystemId]

            else:
                # This means that the systemId was not found in CPQ
                # We will add the code to CPQ
                try:
                    # Remove events that are not system level
                    # Cannot create a global script with product level events

                    mainData['events'] = [e for e in mainData['events']
                        if e['systemEventId'] in self.api.systemEventIds]

                    self.api.addCustomTables(mainData)
                    print(f">>CustomTables>>ADD: {tableSystemId}")
                    log.info(f">>CustomTables>>ADD: {tableSystemId}")
                except Exception as e:
                    print(str(e))
                    log.error(f">>CustomTables>>ADD: {tableSystemId}")

        if util.transBoolEnv('CUSTOM_TABLES_DELETE'):
            # Constrain delete action to .env.deploy boolean
            for record in customTableDict.values():
                try:
                    self.api.deleteCustomTables(
                        record['scriptDefinition']['id']
                    )
                    print(
                        f">>CustomTables>>DELETE:  {record['scriptDefinition']['systemId']}"
                    )
                    log.info(
                        f">>CustomTables>>DELETE:  {record['scriptDefinition']['systemId']}"
                    )
                except Exception as e:
                    print(str(e))
                    log.error(
                        f">>CustomTables>>DELETE:  {record['scriptDefinition']['systemId']}"
                    )
