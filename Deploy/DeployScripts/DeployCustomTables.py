# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployCustomTables
#   Type: Class
#   Author: Lucas Yepez
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
        allCustomTables = self.api.getAllCustomTables()
        for table in allCustomTables:
            customTableDict[table['tableName']] = table
        pathToJsonFiles = "Code/CustomTables/"
        filter = '*.json'
        if len(sys.argv) > 1:
            filter = f'{sys.argv[1]}.json'
        for file in glob.glob(pathToJsonFiles + filter):
            with open(file) as f:
                mainData = json.load(f)
            tableName = mainData['tableName']

            # Check if script shares systemId
            if tableName in customTableDict:

                apiData = customTableDict[tableName]


                # delete unnecessary fields for comparison
                del (apiData["modifiedBy"])
                del (apiData["modifiedAt"])

                # Update if the json is different in CPQ
                if self.api.ordered(apiData) != self.api.ordered(mainData):

                    try:
                        self.api.updateCustomTables(
                            apiData['tableName'],
                            mainData
                        )
                        log.info(f">>Custom Table>>UPDATE: {tableName}")
                        print(f">>Custom Table>>UPDATE: {tableName}")
                    except Exception as e:
                        log.error(f">>Custom Table>>UPDATE: {tableName}")
                else:
                    log.info(f">>Custom Table>>IDENTICAL: {tableName}")
                del customTableDict[tableName]

            else:
                # This means that the table name was not found in CPQ
                # We will add the code to CPQ
                try:
                    mainData['tableName'] = tableName
                    self.api.addCustomTables(mainData)
                    print(f">>Custom Tables>>ADD: {tableName}")
                    log.info(f">>Custom Tables>>ADD: {tableName}")
                except Exception as e:
                    print(str(e))
                    log.error(f">>Custom Tables>>ADD: {tableName}")

        if util.transBoolEnv('CUSTOM_TABLES_DELETE'):
            # Constrain delete action to .env.deploy boolean

            for record in customTableDict.values():
                try:
                    self.api.deleteCustomTables(
                        record['tableName']
                    )
                    print(
                        f">>Custom Tables>>DELETE:  {record['tableName']}"
                    )
                    log.info(
                        f">>Custom Tables>>DELETE:  {record['tableName']}"
                    )
                except Exception as e:
                    print(str(e))
                    log.error(
                        f">>Custom Tables >>DELETE:  {record['tableName']}"
                    )
