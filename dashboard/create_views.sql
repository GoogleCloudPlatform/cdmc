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

-- Create views for CDMC Looker Studio dashboard
-- Substitute <your_cdmc_data_gov_project> with the name of your GCP Secure Data Warehouse Blueprint data governance project
-- Substitute <your_gcp_region> with the name of the GCP region used by your GCP Secure Data Warehouse Blueprint data governance and confidential data projects (e.g. us or us-central1)

-- List all data assets scanned in the last run, broken into project, dataset and table

create or replace view <your_cdmc_data_gov_project>.cdmc_report.last_run_data_assets as

SELECT 
SPLIT(asset_name,'.') [ORDINAL(1)] as project,
SPLIT(asset_name,'.') [ORDINAL(2)] as dataset,
SPLIT(asset_name,'.') [ORDINAL(3)] as table,
sensitive

FROM `<your_cdmc_data_gov_project>.cdmc_report.data_assets` 
WHERE event_timestamp = (SELECT MAX(event_timestamp) FROM `<your_cdmc_data_gov_project>.cdmc_report.data_assets`);

-- List all findings with control number, description and remediation recommendation

create or replace view <your_cdmc_data_gov_project>.cdmc_report.last_run_findings_detail as

SELECT 
  SUBSTR(DataAsset, (STRPOS(DataAsset, '/projects/') + 10), STRPOS(DataAsset, '/datasets/') - STRPOS(DataAsset, '/projects/') - 10) as Project_Name,
  SUBSTR(DataAsset, (STRPOS(DataAsset, '/datasets/') + 10), STRPOS(DataAsset, '/tables/') - STRPOS(DataAsset, '/datasets/') - 10) as Dataset_Name,
  SUBSTR(DataAsset, (STRPOS(DataAsset, '/tables/') + 8), LENGTH(DataAsset) - STRPOS(DataAsset, '/tables/') - 7) as Table_Name,  
  CdmcControlNumber as Control_Number,
  Findings as Finding_Description,
  RecommendedAdjustment as Recommended_Adjustment
FROM 
  `<your_cdmc_data_gov_project>.cdmc_report.events` 
where 
  CdmcControlNumber>0 
  AND reportMetadata.uuid=(SELECT reportMetadata.uuid FROM `<your_cdmc_data_gov_project>.cdmc_report.events` order by ExecutionTimestamp desc limit 1);
  

-- Summary table with row per table and column per control with count of findings based on assets scanned

create or replace view <your_cdmc_data_gov_project>.cdmc_report.last_run_findings_summary as

SELECT
  SUBSTR(DataAsset, (STRPOS(DataAsset, '/projects/') + 10), STRPOS(DataAsset, '/datasets/') - STRPOS(DataAsset, '/projects/') - 10) as Project_Name,
  SUBSTR(DataAsset, (STRPOS(DataAsset, '/datasets/') + 10), STRPOS(DataAsset, '/tables/') - STRPOS(DataAsset, '/datasets/') - 10) as Dataset_Name,
  SUBSTR(DataAsset, (STRPOS(DataAsset, '/tables/') + 8), LENGTH(DataAsset) - STRPOS(DataAsset, '/tables/') - 7) as Table_Name,  
  COUNTIF(CdmcControlNumber=1) as C01_Findings,
  COUNTIF(CdmcControlNumber=2) as C02_Findings,
  COUNTIF(CdmcControlNumber=3) as C03_Findings,
  COUNTIF(CdmcControlNumber=4) as C04_Findings,
  COUNTIF(CdmcControlNumber=5) as C05_Findings,
  COUNTIF(CdmcControlNumber=6) as C06_Findings,
  COUNTIF(CdmcControlNumber=7) as C07_Findings,
  COUNTIF(CdmcControlNumber=8) as C08_Findings,
  COUNTIF(CdmcControlNumber=9) as C09_Findings,
  COUNTIF(CdmcControlNumber=10) as C10_Findings,
  COUNTIF(CdmcControlNumber=11) as C11_Findings,
  COUNTIF(CdmcControlNumber=12) as C12_Findings,
  COUNTIF(CdmcControlNumber=13) as C13_Findings,
  COUNTIF(CdmcControlNumber=14) as C14_Findings,
   
