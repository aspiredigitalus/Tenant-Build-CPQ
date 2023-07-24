# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Name: DeployUtilities
#   Type: Class
#   Author: Lucas Yepez & David Mehoves
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
        headers = self.getHeaderBearer()
        headers['Content-Type'] = 'application/json'
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
        headers = self.getHeaderBearer()
        headers['Content-Type'] = 'application/json'
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

    def getHeaderBearer(self):
        return {
            'Authorization': 'Bearer ' + self.__tokens['bearerToken']
        }

    def getHeaderJwt(self):
        return {
            'Authorization': 'Bearer ' + self.__tokens['jwtToken']
        }

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
        
        
        # Get Bearer Tokens
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

        print('Bearer Token')
        print(self.__tokens['bearerToken'] + "\n")

        print('JWT Token')
        print(self.__tokens['jwtToken'] + "\n")

        print('X-CSRF Token')
        print(self.__tokens['xcsrfToken'] + "\n")

        print('Cookies')
        print(str(self.__tokens['cookies'].get_dict()) + "\n")
