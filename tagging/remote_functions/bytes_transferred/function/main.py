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

from __future__ import print_function
from google.cloud import bigquery
import base64
import json

DATA_TRANSFER_LOG_TABLE = 'sdw-conf-b1927e-bcc1.bigquery_log_sink.bigquerydatatransfer_googleapis_com_transfer_config'
LAST_30_DAYS = ('(select date(year, month, 01) from (select extract(year from current_date) as year,' 
               ' extract(month from current_date) as month))')

BIGQUERY_PROJECT = 'sdw-conf-b1927e-bcc1' # this is the destination project in which the audit logs reside
                                          # we are attributing egress charges to the destination project

bq_client = bigquery.Client(project=BIGQUERY_PROJECT)

def event_handler(request):
    request_json = request.get_json()
    #print('request_json:', request_json)
    
    mode = request_json['calls'][0][0].strip()
    project = request_json['calls'][0][1].strip()
    dataset = request_json['calls'][0][2].strip()
    table = request_json['calls'][0][3].strip()
    
    try:
        if mode == 'bytes':
            physical_bytes_sum = run(mode, project, dataset, table)
            print('physical_bytes_sum:', physical_bytes_sum)
            return json.dumps({"replies": [physical_bytes_sum]})
        
        elif mode == 'cost':
            egress_charges = run(mode, project, dataset, table)
            print('egress_charges:', egress_charges)
            return json.dumps({"replies": [egress_charges]})
        
        else:
            print('Error: invalid mode', mode)
            return json.dumps({"errorMessage": 'invalid mode'})
            
    
    except Exception as e:
        print("Exception caught: " + str(e))
        return json.dumps({"errorMessage": str(e)}), 400


def run(mode, project, dataset, table):
    
    print('Running in {} mode'.format(mode))
    
    physical_bytes_sum = 0
    
    # get the region for the dataset where the destination table resides
    location = bq_client.get_dataset(project + '.' + dataset).location
    #print('location:', location) 
    
    # are there any data transfer jobs that have written into this table
    jobs_exist_sql = ('select resource.labels.config_id from {}'   
                    ' where date(timestamp) >= {}' 
                    ' and resource.labels.location = "{}"'
                    ' and resource.type = "bigquery_dts_config" ' 
                    ' and jsonPayload.message like "%(table {}) completed successfully."'.format(DATA_TRANSFER_LOG_TABLE,
                                                                                          LAST_30_DAYS, location, table))
    #print('jobs_exist_sql:', jobs_exist_sql)
    
    rows = list(bq_client.query(jobs_exist_sql).result())
    
    if len(rows) == 0:
        print('Table {} has not been copied into'.format(table))
        return 0
    
    # table has been copied into
    for row in rows:
        config_id = row[0]
        print('config_id:', config_id)
        
        src_sql = ('select jsonPayload.message from {}'   
                   ' where resource.labels.config_id = "{}"' 
                   ' and jsonPayload.message like "%Identified % tables to copy in the source dataset%"' 
                   ' and date(timestamp) >= {}'   
                   ' and resource.type = "bigquery_dts_config"').format(DATA_TRANSFER_LOG_TABLE, config_id, LAST_30_DAYS)
        
        #print(src_sql)
        
        row = list(bq_client.query(src_sql).result())
        
        if len(row) == 0:
            print('Error: missing source details')
            return -1
        
        json_payload_split = row[0][0].split(' ')
        src_project_dataset = json_payload_split[9].strip()
        src_region = json_payload_split[12].strip()
        #print('src_project_dataset:', src_project_dataset)
        #print('src_region:', src_region)
        
        # copy within same region -> no egress 
        if src_region == location:
            print('Copy within same region, no egress charges')
            return 0
        
        # cross-region copy, use physical bytes of table to estimate egress 
        phys_bytes_sql = ('select total_physical_bytes from `{}`.`region-{}`.INFORMATION_SCHEMA.TABLE_STORAGE_BY_PROJECT ' 
                         'where table_schema = "{}" and table_name = "{}"').format(project, location, dataset, table)

        row = list(bq_client.query(phys_bytes_sql).result())
        
        if len(row) == 0:
            print('Error: missing physical bytes')
            return -1
        
        physical_bytes_sum += row[0][0]
        print('{} bytes were transferred'.format(row[0][0]))
        #print('physical_bytes_sum =', physical_bytes_sum)
        
    if mode == 'bytes':
        return physical_bytes_sum
    if mode == 'cost':   
        return calculate_egress(location, src_region, physical_bytes_sum)
    else:
        print('Error: invalid mode')
        return -1
    
        
def calculate_egress(location, src_region, physical_bytes_sum):
    
    if location[0:2] == src_region[0:2]:
        # source and destination are both in same continent
        egress_usd = round((physical_bytes_sum / (1024 * 1024 * 1024)) * 0.01, 4)
    else:
        # source and destination are NOT in same continent
        egress_usd = round((physical_bytes_sum / (1024 * 1024 * 1024)) * 0.08, 4)
    
    return egress_usd