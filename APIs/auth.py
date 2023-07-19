import json
import requests
import os




class Auth:

  def __init__(self,url ):
        self.headers = {
        'Authorization': 'Bearer ' + bearerToken
    }
        self.tenant_url = url

        self.cookies = ""

        self.bearerToken = ""

        self.jwtToken = ""

        self.xcsrfToken = ""


        self.data = '''grant_type=password&username={}&password={}'''.format(
    '',
    ''
)



  def getBearerToken(self):
    base_url = self.tenant_url + "/basic/api/token"
    r = requests.post(base_url, data=self.data)
    # print(r.json())
    response = r.json()['access_token']
    global bearerToken
    bearerToken = response
    return bearerToken

  def getJwtToken(self):

      api='/api/rd/v1/Core/GenerateJWT'
      url=self.tenant_url + api
      headers = {"Authorization": "Bearer "+ self.getBearerToken()}
      r = requests.post(url, headers=headers)
      response = r.json()["token"]
      global jwtToken
      jwtToken=response
      return jwtToken

  def jwtLogin(self):
    api = "/api/rd/v1/Core/LoginJWT"
    url=self.tenant_url + api
    headers = {"Authorization": "Bearer "+ self.getJwtToken()}
    r = requests.post(url, headers=headers)
    global xcsrfToken
    xcsrfToken = r.json()
    global myCookies
    myCookies = r.cookies