from 
  `<your_cdmc_data_gov_project>.cdmc_report.events` 
where 
  reportMetadata.uuid=(SELECT reportMetadata.uuid FROM `<your_cdmc_data_gov_project>.cdmc_report.events` order by ExecutionTimestamp desc limit 1) 
  # and DataAsset NOT LIKE ('%finwire%')
  and CdmcControlNumber > 0
group by DataAsset
Order by DataAsset;


-- Summary table with row per table and column per control with count of findings based on all assets

create or replace view <your_cdmc_data_gov_project>.cdmc_report.last_run_findings_summary_alldata as

SELECT 
  assets.project,
  assets.dataset,
  assets.table,
  assets.sensitive,
  IF (findings.C01_Findings > 0, findings.C01_Findings, 0) as C01_Findings,
  IF (findings.C02_Findings > 0, findings.C02_Findings, 0) as C02_Findings,
  IF (findings.C03_Findings > 0, findings.C03_Findings, 0) as C03_Findings,
  IF (findings.C04_Findings > 0, findings.C04_Findings, 0) as C04_Findings,
  IF (findings.C05_Findings > 0, findings.C05_Findings, 0) as C05_Findings,
  IF (findings.C06_Findings > 0, findings.C06_Findings, 0) as C06_Findings,
  IF (findings.C07_Findings > 0, findings.C07_Findings, 0) as C07_Findings,
  IF (findings.C08_Findings > 0, findings.C08_Findings, 0) as C08_Findings,
  IF (findings.C09_Findings > 0, findings.C09_Findings, 0) as C09_Findings,
  IF (findings.C10_Findings > 0, findings.C10_Findings, 0) as C10_Findings,
  IF (findings.C11_Findings > 0, findings.C11_Findings, 0) as C11_Findings,
  IF (findings.C12_Findings > 0, findings.C12_Findings, 0) as C12_Findings,
  IF (findings.C13_Findings > 0, findings.C13_Findings, 0) as C13_Findings,
  IF (findings.C14_Findings > 0, findings.C14_Findings, 0) as C14_Findings,
  IF ((C01_Findings + C02_Findings + C03_Findings + C04_Findings + C05_Findings + C06_Findings + C07_Findings + C08_Findings + C09_Findings + C10_Findings + C11_Findings + C12_Findings + C13_Findings + C14_Findings) > 0, (C01_Findings + C02_Findings + C03_Findings + C04_Findings + C05_Findings + C06_Findings + C07_Findings + C08_Findings + C09_Findings + C10_Findings + C11_Findings + C12_Findings + C13_Findings + C14_Findings), 0) as Total_Findings
FROM
  (SELECT project, dataset, table, sensitive FROM `<your_cdmc_data_gov_project>.cdmc_report.last_run_data_assets`) as assets
FULL JOIN 
  `<your_cdmc_data_gov_project>.cdmc_report.last_run_findings_summary` as findings
ON
  assets.project = findings.Project_Name AND assets.dataset = findings.Dataset_Name AND assets.table = findings.Table_Name
ORDER BY project, dataset, table ASC;

-- List count, number and % of findings and number of sensitive tables by dataset

create or replace view  <your_cdmc_data_gov_project>.cdmc_report.last_run_dataset_stats as

SELECT project, dataset, 
  COUNT(table) as num_tables, 
  COUNTIF(Total_Findings > 0) as num_tables_with_findings,
  COUNTIF(sensitive = true) as num_sensitive_tables,
  ROUND(COUNTIF(Total_Findings > 0) / COUNT(table), 2) as percentage_with_findings
FROM `<your_cdmc_data_gov_project>.cdmc_report.last_run_findings_summary_alldata` 
GROUP BY project, dataset;

