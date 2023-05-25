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
from BigQueryAPI import extractTableId,getTableLocation
from LineageAPI import isLineageTarget
import configparser
import time


class Control14:
    def __init__(self,org_id,project_id,topicProjectId,topic,avsc_file,report_metadata,config_file, regionAPI, projectNumber) -> None:
        self.org_id = org_id
        self.project_id = project_id
        self.topic_project_id = topicProjectId
        self.topic = topic
        self.avsc_file = avsc_file
        self.report_metadata = report_metadata
        self.config_file = config_file
        self.regionAPI = regionAPI
        self.projectNumber = projectNumber

    def generateReport(self):
        config = configparser.ConfigParser()
        config.read(self.config_file)
        print("Verifying Control 14" )
        #Sensitive + TAG Lineage value
        results_tag_lineage = searchCatalogAssets(self.org_id,self.project_id,str(config["DC_FILTERS"]["Control14_tag"]))
        for result in results_tag_lineage:
            message = {
                "reportMetadata":self.report_metadata,
                "CdmcControlNumber":14,
                "Findings":str(config["FINDINGS"]["Control14_tag"]),
                "DataAsset":str(result.linked_resource),
                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control14_tag"]),
                "ExecutionTimestamp":str(time.time())
            }
            print("|---- Finding in asset:" + result.linked_resource)
            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
        
        #Sensitive + Lineage API
        results_sensitive = searchCatalogAssets(self.org_id,self.project_id,str(config["DC_FILTERS"]["Control14_api"]))
        for result in results_sensitive:
            if not isLineageTarget(self.projectNumber,self.regionAPI,"bigquery:" + extractTableId(result.linked_resource)):
                message = {
                    "reportMetadata":self.report_metadata,
                    "CdmcControlNumber":14,
                    "Findings":str(config["FINDINGS"]["Control14_api"]),
                    "DataAsset":str(result.linked_resource),
                    "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control14_api"]),
                    "ExecutionTimestamp":str(time.time())
                }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)