# Copyright 2023 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account, id_token
import requests, json
from google.protobuf.timestamp_pb2 import Timestamp

DL_API = 'https://datalineage.googleapis.com/v1'

def get_credentials(audience = "https://datalineage.googleapis.com"):
    METADATA_URL = 'http://metadata.google.internal/computeMetadata/v1/'
    METADATA_HEADERS = {'Metadata-Flavor': 'Google'}
    SERVICE_ACCOUNT = 'default'
    url = '{}instance/service-accounts/{}/token'.format(
        METADATA_URL, SERVICE_ACCOUNT)
    r = requests.get(url, headers=METADATA_HEADERS)
    r.raise_for_status()
    access_token = r.json()['access_token']
    return access_token
         
def isLineageSource(project_num, region, asset):
    url = '{0}/projects/{1}/locations/{2}:searchLinks'.format(DL_API, project_num, region)
    headers = {'Authorization' : 'Bearer ' + get_credentials()}
    payload = payload = {'source': {'fully_qualified_name': asset, 'location': region}}

    res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    
    if 'links' in res:
        links = res['links']
        return True
    else:
        return False

def isLineageTarget(project_num, region, asset):
    url = '{0}/projects/{1}/locations/{2}:searchLinks'.format(DL_API, project_num, region)
    headers = {'Authorization' : 'Bearer ' + get_credentials()}
    payload = {'target': {'fully_qualified_name': asset, 'location': region}}
    res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    if 'links' in res:
        return True
    else:
        return False