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

import requests


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

    def __init__(self, username: str, password: str, host: str):
        """
        Description: Constructor to take in auth data 
                    and save to private variables
        Parameters:
                    (str): username
                    (str): password
                    (str): host url to prepend api url snippet.
        """
        self.__username = username
        self.__password = password
        self.__host = host

        self.getTokens()

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

    def getTokens(self):
        """
        Description: Method to get an populate tokens
                    dict.
        Parameters: None
        """

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
