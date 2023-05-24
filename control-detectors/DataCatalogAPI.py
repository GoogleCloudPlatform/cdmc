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

from google.cloud import datacatalog_v1
from google.protobuf.json_format import MessageToDict

def getColumnTagDict(asset, tag_template_name,tag_display_name, data_type):
    table_dict = {}
    client = datacatalog_v1.DataCatalogClient()
    tagrequest = datacatalog_v1.ListTagsRequest(parent=asset,page_size=1000)
    response_tags = client.list_tags(request=tagrequest)
    for item in response_tags.tags:
        if(item.column):
            tag_name = MessageToDict(item._pb)                  
            for field in tag_name["fields"]:
                if(field == tag_template_name):                    
                    if data_type == "boolValue":
                        table_dict[item.column.upper()]=tag_name["fields"][tag_template_name][data_type]
                    else:
                        if data_type == "stringValue":
                            table_dict[item.column.upper()]=tag_name["fields"][tag_template_name][data_type].upper()
                        else:
                            table_dict[item.column.upper()]=tag_name["fields"][tag_template_name][data_type]["displayName"].upper()
    return table_dict

def getTableTagValue(asset,tag_template_name,tag_display_name, value_type):
    client = datacatalog_v1.DataCatalogClient()
    tagrequest = datacatalog_v1.ListTagsRequest(parent=asset)
    response_tags = client.list_tags(request=tagrequest)
    for item in response_tags.tags:
        if(item.template==tag_template_name):
            return MessageToDict(item._pb)["fields"][tag_display_name][value_type]


def searchCatalogAssets(org_id, proj_id, filter):
    datacatalog = datacatalog_v1.DataCatalogClient()
    project_id = proj_id
    # [START data_catalog_search_assets]
    scope = datacatalog_v1.types.SearchCatalogRequest.Scope()
    #scope.include_project_ids.append(project_id)
    scope.include_org_ids.append(org_id)
    search_results = datacatalog.search_catalog(scope=scope, query="projectId:" + project_id + " "+ filter)
    return search_results

def getCatalogAssetTags(org_id,proj_id,entry):
    scope = datacatalog_v1.types.SearchCatalogRequest.Scope()
    datacatalog = datacatalog_v1.DataCatalogClient()
    project_id = proj_id
    client = datacatalog_v1.DataCatalogClient()
    asset = client.lookup_entry({"linked_resource": entry})
    tagrequest = datacatalog_v1.ListTagsRequest(parent=asset.name)
    tags = client.list_tags(request=tagrequest)
    return tags