-- Details of last report engine run including timestamp, UUID and controls in scope

create or replace view <your_cdmc_data_gov_project>.cdmc_report.last_run_metadata as

SELECT 
  reportMetadata.uuid as UUID, 
  ExecutionTimestamp, 
  reportMetadata.Controls as Controls_In_Scope
FROM `<your_cdmc_data_gov_project>.cdmc_report.events` 
order by ExecutionTimestamp desc 
limit 1;

-- List the data quality metrics for both completeness and correctness on a per-column basis across all data assets

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_column_dq_report as

SELECT 
project, dataset, table, column,
MAX (IF(tag_field = 'sensitive_field', tag_value, NULL)) as sensitive_field,
MAX (IF(tag_field = 'sensitive_type', tag_value, NULL)) as sensitive_type,

MAX (IF(tag_template = 'completeness_template', IF(tag_field = 'metric', tag_value, NULL), NULL)) as completenes_metric,
MAX (IF(tag_template = 'completeness_template', IF(tag_field = 'rows_validated', tag_value, NULL), NULL)) as completenes_rows_validated,
MAX (IF(tag_template = 'completeness_template', IF(tag_field = 'success_percentage', CAST(tag_value AS NUMERIC) * 100, NULL), NULL)) as completenes_success_percentage,
MAX (IF(tag_template = 'completeness_template', IF(tag_field = 'acceptable_threshold', tag_value, NULL), NULL)) as completenes_acceptable_threshold,
MAX (IF(tag_template = 'completeness_template', IF(tag_field = 'meets_threshold', tag_value, NULL), NULL)) as completenes_meets_threshold,
MAX (IF(tag_template = 'completeness_template', IF(tag_field = 'most_recent_run', tag_value, NULL), NULL)) as completenes_most_recent_run,

MAX (IF(tag_template = 'correctness_template', IF(tag_field = 'metric', tag_value, NULL), NULL)) as correctness_metric,
MAX (IF(tag_template = 'correctness_template', IF(tag_field = 'rows_validated', tag_value, NULL), NULL)) as correctness_rows_validated,
MAX (IF(tag_template = 'correctness_template', IF(tag_field = 'success_percentage', CAST (tag_value AS NUMERIC) * 100, NULL), NULL)) as correctness_success_percentage,
MAX (IF(tag_template = 'correctness_template', IF(tag_field = 'acceptable_threshold', tag_value, NULL), NULL)) as correctness_acceptable_threshold,
MAX (IF(tag_template = 'correctness_template', IF(tag_field = 'meets_threshold', tag_value, NULL), NULL)) as correctness_meets_threshold,
MAX (IF(tag_template = 'correctness_template', IF(tag_field = 'most_recent_run', tag_value, NULL), NULL)) as correctness_most_recent_run,

FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_column_tags` 
GROUP BY project, dataset, table, column;


-- List the data classification and de-identification method on a per-column basis across all data assets

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_column_security_report as

SELECT 
project, dataset, table, column,
MAX (IF(tag_field = 'sensitive_field', tag_value, NULL)) as sensitive_field,
MAX (IF(tag_field = 'sensitive_type', tag_value, NULL)) as sensitive_type,
MAX (IF(tag_field = 'platform_deid_method', tag_value, NULL)) as platform_deid_method

FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_column_tags` 
GROUP BY project, dataset, table, column;


-- Summary of which tags are present for each data asset

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_table_cdmc_controls_heatmap as

