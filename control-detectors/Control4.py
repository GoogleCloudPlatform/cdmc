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
from DataCatalogAPI import searchCatalogAssets, getTableTagValue
from BigQueryAPI import getTableLocation, extractTableId
import configparser
import time

class Control4:
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
        print("Verifying Control 4" )
        results = searchCatalogAssets(self.org_id,self.project_id,str(config["DC_FILTERS"]["Control4_1"]))
        for result in results:
            message = {
                "reportMetadata":self.report_metadata,
                "CdmcControlNumber":4,
                "Findings":str(config["FINDINGS"]["Control4_1"]),
                "DataAsset":str(result.linked_resource),
                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control4_1"]),
                "ExecutionTimestamp":str(time.time())
            }
            print("|---- Finding in asset:" + result.linked_resource)
            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)

        tag_template_name=str(config["TAGS"]["Control4_template"])
        tag_display_name=str(config["TAGS"]["Control4_display"])
        results = searchCatalogAssets(self.org_id,self.project_id,str(config["DC_FILTERS"]["Control4_2"]))
        for result in results:
            location=getTableTagValue(result.relative_resource_name,tag_template_name,tag_display_name,"stringValue")
            approved_locations=""
            for item in location.split(","):
                approved_locations = approved_locations + config["LOCATIONS"][item].upper()
            if(getTableLocation(result.linked_resource).upper()+",") not in approved_locations:
                message = {
                    "reportMetadata":self.report_metadata,
                    "CdmcControlNumber":4,
                    "Findings":str(config["FINDINGS"]["Control4_2"]),
                    "DataAsset":str(result.linked_resource),
                    "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control4_2"]),
                    "ExecutionTimestamp":str(time.time())
                    }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)