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

from pubsub_handler import publishPubSubAvro,publishPubSubAvroBatch
from DataCatalogAPI import searchCatalogAssets
from BigQueryAPI import getBQAssets,extractTableId
import configparser

class AssetsScope:
    def __init__(self,org_id,project_id,report_metadata,config_file) -> None:
        self.org_id = org_id
        self.project_id = project_id
        self.report_metadata = report_metadata
        self.config_file = config_file
    

    def publishAssets(self, execution_timestamp):
        config = configparser.ConfigParser()
        config.read(self.config_file)

        full_list = getBQAssets(self.project_id,str(config["ASSETS_SCOPE"]["region"]))
        sensitive_list = []
        result_list = []

        dc_results = searchCatalogAssets(self.org_id,self.project_id, str(config["ASSETS_SCOPE"]["filter"]))
        for result in dc_results:
            sensitive_list.append(extractTableId(result.linked_resource))
        
        for asset in full_list:
            if asset in sensitive_list:
                result_list.append(
                            {
                                "event_uuid":self.report_metadata["uuid"],
                                "asset_name":asset,
                                "sensitive": True,
                                "event_timestamp":execution_timestamp
                            })
            else:
                result_list.append(
                            {
                                "event_uuid":self.report_metadata["uuid"],
                                "asset_name":asset,
                                "sensitive": False,
                                "event_timestamp":execution_timestamp
                            })

        publishPubSubAvroBatch(str(config["ASSETS_SCOPE"]["project_pubsub"]),
                          str(config["ASSETS_SCOPE"]["topic"]),
                          str(config["ASSETS_SCOPE"]["avsc"]),
                          str(config["ASSETS_SCOPE"]["batch_max_size"]),
                          str(config["ASSETS_SCOPE"]["batch_max_bytes"]),
                          str(config["ASSETS_SCOPE"]["batch_max_latency"]),
                          result_list)        