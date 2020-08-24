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

def newSDDCnetworks(proxy_url, sessiontoken, display_name, gateway_address, dhcp_range, domain_name, routing_type):
    """ Creates a new SDDC Network. """
    myHeader = {"Content-Type": "application/json","Accept": "application/json", 'csp-auth-token': sessiontoken}
    myURL = (proxy_url + "/policy/api/v1/infra/tier-1s/cgw/segments/" + display_name)
    json_data = {
        "subnets":[{"dhcp_ranges":[dhcp_range],
        "gateway_address":gateway_address}],
        "type":routing_type,
        "display_name":display_name,
        "domain_name":domain_name,
        "advanced_config":{"connectivity":"ON"},
        "id":display_name
         }
    response = requests.put(myURL, headers=myHeader, json=json_data)
    json_response_status_code = response.status_code
    if json_response_status_code == 200 :
        print("The network " + display_name + " has been created.")
    else :
        print("There was an error. Try again.")
        return
    
Refresh_Token = ""
ORG_ID = ""
SDDC_ID = ""
    
def handler(context, inputs):
    print('Create Network')
    display_name    = inputs["Name"]
    gateway_address = inputs["Gateway"]
    dhcp_range      = inputs["Range"]
    routing_type    = inputs["Type"]
    domain_name    = inputs["Domain name"]
    session_token = getAccessToken(Refresh_Token)
    proxy = getNSXTproxy(ORG_ID, SDDC_ID, session_token)
    newSDDC = newSDDCnetworks(proxy, session_token, display_name, gateway_address, dhcp_range, domain_name, routing_type)
    print(newSDDC)
