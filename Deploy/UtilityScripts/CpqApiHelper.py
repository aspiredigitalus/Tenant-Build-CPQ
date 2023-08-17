# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployUtilities
#   Type: Class
#   Author: Aspire Dev Team
#   Copyright: Aspire Digital
#   Purpose: A Class that holds all crud operation API calls
#           and other useful methods for sorting data.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from UtilityScripts.DeployLogger import Log as log
import requests
import json


class CpqApiHelper:

    __username = ""
    __password = ""
    __host = ""

    __tokens = {
        'bearerToken': '',
        'jwtToken': '',
        'xcsrfToken': '',
        'cookies': ''
    }

    __jwtBearerBreakPoint = 600

    systemEvenIds = [
        1,
        2,
        3,
        17,
        18,
        19,
        34,
        37,
        41,
        49,
        50,
        51,
        52,
        53,
        54,
        56
    ]

    def __init__(self, username: str, password: str, host: str):
        """
        Description: Constructor to take in auth data
                    and save to private variables
        Parameters:
                    (str): username
                    (str): password
                    (str): host url to prepend api url snippet.
        """
        if not username or not password or not host:
            raise Exception("Exception: Credentials not passed to CpqApiHelper")
        self.__username = username
        self.__password = password
        self.__host = host

        self.getTokens()

    # GLOBAL SCRIPT APIS

    def getAllGlobalSCripts(self):
        api = "/api/script/v1/globalscripts"
        url = self.__host + api
        headers = self.getHeaderBearer()
        response = self.testCallSuccess(
            requests.get,
            url,
            headers=headers
        )
        return response.json()['pagedRecords']

    def updateGlobalScript(self, id, package):
        api = "/api/script/v1/globalscripts/" + str(id)
        url = self.__host + api
        headers = self.getHeaderBearer(contentType=True)
        response = self.testCallSuccess(
            requests.put,
            url,
            data=json.dumps(package),
            headers=headers
        )
        return response

    def addGlobalScript(self, package):
        api = "/api/script/v1/globalscripts"
        url = self.__host + api
        headers = self.getHeaderBearer(contentType=True)
        response = self.testCallSuccess(
            requests.post,
            url,
            data=json.dumps(package),
            headers=headers
        )
        return response

    def deleteGlobalScript(self, id):
        api = "/api/script/v1/globalscripts/" + str(id)
        url = self.__host + api
        headers = self.getHeaderBearer()
        response = self.testCallSuccess(
            requests.delete,
            url,
            headers=headers
        )
        return response

    # Custom Table APIS

    def getAllCustomTables(self):
        headers = self.getHeaderJwt()
        headers["Content-Type"] = "application/json"
        headers["accept"] = "*/*"
        url = self.__host + "api/custom-table/v1/customTables"
        # tables = requests.get(url, headers=headers)
        tables= self.testCallSuccess(
            requests.get,
            url,
            headers=headers
        )

        if tables.status_code == 200:
            tables_data = tables.json()
            return tables_data["pagedRecords"]

    def updateCustomTables(self, table_name, payload):
        data = payload
        headers = self.getHeaderJwt()
        headers["Content-Type"] = "application/json"
        tableName = table_name
        url = self.__host+ f"api/custom-table/v1/customTables/{tableName}"
        tables= self.testCallSuccess(
            requests.patch,
            url,
            headers=headers,
            data=json.dumps(data)
        )

        return tables

    def addCustomTables(self, mainData):
        headers = self.getHeaderJwt()
        headers["Content-Type"] = "application/json"
        data = mainData
        url = self.__host + "api/custom-table/v1/customTables"

        response= self.testCallSuccess(
            requests.post,
            url,
            headers=headers,
            data=json.dumps(data)
        )

        if response.status_code == 201:
            response_data = response.json()
            print("Response:", response_data)
            return response_data

    def deleteCustomTables(self, name):
        headers = self.getHeaderJwt()
        tableName=name
        url = self.__host + f"api/custom-table/v1/customTables/{tableName}"
        deleted_table= self.testCallSuccess(
            requests.delete,
            url,
            headers=headers
        )

    # UTILITY METHODS

    def testCallSuccess(self, func, url, data='', params='', headers=''):
        response = func(url, data=data, params=params, headers=headers)
        if response.status_code == 403:
            self.getTokens()
            if len(str(headers)) > self.__jwtBearerBreakPoint:
                headers = self.getHeaderBearer()
            elif headers != '':
                headers = self.getHeaderJwt()
            else:
                headers = ''
            response = func(url, data=data, params=params, headers=headers)
            if not response.ok:
                raise Exception(
                    "Failed Login Second Attempt: " + str(response.json())
                )
            return response
        elif not response.ok:
            raise Exception(
                "Failed Login First Attempt: " + str(response.json())
            )

        return response

    def getHeaderBearer(
        self,
        contentType: bool = False,
        acceptAll: bool = False
    ):
        """
        Summary: Standard method for returning
        headers with Bearer Token

        Args:
            contentType (bool, optional): Defaults to False.
            acceptAll (bool, optional): Defaults to False.

        Returns:
            (dict): Packaged Header
        """
        headerResponse = {}
        headerResponse['Authorization'] = \
            'Bearer ' + self.__tokens['bearerToken']
        if contentType:
            headerResponse['Content-Type'] = 'application/json'
        if acceptAll:
            headerResponse['accept'] = '*/*'
        return headerResponse

    def getHeaderJwt(
        self,
        contentType: bool = False,
        acceptAll: bool = False
    ):
        """
        Summary: Standard method for returning
        headers with Bearer Token

        Args:
            contentType (bool, optional): Defaults to False.
            acceptAll (bool, optional): Defaults to False.

        Returns:
            (dict): Packaged Header
        """
        headerResponse = {}
        headerResponse['Authorization'] = \
            'Bearer ' + self.__tokens['jwtToken']
        if contentType:
            headerResponse['Content-Type'] = 'application/json'
        if acceptAll:
            headerResponse['accept'] = '*/*'
        return headerResponse

    def ordered(self, obj):
        """
        Orders or structures lists and dict so that
        they can be compared.

        Parameters:
            (dict|list): object to be ordered

        Returns: Ordered object of same type
        """
        if isinstance(obj, dict):
            return sorted((k, self.ordered(v)) for k, v in obj.items())
        if isinstance(obj, list):
            return sorted(self.ordered(x) for x in obj)
        else:
            return obj

    def getTokens(self):
        """
        Description: Method to get an populate tokens
                    dict.
        Parameters: None
        """

        log.info("[API Login Flow - Getting Tokens]")

        api = "/basic/api/token"
        url = self.__host + api
        body = """grant_type=password&username={}&password={}""".format(
            self.__username,
            self.__password
        )
        response = requests.get(url, data=body)
        self.__tokens['bearerToken'] = response.json()['access_token']

        # Get JWT Tokens
        api = "/api/rd/v1/Core/GenerateJWT"
        url = self.__host + api
        headers = {
            'Authorization': 'Bearer ' + self.__tokens['bearerToken']
        }
        response = requests.post(url, headers=headers)
        self.__tokens['jwtToken'] = response.json()['token']

        # Get X-CSRF Tokens and Cookies
        api = "/api/rd/v1/Core/LogInJWT"
        url = self.__host + api
        headers = {
            'Authorization': 'Bearer ' + self.__tokens['jwtToken']
        }
        response = requests.post(url, headers=headers)
        self.__tokens['xcsrfToken'] = response.json()
        self.__tokens['cookies'] = response.cookies

        print('Bearer Token -> [SAVED]\n')

        print('JWT Token -> [SAVED]\n')

        print('X-CSRF Token -> [SAVED]\n')

        print('Cookies -> [SAVED]\n')

