# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployQuoteTables
#   Type: Class
#   Author: Anoosha Syed
#   Copyright: Aspire Digital
#   Purpose: Child Class of DeployScriptInterface, syncs repository
#   and tenant Quote Tables, with optional delete.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployScriptInterface import DeployScriptInterface
from UtilityScripts.CpqApiHelper import CpqApiHelper
from UtilityScripts.DeployLogger import Log as log
import json
import sys
import glob

class DeployQuoteTables(DeployScriptInterface):

    def __init__(self, api: CpqApiHelper):
        self.api = api

    def __str__(self):
        return "DeployQuoteTables"

    def run(self):
        """
        Description: This is the driver method that
        syncs CPQ tenant to repository.
        Parameters: None
        """
        quoteTableDict = {}
        allQuoteTables = self.api.getAllQuoteTables()
        
        for quoteTable in allQuoteTables:
            quoteTableDict[quoteTable['id']] = quoteTable


        pathToJsonFiles = 'Code/QuoteTables/'

        filter = '*.json'
        if len(sys.argv) > 1:
            filter = f'{sys.argv[1]}.json'


        for file in glob.glob(pathToJsonFiles + filter):
            with open(file) as f:
                mainData = json.load(f)
            quoteTableId = mainData['id']


            # Check if product shares systemId
            if quoteTableId in quoteTableDict:

                apiData = quoteTableDict[quoteTableId]

                # Update if the json is different in CPQ
                if self.api.ordered(apiData) != self.api.ordered(mainData):

                    try:

                        self.api.deleteQuoteTable(
                            apiData['id']
                        )

                        self.api.addQuoteTable(mainData)

                        print(f">>Quote Table>>UPDATE: {quoteTableId}")
                        log.info(f">>Quote Table>>UPDATE: {quoteTableId}")
                    except Exception as e:
                        print(str(e))
                        log.error(f">>Quote Table>>UPDATE: {quoteTableId}")
                else:
                    print(f">>Quote Table>>IDENTICAL: {quoteTableId}")
                    log.info(f">>Quote Table>>IDENTICAL: {quoteTableId}")
                del quoteTableDict[quoteTableId]

            else:
                # This means that the systemId was not found in CPQ
                # We will add the code to CPQ
                try:

                    print("add")

                    self.api.addQuoteTable(mainData)
                    print(f">>Quote Table>>ADD: {quoteTableIdd}")
                    log.info(f">>Quote Table>ADD: {quoteTableId}")
                except Exception as e:
                    print(str(e))
                    log.error(f">>Quote Table>>ADD: {quoteTableId}")


         if util.transBoolEnv('QUOTE_TABLES_DELETE'):
            # Constrain delete action to .env.deploy boolean
            for record in quoteTableDict.values():

                try:
                    allQuoteTables = self.api.getAllQuoteTables()
                    for quoteTable in allQuoteTables:

                        if quoteTable['name'] == record['name']:

                            self.api.deleteQuoteTable(
                                quoteTable['id']
                            )
                    print(
                        f">>Quote Table>>DELETE:  {record['id']}"
                    )
                    log.info(
                        f">>Quote Table>>DELETE:  {record['id']}"
                    )
                except Exception as e:
                    print(str(e))
                    log.error(
                        f">>Quote Table>>DELETE:  {record['id']}"
                    )