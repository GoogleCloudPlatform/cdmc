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

class Control12:
    def __init__(self,org_id,project_id,topicProjectId,topic,avsc_file,report_metadata,config_file) -> None:
        self.org_id = org_id
        self.project_id = project_id
        self.topic_project_id = topicProjectId
        self.topic = topic
        self.avsc_file = avsc_file
        self.report_metadata = report_metadata
        self.config_file = config_file
    
    def generateReportSensitive(self):

        config = configparser.ConfigParser()
        config.read(self.config_file)

        print("Verifying Control 12 - Sensitive")
        search_string = str(config["DC_FILTERS"]["Control12_sensitive"])
        for template in str(config["QUALITY_TEMPLATE"]["dimensions"]).split(","):
            search_string = search_string + " -tag:" + template
        results = searchCatalogAssets(self.org_id,self.project_id, search_string)

        #SENSITIVE DATA WITHOUT QUALITY CONTROLS
        for result in results:
            message = {
                "reportMetadata":self.report_metadata,
                "CdmcControlNumber":12,
                "Findings":str(config["FINDINGS"]["Control12_sensitivewithoutquality"]),
                "DataAsset":str(result.linked_resource),
                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control12_sensitivewithoutquality"]),
                "ExecutionTimestamp":str(time.time())
            }
            print("|---- Finding 12_missing_quality_table in asset:" + result.linked_resource)
            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)

        #SENSITIVE DATA WITH QUALITY CONTROL IN COLUMNS
        search_string = "(" + str(config["DC_FILTERS"]["Control12_sensitive"]) + "("
        for template in str(config["QUALITY_TEMPLATE"]["dimensions"]).split(","):
            search_string = search_string + "tag:" + template + " OR "
        search_string = search_string + ")"
        search_string = search_string.replace(" OR )",")")
        results = searchCatalogAssets(self.org_id,self.project_id, search_string)
        for result_assets in results:
            for template in str(config["QUALITY_TEMPLATE"]["dimensions"]).split(","):
                column_sensitive_dict = getColumnTagDict(result_assets.relative_resource_name, str(config["TAGS"]["Control12_sensitivity"]), str(config["TAGS"]["Control12_sensitivity_display"]),"boolValue")
                column_quality_dict = getColumnTagDict(result_assets.relative_resource_name, str(config["QUALITY_TEMPLATE"]["threshold_field"]), str(config["TAGS"]["Control12_display"]),"boolValue")                
                for key in column_sensitive_dict:
                    # IF COLUMN IS SENSITIVE AND DOES NOT HAVE A QUALITY IN COLUMN
                    if(key not in column_quality_dict and column_sensitive_dict[key]):                        
                        message = {
                            "reportMetadata":self.report_metadata,
                            "CdmcControlNumber":12,
                            "Findings":str(config["FINDINGS"]["Control12_missingcolumn"]),
                            "DataAsset":str(result_assets.linked_resource),
                            "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control12_missingcolumn"])  + " Quality dimension:" + template +" Column:" + key,
                            "ExecutionTimestamp":str(time.time())
                        }
                        print("|---- Finding 12_missing_column_quality_" + template +" in asset:" + result_assets.linked_resource)
                        publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
                    else: 
                        #IF COLUMN IS SENSITIVE, HAVE COLUMN AND QUALITY THRESHOLD IS FALSE
                        if(not column_quality_dict[key]):
                            message = {
                                "reportMetadata":self.report_metadata,
                                "CdmcControlNumber":12,
                                "Findings":str(config["FINDINGS"]["Control12_threshold"]),
                                "DataAsset":str(result_assets.linked_resource),
                                "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control12_threshold"]) + " Quality dimension:" + template +" Column:" + key,
                                "ExecutionTimestamp":str(time.time())
                            }
                            print("|---- Finding 12_threshold_" + template +" in asset:" + result_assets.linked_resource)
                            publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)
                    
                for key in column_quality_dict:    
                    #DATA ASSET IS SENSITIVE, COLUMN IS NOT SENSITIVE AND DOES NOT MEETS THRESHOLD
                    if(key not in column_sensitive_dict and not column_quality_dict[key]):                        
                        message = {
                            "reportMetadata":self.report_metadata,
                            "CdmcControlNumber":12,
                            "Findings":str(config["FINDINGS"]["Control12_nonsensitivecolumn_threshold"]),
                            "DataAsset":str(result_assets.linked_resource),
                            "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control12_nonsensitivecolumn_threshold"]),
                            "ExecutionTimestamp":str(time.time())
                        }
                        print("|---- Finding 12_nonsensitivecolumn_threshold" + template +" in asset:" + result_assets.linked_resource)
                        publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)                    

    def generateReportNonSensitive(self):

        config = configparser.ConfigParser()
        config.read(self.config_file)

        print("Verifying Control 12 - Non Sensitive" )
        search_string = "(" + str(config["DC_FILTERS"]["Control12_nonsensitive"])
        for template in str(config["QUALITY_TEMPLATE"]["dimensions"]).split(","):
            search_string = search_string + " tag:" + template + "." + str(config["QUALITY_TEMPLATE"]["threshold_field"]) + "=FALSE OR "
        search_string = search_string + ")"
        search_string = search_string.replace(" OR )",")")
        results = searchCatalogAssets(self.org_id,self.project_id, search_string)
        for result_assets in results:
            for template in str(config["QUALITY_TEMPLATE"]["dimensions"]).split(","):
                column_quality_dict = getColumnTagDict(result_assets.relative_resource_name, str(config["QUALITY_TEMPLATE"]["threshold_field"]), str(config["TAGS"]["Control12_display"]),"boolValue")                
                for key in column_quality_dict:
                    # IF COLUMN HAS QUALITY IN COLUMN WITH THRESHOLD = FALSE
                    if(not column_quality_dict[key]):
                        message = {
                            "reportMetadata":self.report_metadata,
                            "CdmcControlNumber":12,
                            "Findings":str(config["FINDINGS"]["Control12_nonsensitive"]),
                            "DataAsset":str(result_assets.linked_resource),
                            "RecommendedAdjustment":str(config["RECOMMENDATIONS"]["Control12_nonsensitive"]) + " Quality dimension:" + template +" Column:" + key,
                            "ExecutionTimestamp":str(time.time())
                        }
                        print("|---- Finding 12_nonsensitive_threshold in asset no sensitive:" + result_assets.linked_resource)
                        publishPubSubAvro(self.topic_project_id,self.topic,self.avsc_file,message)           