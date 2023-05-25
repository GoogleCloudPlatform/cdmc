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

class Control10:
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

        print("Verifying Control 10" )
        results = searchCatalogAssets(self.org_id,self.project_id, str(config["DC_FILTERS"]["Control10_without_tag"]))
        for result in results:
            message = {
                "reportMetadata":self.report_metadata,
                "CdmcControlNumber":10,
                "Findings":str(config["FINDINGS"]["Control10_without_tag"]),
                "DataAsset":str(result.linked_resource),
                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control10_without_tag"]),
                "ExecutionTimestamp":str(time.time())
            }
            print("|---- Finding in asset:" + result.linked_resource)
            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)

        results = searchCatalogAssets(self.org_id,self.project_id, str(config["DC_FILTERS"]["Control10_without_ia"]))
        for result in results:
            message = {
                "reportMetadata":self.report_metadata,
                "CdmcControlNumber":10,
                "Findings":str(config["FINDINGS"]["Control10_without_ia"]),
                "DataAsset":str(result.linked_resource),
                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control10_without_ia"]),
                "ExecutionTimestamp":str(time.time())
            }
            print("|---- Finding in asset:" + result.linked_resource)
            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)

        bq_ia_rows = queryTable(str(config["SQL"]["project_id_10"]),
                                str(config["SQL"]["dataset_10"]),
                                str(config["SQL"]["sql_file_10_control_table"]))
        for row in bq_ia_rows:
            results = searchCatalogAssets(self.org_id,self.project_id, str(config["DC_FILTERS"]["Control10_control_table"])
                                              .replace("$data_location",row["data_location"])
                                              .replace("$sensitive_type",row["sensitive_type"])
                                              .replace("$subject_location",row["subject_location"])
                                              .replace("$ia_type",row["ia_type"])
                                         )
            for result in results:
                message = {
                    "reportMetadata":self.report_metadata,
                    "CdmcControlNumber":10,
                    "Findings":str(config["FINDINGS"]["Control10_control_table"]),
                    "DataAsset":str(result.linked_resource),
                    "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control10_control_table"]),
                    "ExecutionTimestamp":str(time.time())
                }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
        
        bq_iaca_rows = queryTable(str(config["SQL"]["project_id_10"]),
                                str(config["SQL"]["dataset_10"]),
                                str(config["SQL"]["sql_file_10_ca"]))
        for row in bq_iaca_rows:
            results = searchCatalogAssets(self.org_id,self.project_id, str(config["DC_FILTERS"]["Control10_ca"])
                                              .replace("$asset",row["aiad_asset_name"])
                                              .replace("$most_recent_assessment",row["last_ca_approval_date"].strftime('%Y-%m-%d'))
                                         )
            for result in results:
                message = {
                    "reportMetadata":self.report_metadata,
                    "CdmcControlNumber":10,
                    "Findings":str(config["FINDINGS"]["Control10_ca"]),
                    "DataAsset":str(result.linked_resource),
                    "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control10_ca"]),
                    "ExecutionTimestamp":str(time.time())
                }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)