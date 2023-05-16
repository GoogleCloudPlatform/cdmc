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
from DataCatalogAPI import searchCatalogAssets
from BigQueryAPI import queryTable
import configparser
import time

class Control11:
    def __init__(self,org_id,project_id,topicProjectId,topic,avsc_file,report_metadata, config_file) -> None:
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

        print("Verifying Control 11" )
        bq_rp = queryTable(str(config["SQL"]["project_id_11"]),
                                  str(config["SQL"]["dataset_11"]),
                                  str(config["SQL"]["sql_file_11"]))
        
        for row in bq_rp:
            dc_search_string_action = (str(config["DC_FILTERS"]["Control11_1"])
                                .replace("$location",row["geographical_region"])
                                .replace("$sensitive_category",row["sensitive_category"])
                                .replace("$retention_method", row["expiration_action"])
                                )

            dc_results = searchCatalogAssets(self.org_id,self.project_id, dc_search_string_action)
            for result in dc_results:
                message_action = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":11,
                        "Findings":str(config["FINDINGS"]["Control11_1"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control11_1"]),
                        "ExecutionTimestamp":str(time.time())
                }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message_action)
            
            dc_search_string_period = (str(config["DC_FILTERS"]["Control11_2"])
                                .replace("$location",row["geographical_region"])
                                .replace("$sensitive_category",row["sensitive_category"])
                                .replace("$retention_method", row["expiration_action"])
                                .replace("$retention_period",str(row["retention_period_days"]))
                                )

            dc_results = searchCatalogAssets(self.org_id,self.project_id, dc_search_string_period)
            for result in dc_results:
                message_period = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":11,
                        "Findings":str(config["FINDINGS"]["Control11_2"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control11_2"]),
                        "ExecutionTimestamp":str(time.time())
                }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message_period)            

            