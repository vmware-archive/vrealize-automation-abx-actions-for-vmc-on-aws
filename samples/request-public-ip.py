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

def getNSXTproxy(org_id, sddc_id, sessiontoken):
    """ Gets the Reverse Proxy URL """
    myHeader = {'csp-auth-token': sessiontoken}
    myURL = "{}/vmc/api/orgs/{}/sddcs/{}".format(strProdURL,org_id, sddc_id)
    response = requests.get(myURL, headers=myHeader)
    json_response = response.json()
    proxy_url = json_response['resource_config']['nsx_api_public_endpoint_url']
    return proxy_url

def newSDDCPublicIP(proxy_url, sessiontoken, notes):
    """ Gets a new public IP for compute workloads. Requires a description to be added to the public IP."""
    myHeader = {"Content-Type": "application/json","Accept": "application/json", 'csp-auth-token': sessiontoken}
    proxy_url_short = proxy_url.rstrip("sks-nsxt-manager")
    myURL = (proxy_url_short + "cloud-service/api/v1/infra/public-ips/" + notes)
    json_data = {
    "display_name" : notes
    }
    print(json_data)
    response = requests.put(myURL, headers=myHeader, json=json_data)
    json_response_status_code = response.status_code
    print(json_response_status_code)
    return json_response_status_code
    
Refresh_Token = ""
ORG_ID = ""
SDDC_ID = ""
    
def handler(context, inputs):
    print('Create Public IP')
    notes    = inputs["notes"]
    session_token = getAccessToken(Refresh_Token)
    proxy = getNSXTproxy(ORG_ID, SDDC_ID, session_token)
    newSDDCPublicIP(proxy, session_token, notes)
