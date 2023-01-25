import xml.etree.ElementTree as ET
import os
from docusign_esign.client.api_client import ApiClient
from config import DemoEnvironment as tst
from config import ProductionEnvironment as prd
from config import output


def get_access_token(environment: str):

    if environment in ['tst']:

        token_response = ApiClient.request_jwt_user_token(self=ApiClient(),
                                                          client_id=tst.iss,
                                                          user_id=tst.sub,
                                                          oauth_host_name=tst.aud,
                                                          private_key_bytes=tst.private_key,
                                                          expires_in=3600,
                                                          scopes=tst.scope)

        access_token = getattr(token_response, 'access_token')

        return access_token

    if environment in ['prd']:
        token_response = ApiClient.request_jwt_user_token(self=ApiClient(),
                                                          client_id=prd.iss,
                                                          user_id=prd.sub,
                                                          oauth_host_name=prd.aud,
                                                          private_key_bytes=prd.private_key,
                                                          expires_in=3600,
                                                          scopes=prd.scope)

        access_token = getattr(token_response, 'access_token')

        return access_token


def post_xml(filename: str, environment: str,  access_token: str):
## TODO: if Junk in XML format, catch and send it
    os.chdir(output)

    with open(f'{filename}', 'r') as xml:
        root = ET.fromstring(xml.read())

    xml_string = ET.tostring(root).decode('iso-8859-5')

    body = {
        "Name": "Integration Workflow",
        "StartDate": "",
        "EndDate": "",
        "Status": "",
        "Info": "",
        "Params": f"{xml_string}",
        "WorkflowDocuments": {
          "Items": [
            "Document"
          ],
          "Href": "",
          "Offset": 0,
          "Limit": 0,
          "First": "",
          "Previous": "",
          "Next": "",
          "Last": "",
          "Total": 0
        },
        "Href": ""
      }

    header = {'Content-Type': 'application/json', 'Accept': 'application/xml', 'Authorization': f'Bearer {access_token}'}

    if environment in ['tst']:
        workflow_url = f'https://apiuatna11.springcm.com/v2/{tst.ds_account_id}/workflows'

    if environment in ['prd']:
        workflow_url = f'https://apina11.springcm.com/v2/{prd.ds_account_id}/workflows'

    response = ApiClient.request(self=ApiClient(), method='POST', url=workflow_url, headers=header, body=body)

    return response


if __name__ == "__main__":
    print('@ DocuSignAPI.py')
    # access_token = get_access_token(environment='prd')
    # response = post_xml(filename='ASEN_5859.xml', environment='tst', access_token=access_token)
    # print(f'Status: {response.status} {response.reason}\n Body: {response.data.decode("utf-8")}')
