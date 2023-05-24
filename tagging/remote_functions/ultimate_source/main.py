# Copyright 2022-2023 Google, LLC.
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

import google.auth.transport.requests
from google.oauth2 import service_account

import base64, requests, json, os

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

def process_request(request):
        
    request_json = request.get_json()
    print('request_json:', request_json)
    
    project_id = request_json['calls'][0][0].strip()
    print('project_id:', project_id)
    
    project_num = request_json['calls'][0][1]
    print('project_num:', project_num)
    
    region = request_json['calls'][0][2].strip()
    print('region:', region)
    
    dataset = request_json['calls'][0][3].strip()
    print('dataset:', dataset)
    
    table = request_json['calls'][0][4].strip()
    print('table:', table)
    
    table = 'bigquery:' + project_id + '.' + dataset + '.' + table
    print('table: ', table)
    
    ultimate_source = get_source_links(table, project_num, region)
    print('ultimate_source:', ultimate_source)
    
    return json.dumps({"replies": [ultimate_source]})


def get_credentials_from_environment():

    secret = os.getenv('SECRET')
    service_account_info = json.loads(secret)
    credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
     
    return credentials.token
    

def get_source_links(target, project_num, region):

    api = 'https://' + region + '-datalineage.googleapis.com/v1'
    url = '{0}/projects/{1}/locations/{2}:searchLinks'.format(api, project_num, region)
    headers = {'Authorization' : 'Bearer ' + get_credentials_from_environment()}
    payload = {'target': {'fully_qualified_name': target, 'location': region}}

    res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    print(res)

    if 'links' in res:
        for link in res['links']:
            if target == link['source']['fullyQualifiedName']:
                return target
            else:
                print('Target:', target, '<- Source:', link['source']['fullyQualifiedName'])
                return get_source_links(link['source']['fullyQualifiedName'], project_num, region)
    else:
        return target         
