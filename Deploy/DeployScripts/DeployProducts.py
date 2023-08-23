# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployProducts
#   Type: Class
#   Author: Lucas Yepez
#   Copyright: Aspire Digital
#   Purpose: Child Class of DeployproductInterface, syncs repository
#   and tenant Products, with optional delete.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployScriptInterface import DeployScriptInterface
from UtilityScripts.CpqApiHelper import CpqApiHelper
from UtilityScripts.DeployUtilities import DeployUtilities as util
from UtilityScripts.DeployLogger import Log as log
import json
import sys
import glob


class DeployProducts(DeployScriptInterface):

    def __init__(self, api: CpqApiHelper):
        self.api = api

    def __str__(self):
        return "DeployProducts"

    def run(self):
        """
        Deproduction: This is the driver method that
        syncs CPQ tenant to repository.
        Parameters: None
        """

        # Get dict for All Products, save by SystemID

        ProductsDict = {}
        allProducts = self.api.getAllProducts()

        for product in allProducts:
            ProductsDict[product['systemId']] = product

        pathToJsonFiles = "Code/Products/"

        filter = '*.json'
        if len(sys.argv) > 1:
            filter = f'{sys.argv[1]}.json'

        for file in glob.glob(pathToJsonFiles + filter):
            with open(file) as f:
                mainData = json.load(f)
            productSystemId = mainData['systemId']



            # Check if product shares systemId
            if productSystemId in ProductsDict:

                apiData = ProductsDict[productSystemId]




                # delete unnecessary fields for comparison
                del (apiData["modifiedBy"])
                del (apiData["modifiedDate"])


                # Update if the json is different in CPQ
                if self.api.ordered(apiData) != self.api.ordered(mainData):

                    try:

                        self.api.deleteProducts(
                            apiData['id']
                        )

                        self.api.addProduct(mainData)

                        print(f">>Products>>UPDATE: {productSystemId}")
                        log.info(f">>Products>>UPDATE: {productSystemId}")
                    except Exception as e:
                        print(str(e))
                        log.error(f">>Products>>UPDATE: {productSystemId}")
                else:
                    print(f">>Products>>IDENTICAL: {productSystemId}")
                    log.info(f">>Products>>IDENTICAL: {productSystemId}")
                del ProductsDict[productSystemId]

            else:
                # This means that the systemId was not found in CPQ
                # We will add the code to CPQ
                try:

                    print("add")

                    self.api.addProduct(mainData)
                    print(f">>Products>>ADD: {productSystemId}")
                    log.info(f">>Products>>ADD: {productSystemId}")
                except Exception as e:
                    print(str(e))
                    log.error(f">>Products>>ADD: {productSystemId}")

        if util.transBoolEnv('PRODUCTS_DELETE'):
            # Constrain delete action to .env.deploy boolean
            for record in ProductsDict.values():

                try:
                    allProducts = self.api.getAllProducts()
                    for product in allProducts:

                        if product['name'] == record['name']:

                            self.api.deleteProducts(
                                product['id']
                            )
                    print(
                        f">>Products>>DELETE:  {record['systemId']}"
                    )
                    log.info(
                        f">>Products>>DELETE:  {record['systemId']}"
                    )
                except Exception as e:
                    print(str(e))
                    log.error(
                        f">>Products>>DELETE:  {record['systemId']}"
                    )
