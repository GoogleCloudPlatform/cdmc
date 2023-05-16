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
from BigQueryAPI import getTablePolicyTagsDict
import configparser
import time

class Control7:
    def __init__(self,org_id,project_id,topicProjectId,topic,avsc_file,report_metadata,config_file) -> None:
        self.org_id = org_id
        self.project_id = project_id
        self.topic_project_id = topicProjectId
        self.topic = topic
        self.avsc_file = avsc_file
        self.report_metadata = report_metadata
        self.config_file = config_file
    
    def generateReport_1(self):

        config = configparser.ConfigParser()
        config.read(self.config_file)

        print("Verifying Control 7" )
        results = searchCatalogAssets(self.org_id,self.project_id,str(config["DC_FILTERS"]["Control7_1"]))
        for result in results:
            message = {
                "reportMetadata":self.report_metadata,
                "CdmcControlNumber":7,
                "Findings":str(config["FINDINGS"]["Control7_1"]),
                "DataAsset":str(result.linked_resource),
                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control7_1"]),
                "ExecutionTimestamp":str(time.time())
            }
            print("|---- Finding 7.1 in asset:" + result.linked_resource)
            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)

    def generateReport_2(self):

        config = configparser.ConfigParser()
        config.read(self.config_file)

        print("Verifying Control 7_2" )

        
        results = searchCatalogAssets(self.org_id,self.project_id,str(config["DC_FILTERS"]["Control7_2"]))
        for result_assets in results:
            tag_dict = getColumnTagDict(result_assets.relative_resource_name, str(config["TAGS"]["Control7"]), str(config["TAGS"]["Control7_display"]),"enumValue")
            policy_dict = getTablePolicyTagsDict(result_assets.linked_resource)
            for key in tag_dict:
                if(key in policy_dict and tag_dict[key]!= policy_dict[key]):
                    message = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":7,
                        "Findings":str(config["FINDINGS"]["Control7_2"]),
                        "DataAsset":str(result_assets.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control7_2"]),
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding 7.2 in asset:" + result_assets.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
