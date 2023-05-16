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
import configparser
import time

class Control6:
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

        print("Verifying Control 6" )
        results = searchCatalogAssets(self.org_id,self.project_id,str(config["DC_FILTERS"]["Control6_1"]))
        for result in results:
            message = {
                "reportMetadata":self.report_metadata,
                "CdmcControlNumber":6,
                "Findings":str(config["FINDINGS"]["Control6_1"]),
                "DataAsset":str(result.linked_resource),
                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control6_1"]),
                "ExecutionTimestamp":str(time.time())
            }
            print("|---- Finding in asset:" + result.linked_resource)
            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
        
        results = searchCatalogAssets(self.org_id,self.project_id, str(config["DC_FILTERS"]["Control6_2"]))
        for result_assets in results:
            column_sensitive_dict = getColumnTagDict(result_assets.relative_resource_name, str(config["TAGS"]["Control6_sensitivity"]), str(config["TAGS"]["Control6_sensitivity_display"]),"boolValue")
            column_sensitive_category_dict = getColumnTagDict(result_assets.relative_resource_name, str(config["TAGS"]["Control6_sensitivy_category"]), str(config["TAGS"]["Control6_sensitivy_category_display"]),"enumValue")
            for key in column_sensitive_dict:
                # IF COLUMN IS SENSITIVE AND DOES NOT HAVE A CATEGORY IN COLUMN
                if(key not in column_sensitive_category_dict and column_sensitive_dict[key]):                        
                    message = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":6,
                        "Findings":str(config["FINDINGS"]["Control6_2"]),
                        "DataAsset":str(result_assets.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control6_2"])  + " Column:" + key,
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding 6_2 in asset:" + result_assets.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)