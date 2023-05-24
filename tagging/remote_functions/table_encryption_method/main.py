#!/usr/bin/python
#
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.cloud import kms_v1
from google.cloud import bigquery
import base64
import json

BIGQUERY_REGION = 'us-central1'

def event_handler(request):
    
    request_json = request.get_json()
    print('request_json:', request_json)
    
    project = request_json['calls'][0][0].strip()
    dataset = request_json['calls'][0][1].strip()
    table = request_json['calls'][0][2].strip()
    
    print('project:', project)
    print('dataset:', dataset)
    print('table:', table)
    
    try:
        encryption_type = get_encryption_type(project, dataset, table)
        print('encryption_type:', encryption_type)
        print('replies:', {"replies": [encryption_type]})
        return json.dumps({"replies": [encryption_type]})
    
    except Exception as e:
        print("Exception caught: " + str(e))
        return json.dumps({"errorMessage": str(e)}), 400


def get_encryption_type(project, dataset, table):
    
    key_string = None
    
    try:
        query = "select option_value from " + dataset + ".INFORMATION_SCHEMA.TABLE_OPTIONS where table_name = '" + table + "' and option_name = 'kms_key_name'"
        bq_client = bigquery.Client(project=project, location=BIGQUERY_REGION)
        rows = bq_client.query(query).result()
            
        for row in rows:
            key_string = row['option_value']
    
    except Exception as e:
        print('Error occurred while querying Information Schema:', e)
    
    if key_string:
        print('table uses cmek encryption')
        key_name = key_string.replace('/cryptoKeyVersions/', '')[1:-2]
        encryption_type = get_cmek_level(key_name)
    else:
        print('table uses default encryption')
        encryption_type = 'Default'
    
    print('encryption_type:', encryption_type)
    
    return encryption_type


def get_cmek_level(key_name):
    
    encryption_type = None
    
    client = kms_v1.KeyManagementServiceClient()

    request = kms_v1.GetCryptoKeyRequest(
        name=key_name,
    )

    crypto_key = client.get_crypto_key(request=request)
    print(crypto_key.primary.protection_level)
    
    if crypto_key.primary.protection_level == kms_v1.types.ProtectionLevel.HSM:
        encryption_type = 'CMEK+HSM'
    
    if crypto_key.primary.protection_level == kms_v1.types.ProtectionLevel.SOFTWARE:
        encryption_type = 'CMEK'
    
    return encryption_type    
    

if __name__ == '__main__':
    project = 'sdw-conf-b1927e-bcc1'
    dataset = 'scratch_space'
    table = 'cmek_hsm_table' # can be cmek_hsm_table, cmek_table, or default_table
    encryption_type = get_encryption_type(project, dataset, table)
    print('encryption_type:', encryption_type)
