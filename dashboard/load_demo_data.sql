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

-- Sample data load for CDMC dashboard
-- Substitute <your_cdmc_data_gov_project> with the name of your GCP Secure Data Warehouse Blueprint data governance project
-- Substitute <your_cdmc_demo_data_bucket> with the name of the GCS bucket you uploaded the Avro files into. Should be in same region as BigQuery datasets being created (e.g. US multi-region)
-- Substitute <your_gcp_region> with the name of the GCP region used by your GCP Secure Data Warehouse Blueprint data governance and confidential data projects (e.g. us or us-central1)

CREATE SCHEMA `<your_cdmc_data_gov_project>.cdmc_report`
  OPTIONS (
    location = '<your_gcp_region>'
    );

CREATE TABLE `<your_cdmc_data_gov_project>.cdmc_report.data_assets` (
  event_uuid STRING,
  asset_name STRING,
  event_timestamp TIMESTAMP,
  sensitive BOOLEAN
);

CREATE TABLE `<your_cdmc_data_gov_project>.cdmc_report.events` (
  reportMetadata STRUCT <
    uuid STRING,
    Controls STRING>,
  CdmcControlNumber INTEGER,
  Findings STRING,
  DataAsset STRING,
  RecommendedAdjustment STRING,
  ExecutionTimestamp TIMESTAMP
);

CREATE SCHEMA `<your_cdmc_data_gov_project>.tag_exports`
  OPTIONS (
    location = '<your_gcp_region>'
    );

CREATE TABLE `<your_cdmc_data_gov_project>.tag_exports.catalog_report_column_tags` (
 project STRING, 
 dataset STRING, 
 table STRING, 
 column STRING,
 tag_template STRING,
 tag_field STRING, 
 tag_value STRING, 
 export_time TIMESTAMP
);

CREATE TABLE `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` (
 project STRING, 
 dataset STRING, 
 table STRING, 
 tag_template STRING,
 tag_field STRING, 
 tag_value STRING, 
 export_time TIMESTAMP
);

LOAD DATA INTO <your_cdmc_data_gov_project>.cdmc_report.data_assets
  FROM FILES(
    format='AVRO',
    uris = ['gs://<your_cdmc_demo_data_bucket>/cdmc_report_data_assets_demo.avro']
  );
  
LOAD DATA INTO <your_cdmc_data_gov_project>.cdmc_report.events
  FROM FILES(
    format='AVRO',
    uris = ['gs://<your_cdmc_demo_data_bucket>/cdmc_report_events_demo.avro']
  );

LOAD DATA INTO <your_cdmc_data_gov_project>.tag_exports.catalog_report_column_tags
  FROM FILES(
    format='AVRO',
    uris = ['gs://<your_cdmc_demo_data_bucket>/tag_exports_catalog_report_column_tags_demo.avro']
  );

LOAD DATA INTO <your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags
  FROM FILES(
    format='AVRO',
    uris = ['gs://<your_cdmc_demo_data_bucket>/tag_exports_catalog_report_table_tags_demo.avro']
  );  