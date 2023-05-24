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
from DataCatalogAPI import searchCatalogAssets, getColumnTagDict, getTableTagValue
from BigQueryAPI import queryTable, getTableLocation
import configparser
import time
from collections import defaultdict

class Control9:
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

        print("Verifying Control 9" )
        #Data asset is sensitive - table level tag
        dc_results = searchCatalogAssets(self.org_id,self.project_id, str(config["DC_FILTERS"]["Control9"]))

        bq_sec_encrypt = queryTable(str(config["SQL"]["project_id_9"]),
                                  str(config["SQL"]["dataset_9"]),
                                  str(config["SQL"]["sql_file_9_encrypt"]))
        dict_encrypt = defaultdict(list)
        for row in bq_sec_encrypt:
            dict_encrypt[row["sensitive_category"].upper()+ "-" +row["pm_geo"].upper()].append(row["encrypt_method"].upper()) 
            dict_encrypt[row["sensitive_category"].upper()+ "-" +row["pm_geo"].upper()].append(row["default_encrypt_method"].upper()) 

        bq_sec_dedid = queryTable(str(config["SQL"]["project_id_9"]),
                                  str(config["SQL"]["dataset_9"]),
                                  str(config["SQL"]["sql_file_9_deid"]))     
        dict_deid = defaultdict(list)
        for row in bq_sec_dedid:
            dict_deid[row["sensitive_category"].upper()+ "-" +row["pm_geo"].upper()].append(row["deid_method"].upper()) 
            dict_deid[row["sensitive_category"].upper()+ "-" +row["pm_geo"].upper()].append(row["default_deid_method"].upper())                                                           

        for result in dc_results:
            table_location = getTableLocation(result.linked_resource)
            table_sensitivity = getTableTagValue(result.relative_resource_name,str(config["TAGS"]["Control9_tag_table_sensitivity"]), str(config["TAGS"]["Control9_display_table_sensivity"]), "stringValue")
            asset_encrypt = getTableTagValue(result.relative_resource_name,str(config["TAGS"]["Control9_tag_encrypt"]), str(config["TAGS"]["Control9_display_encrypt"]), "stringValue")
            columns_sensitivity_dict = getColumnTagDict(result.relative_resource_name, str(config["TAGS"]["Control9_tag_column_sensitivity"]), str(config["TAGS"]["Control9_display_table_sensivity"]),"boolValue")
            columns_security_deid = getColumnTagDict(result.relative_resource_name, str(config["TAGS"]["Control9_tag_column_deid"]), str(config["TAGS"]["Control9_display_column_deid"]),"stringValue")
            
            #ASSET WITH INCORRECT ENCRYPTION
            if asset_encrypt not in dict_encrypt[table_sensitivity.upper() + "-" + table_location.upper()]:
                message_enc = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":9,
                        "Findings":str(config["FINDINGS"]["Control9_1"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control9_1"]),
                        "ExecutionTimestamp":str(time.time())
                }
                print("|---- Finding in asset:" + result.linked_resource)
                publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message_enc)

            for key in columns_sensitivity_dict:
                #IF SENSITIVE WITHOUT DEID OR SENSITIVE WITHOUT APP DEID OR 
                if (key not in  columns_security_deid.keys()):
                    message_no_enc = {
                        "reportMetadata":self.report_metadata,
                        "CdmcControlNumber":9,
                        "Findings":str(config["FINDINGS"]["Control9_4"]),
                        "DataAsset":str(result.linked_resource),
                        "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control9_4"]),
                        "ExecutionTimestamp":str(time.time())
                    }
                    print("|---- Finding in asset:" + result.linked_resource)
                    publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message_no_enc)                    
                else:    
                    #COLUMN ASSIGNED DEID IS NOT IN TABLE CONTROL IN BQ                   
                    if (columns_security_deid[key] not in dict_deid[table_sensitivity.upper() + "-" + table_location.upper()]):
                        message_deid = {
                            "reportMetadata":self.report_metadata,
                            "CdmcControlNumber":9,
                            "Findings":str(config["FINDINGS"]["Control9_2"]),
                            "DataAsset":str(result.linked_resource),
                            "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control9_2"]) + "for the field: " + key,
                            "ExecutionTimestamp":str(time.time())
                        }
                        print("|---- Finding in asset:" + result.linked_resource)
                        publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message_deid)                 
