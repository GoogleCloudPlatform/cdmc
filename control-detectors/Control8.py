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

from pubsub_handler import publishPubSubAvro
from DataCatalogAPI import searchCatalogAssets, getColumnTagDict
from BigQueryAPI import getTablePolicyTagsDict, queryTable, extractTableId
import configparser
import time

class Control8:
    def __init__(self,org_id,project_id,topicProjectId,topic,avsc_file,report_metadata,config_file) -> None:
        self.org_id = org_id
        self.project_id = project_id
        self.topic_project_id = topicProjectId
        self.topic = topic
        self.avsc_file = avsc_file
        self.report_metadata = report_metadata
        self.config_file = config_file
    

    def generateReport(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        print("Verifying Control 8" )

        #retrieving sensitive data
        dc_results = searchCatalogAssets(self.org_id,self.project_id, str(config["DC_FILTERS"]["Control8"]))
        up_assets = queryTable(str(config["SQL"]["project_id_81"]),
                                  str(config["SQL"]["dataset_81"]),
                                  str(config["SQL"]["sql_file_81"]))
        up_list = []
        for row in up_assets:
            up_list.append(row["data_asset_prefix"])
        
        #UWC means user without case in control table - not registered
        up_assets_notcompliant_uwc = queryTable(str(config["SQL"]["project_id_82"]),
                                  str(config["SQL"]["dataset_82"]),
                                  str(config["SQL"]["sql_file_82_uwc"]))
        up_list_nc_uwc = []
        for row in up_assets_notcompliant_uwc:
            up_list_nc_uwc.append(row["data_asset"])

        #up_assets_notcompliant_lv means query without label value in job
        up_assets_notcompliant_lv = queryTable(str(config["SQL"]["project_id_82"]),
                                  str(config["SQL"]["dataset_82"]),
                                  str(config["SQL"]["sql_file_82_lv"]))
        up_list_nc_lv = []
        for row in up_assets_notcompliant_lv:
            up_list_nc_lv.append(row["data_asset"])

        #up_assets_notcompliant_lk means query without label value in job
        up_assets_notcompliant_lk = queryTable(str(config["SQL"]["project_id_82"]),
                                  str(config["SQL"]["dataset_82"]),
                                  str(config["SQL"]["sql_file_82_lk"]))
        up_list_nc_lk = []
        for row in up_assets_notcompliant_lk:
            up_list_nc_lk.append(row["data_asset"])

        #up_assets_notcompliant_date means query with expired case date in job
        up_assets_notcompliant_date = queryTable(str(config["SQL"]["project_id_82"]),
                                  str(config["SQL"]["dataset_82"]),
                                  str(config["SQL"]["sql_file_82_date"]))
        up_list_nc_date = []
        for row in up_assets_notcompliant_date:
            up_list_nc_date.append(row["data_asset"])

        #up_assets_notcompliant_date means that the user does not have the performed operation approved in a case
        up_assets_notcompliant_op = queryTable(str(config["SQL"]["project_id_82"]),
                                  str(config["SQL"]["dataset_82"]),
                                  str(config["SQL"]["sql_file_82_op"]))
        up_list_nc_op = []
        for row in up_assets_notcompliant_op:
            up_list_nc_op.append(row["data_asset"])
        
        for result in dc_results:
            found=0
            for item in up_list:               
                if item in extractTableId(result.linked_resource):
                    found = 1                    
            if found <1:
                message = {
                    "reportMetadata":self.report_metadata,
                    "CdmcControlNumber":8,
                    "Findings":str(config["FINDINGS"]["Control8_1"]),
                    "DataAsset":str(result.linked_resource),
                    "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control8_1"]),
                    "ExecutionTimestamp":str(time.time())
                }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
            else:
                if extractTableId(result.linked_resource) in up_list_nc_uwc:
                    message = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":8,
                        "Findings":str(config["FINDINGS"]["Control8_2"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control8_2_uwc"]),
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding in asset:" + result.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)                
                if extractTableId(result.linked_resource) in up_list_nc_lv:
                    message = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":8,
                        "Findings":str(config["FINDINGS"]["Control8_2"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control8_2_lv"]),
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding in asset:" + result.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)

                if extractTableId(result.linked_resource) in up_list_nc_lk:
                    message = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":8,
                        "Findings":str(config["FINDINGS"]["Control8_2"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control8_2_lk"]),
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding in asset:" + result.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
    
                if extractTableId(result.linked_resource) in up_list_nc_date:
                    message = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":8,
                        "Findings":str(config["FINDINGS"]["Control8_2"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control8_2_date"]),
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding in asset:" + result.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)

                if extractTableId(result.linked_resource) in up_list_nc_op:
                    message = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":8,
                        "Findings":str(config["FINDINGS"]["Control8_2"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control8_2_op"]),
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding in asset:" + result.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)                    