SELECT 
project,
dataset,
table,
COUNTIF(tag_field='is_sensitive') > 0 as is_sensitive,
COUNTIF(tag_field='sensitive_category') > 0 as sensitive_cat,
COUNTIF(tag_field='data_owner_name') > 0 as owner_name,
COUNTIF(tag_field='data_owner_email') > 0 as owner_email,
COUNTIF(tag_field='is_authoritative') > 0 as is_authoritative,
COUNTIF(tag_field='approved_storage_location') > 0 as approved_locs,
COUNTIF(tag_field='approved_use') > 0 as approved_use,
COUNTIF(tag_field='ultimate_source') > 0 as ult_source,
COUNTIF(tag_field='sharing_scope_geography') > 0 as sharing_geo,
COUNTIF(tag_field='sharing_scope_legal_entity') > 0 as sharing_entity,
COUNTIF(tag_field='encryption_method') > 0 as encryption_meth,
COUNTIF(tag_field='retention_period') > 0 as retention_period,
COUNTIF(tag_field='expiration_action') > 0 as expiration_action

FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags`
where tag_template='cdmc_controls'
GROUP BY project, dataset, table, tag_template;


-- List storage, query and data transfer volumes and estimated charges for each data asset based on tag data

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_table_cost_report as

SELECT 
project, dataset, table, 
MAX (IF(tag_field = 'sensitive_category', tag_value, NULL)) as sensitive_category,
FORMAT("%'d", CAST(MAX (IF(tag_field = 'total_query_bytes_billed', tag_value, NULL)) AS INT64)) as total_query_bytes_billed,
FORMAT("%'d", CAST(MAX (IF(tag_field = 'total_storage_bytes_billed', tag_value, NULL)) AS INT64)) as total_storage_bytes_billed,
FORMAT("%'d", CAST(MAX (IF(tag_field = 'total_bytes_transferred', tag_value, NULL)) AS INT64)) as total_bytes_transferred,
CONCAT('$',FORMAT("%.4f", CAST(MAX (IF(tag_field = 'estimated_query_cost', tag_value, NULL)) AS FLOAT64))) as estimated_query_cost,
CONCAT('$',FORMAT("%.4f", CAST(MAX (IF(tag_field = 'estimated_storage_cost', tag_value, NULL)) AS FLOAT64))) as estimated_storage_cost,
CONCAT('$',FORMAT("%.4f", CAST(MAX (IF(tag_field = 'estimated_egress_cost', tag_value, NULL)) AS FLOAT64))) as estimated_egress_cost,
CONCAT('$',FORMAT("%.4f", CAST(MAX (IF(tag_field = 'estimated_query_cost', tag_value, NULL)) AS FLOAT64) 
  + CAST(MAX (IF(tag_field = 'estimated_storage_cost', tag_value, NULL)) AS FLOAT64) 
  + CAST(MAX (IF(tag_field = 'estimated_egress_cost', tag_value, NULL)) AS FLOAT64))) as total_cost

FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags`
GROUP BY project, dataset, table;


-- Summary data quality report, listing assets which have quality rules and if they pass or fail the defined quality thresholds

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_table_dq_report as

SELECT project, dataset, table, 
MAX (sensitive_type) as sensitive_type,
MIN (completenes_meets_threshold) as dq_is_complete,
MIN (correctness_meets_threshold) as dq_is_correct,
 FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_column_dq_report` 
where completenes_meets_threshold IS NOT NULL OR correctness_meets_threshold IS NOT NULL
GROUP BY project, dataset, table
ORDER BY project, dataset, table ASC;


-- Impact assessment summary by data asset including storage and subject location, data classification, PIA and DPIA assessment status and dates

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_table_ia_report as

SELECT 
proj_tags.project, proj_tags.dataset, proj_tags.table,

ANY_VALUE (IF(proj_tags.tag_field = 'approved_storage_location', proj_tags.tag_value, NULL)) as approved_storage_location,
ANY_VALUE (IF(proj_tags.tag_field = 'is_sensitive', proj_tags.tag_value, NULL)) as is_sensitive,
ANY_VALUE (IF(proj_tags.tag_field = 'sensitive_category', proj_tags.tag_value, NULL)) as sensitive_category,
(SELECT ia_tags.tag_value FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` ia_tags 
  WHERE ia_tags.project=proj_tags.project 
  AND ia_tags.dataset=proj_tags.dataset
  AND ia_tags.table=proj_tags.table
  AND ia_tags.tag_field='subject_locations'
  AND ia_tags.tag_template='impact_assessment') as subject_locations,
