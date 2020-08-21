# VRA ABX ACTION TO ADD HOST TO VMC

################################################################################
### Copyright (C) 2019-2020 VMware, Inc.  All rights reserved.
### SPDX-License-Identifier: BSD-2-Clause
################################################################################

import requests                         # need this for Get/Post/Delete
import json

strProdURL = "https://vmc.vmware.com"

def getAccessToken(myKey):
    params = {'refresh_token': myKey}
    headers = {'Content-Type': 'application/json'}
    response = requests.post('https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize', params=params, headers=headers)
    jsonResponse = response.json()
    access_token = jsonResponse['access_token']
    return access_token
    
def addCDChosts(sddc, hosts, tenantid, sessiontoken):
    myHeader = {'csp-auth-token': sessiontoken}
    myURL = strProdURL + "/vmc/api/orgs/" + tenantid + "/sddcs/" + sddc + "/esxs"
    strRequest = {"num_hosts": hosts}
    response = requests.post(myURL, json=strRequest, headers=myHeader)
    print("result =" + str(response.status_code))
    jsonResponse = response.json()
    strSDDC = jsonResponse['id']
    return(strSDDC)

Refresh_Token = ""
ORG_ID = ""
SDDC_ID = ""
    
def handler(context, inputs):
    numHosts    = inputs["number_hosts"]
    sessiontoken = getAccessToken(Refresh_Token)
    addCDChosts(SDDC_ID, numHosts, ORG_ID, sessiontoken)
