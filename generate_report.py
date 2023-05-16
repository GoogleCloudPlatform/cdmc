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
from BigQueryAPI import getBQAssets
import configparser
from AssetsScope import AssetsScope
from Control2 import Control2
from Control3 import Control3
from Control4 import Control4
from Control6 import Control6
from Control7 import Control7
from Control8 import Control8
from Control9 import Control9
from Control10 import Control10
from Control11 import Control11
from Control12 import Control12
from Control13 import Control13
from Control14 import Control14
import time


def generateReport(orgId, projId, topicProjectId, topicname, report_metadata, projectNumber, assetsScope, controlNumber):
    print("=============================================")
    print("======= STARTING CDMC CONTROLS FINDINGS =====")
    print("=============================================")

    config_file = "./resources/config.ini"
    org_id=orgId
    project_id = projId
    topic = topicname
    avsc_file = "./resources/cmdc_event.avsc"
    execution_timestamp = str(time.time())

    message = {
            "reportMetadata":report_metadata,
            "CdmcControlNumber":0,
            "Findings":"Control record",
            "DataAsset":"",
            "RecommendedAdjustment":"",
            "ExecutionTimestamp":execution_timestamp
        }
    print("|---- Sending finding control")
    publishPubSubAvro(topicProjectId,topic,avsc_file,message)

    if assetsScope: 
        ac = AssetsScope(org_id, project_id,report_metadata,config_file)
        ac.publishAssets(execution_timestamp)

    if controlNumber.find("02")>-1: 
        c2 = Control2(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c2.generateReport()
    if controlNumber.find("03")>-1: 
        c3 = Control3(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c3.generateReport()
    if controlNumber.find("04")>-1:
        c4 = Control4(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c4.generateReport()
    if controlNumber.find("06")>-1:
        c6 = Control6(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c6.generateReport()
    if controlNumber.find("07")>-1:
        c7 = Control7(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c7.generateReport_1()
        c7.generateReport_2()
    if controlNumber.find("08")>-1:
        c8 = Control8(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c8.generateReport()
    if controlNumber.find("09")>-1:
        c9 = Control9(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c9.generateReport()     
    if controlNumber.find("10")>-1:
        c10 = Control10(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c10.generateReport()      
    if controlNumber.find("11")>-1:
        c11 = Control11(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c11.generateReport()  
    if controlNumber.find("12")>-1:
        c12 = Control12(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c12.generateReportSensitive()  
        c12.generateReportNonSensitive()       
    if controlNumber.find("13")>-1:
        c13 = Control13(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c13.generateReport()        
    if controlNumber.find("14")>-1:
        c14 = Control14(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file, 'us-central1',projectNumber)
        c14.generateReport()            
    if controlNumber=="all": 
        c2 = Control2(org_id,project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c2.generateReport()
        c3 = Control3(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c3.generateReport()
        c4 = Control4(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c4.generateReport()
        c6 = Control6(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c6.generateReport()
        c7 = Control7(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c7.generateReport_1()
        c7.generateReport_2()
        c8 = Control8(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c8.generateReport()
        c9 = Control9(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c9.generateReport()
        c10 = Control10(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c10.generateReport()  
        c11 = Control11(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c11.generateReport()
        c12 = Control12(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c12.generateReportSensitive()  
        c12.generateReportNonSensitive()   
        c13 = Control13(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file)
        c13.generateReport()         
        c14 = Control14(org_id, project_id,topicProjectId, topic,avsc_file,report_metadata,config_file,'us', projectNumber)
        c14.generateReport()  