(SELECT ia_tags.tag_value FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` ia_tags 
  WHERE ia_tags.project=proj_tags.project 
  AND ia_tags.dataset=proj_tags.dataset
  AND ia_tags.table=proj_tags.table
  AND ia_tags.tag_field='is_dpia'
  AND ia_tags.tag_template='impact_assessment') as is_dpia,
(SELECT ia_tags.tag_value FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` ia_tags 
  WHERE ia_tags.project=proj_tags.project 
  AND ia_tags.dataset=proj_tags.dataset
  AND ia_tags.table=proj_tags.table
  AND ia_tags.tag_field='is_pia'
  AND ia_tags.tag_template='impact_assessment') as is_pia,
(SELECT ia_tags.tag_value FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` ia_tags 
  WHERE ia_tags.project=proj_tags.project 
  AND ia_tags.dataset=proj_tags.dataset
  AND ia_tags.table=proj_tags.table
  AND ia_tags.tag_field='most_recent_assessment'
  AND ia_tags.tag_template='impact_assessment') as most_recent_assessment,
(SELECT ia_tags.tag_value FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` ia_tags 
  WHERE ia_tags.project=proj_tags.project 
  AND ia_tags.dataset=proj_tags.dataset
  AND ia_tags.table=proj_tags.table
  AND ia_tags.tag_field='oldest_assessment'
  AND ia_tags.tag_template='impact_assessment') as oldest_assessment

FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` proj_tags
where proj_tags.tag_template='cdmc_controls'
GROUP BY project, dataset, table, tag_template;


-- Data retention summary by data asset, including retention period and expiration action

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_table_retention_report as

SELECT 
project, dataset, table, 
MAX (IF(tag_field = 'sensitive_category', tag_value, NULL)) as sensitive_category,
MAX (IF(tag_field = 'retention_period', tag_value, NULL)) as retention_period,
MAX (IF(tag_field = 'expiration_action', tag_value, NULL)) as expiration_action

FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` 
GROUP BY project, dataset, table;


-- Table-level security summary including data classification and encryption method

create or replace view <your_cdmc_data_gov_project>.tag_exports.catalog_report_table_security_report as

SELECT 
project, dataset, table,
ANY_VALUE (IF(tag_field = 'is_sensitive', tag_value, NULL)) as is_sensitive,
ANY_VALUE (IF(tag_field = 'sensitive_category', tag_value, NULL)) as sensitive_category,
ANY_VALUE (IF(tag_field = 'encryption_method', tag_value, NULL)) as encryption_method

FROM `<your_cdmc_data_gov_project>.tag_exports.catalog_report_table_tags` 
where tag_template='cdmc_controls'
GROUP BY project, dataset, table, tag_template;

-- Summary of job tag/value pairs used for entitlement management

create or replace view <your_cdmc_data_gov_project>.cdmc_report.information_schema_view as

select * from (
SELECT
    cast(i.start_time as date) as job_date,
	i.user_email AS user_id,
    i.statement_type AS operation, 
    CONCAT(rf.project_id,'.',rf.dataset_id,'.',rf.table_id) as data_asset,
    l.key as key,
	l.value as value
FROM
    region-<your_gcp_region>.INFORMATION_SCHEMA.JOBS_BY_FOLDER as i,
    unnest(i.referenced_tables) as rf,
	unnest(i.labels) as l
UNION ALL
SELECT
    cast(i.start_time as date) as job_date,
	i.user_email AS user_id,
    i.statement_type AS operation, 
    CONCAT(rf.project_id,'.',rf.dataset_id,'.',rf.table_id) as data_asset,
    NULL as key,
	NULL as value
FROM
    region-<your_gcp_region>.INFORMATION_SCHEMA.JOBS_BY_FOLDER as i,
    unnest(i.referenced_tables) as rf
);