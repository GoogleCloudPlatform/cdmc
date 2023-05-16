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

from google.cloud import bigquery
from google.cloud import datacatalog_v1

def getTableLocation(asset):
    table_id = extractTableId(asset)
    client = bigquery.Client()
    table = client.get_table(table_id)
    return table.location

def getPolicyTagInfo(tag_name):
    client = datacatalog_v1.PolicyTagManagerClient()
    request = datacatalog_v1.GetPolicyTagRequest(
        name=tag_name,
    )
    policy_tag = client.get_policy_tag(request=request)
    return policy_tag.display_name

def getTablePolicyTagsDict(asset):
    table_dict = {}
    table_id = extractTableId(asset)
    client = bigquery.Client()
    table = client.get_table(table_id)
    for field in table.schema:
        if(field.policy_tags != None):
            table_dict[field.name.upper()]=getPolicyTagInfo(field.policy_tags.names[0]).upper() 
    return table_dict

def extractTableId(asset):
    projectId = asset[(asset.find( "/projects/" ) + len( "/projects/")):asset.find( "/datasets/" )]
    dataset = asset[(asset.find( "/datasets/" ) + len( "/projects/")):asset.find( "/tables/" )]
    table = asset[(asset.find( "/tables/" ) + len( "/tables/")):len(asset)+1]
    return (projectId + "." + dataset + "." + table)

def queryTable(project_id, dataset, query_file):
    client = bigquery.Client()
    query = ""
    with open(query_file) as f:
        query = f.read()
    return client.query(query.replace("$project_id",project_id).replace("$dataset",dataset))

def getBQAssets(source_project_id,source_region):
# Define the source and destination datasets
    client = bigquery.Client()
    # Define the query
    query_string = """
                SELECT CONCAT(table_catalog,".",table_schema,".",table_name) as asset_name
                FROM `$project_id.region-$source_region.INFORMATION_SCHEMA.TABLES`
            """.replace("$project_id",source_project_id).replace("$source_region",source_region)

    # Execute the query
    resultset = client.query(query_string)
    result_list = []
    for row in resultset:
        result_list.append(row["asset_name"])

    return result_list
