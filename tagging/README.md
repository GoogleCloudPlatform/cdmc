### Tagging

The tagging aspects of the solution consist of four parts: 1) creating the Data Catalog tag templates and policy tag taxonomy; 2) create the policy tables in BigQuery and the remote BigQuery functions; 3) deploying and configuring Tag Engine; 4) and deploying and scheduling the tag update orchestration workflow. 

This guide assumes that you have already completed the data ingestion deployment, the data scanning deployment, and the data quality deployment.   

#### Part 1: Data Catalog tag templates and policy tag taxonomy

1. Create the Data Catalog tag templates by running these commands:

```
cd tag_templates
pip install -r requirements.txt
python create_template.py PROJECT REGION cdmc_controls.yaml
python create_template.py PROJECT REGION completeness_template.yaml
python create_template.py PROJECT REGION correctness_template.yaml
python create_template.py PROJECT REGION cost_metrics.yaml
python create_template.py PROJECT REGION data_sensitivity.yaml
python create_template.py PROJECT REGION impact_assessment.yaml
python create_template.py PROJECT REGION security_policy.yaml
python create_template.py PROJECT REGION uniqueness_template.yaml
cd ..
```

2. Create the policy tag taxonomy:

```
cd policy_tags
pip install -r requirements.txt
python create_policy_tag_taxonomy.py taxonomy.yaml
cd ..
```

#### Part 2: Policy tables and remote functions

3. Create and populate the policy tables: 

```
bq mk --location=us-central1 --dataset data_classification
bq mk --location=us-central1 --dataset data_retention
bq mk --location=us-central1 --dataset impact_assessment
bq mk --location=us-central1 --dataset entitlement_management
bq mk --location=us-central1 --dataset security_policy

bq query < create_data_classification_tables.sql
bq query < create_data_retention_tables.sql
bq query < create_impact_assessment_tables.sql
bq query < create_populate_entitlement_tables.sql
bq query < create_security_policy_tables.sql
bq query < information_schema_view.sql
```

4. Create the remote BigQuery functions

For each subfolder in `/remote_functions`, create a Python Cloud Function with `requirements.txt` and `main.py`. Once the function has been created, wrap it with a remote BigQuery function using the `create_remove_function.sh`. For more details on creating remote BigQuery functions, refer to the [product documentation](https://cloud.google.com/bigquery/docs/remote-functions#create_a_remote_function). 


#### Part 3: Tag Engine deployment and configuration

5. Deploy Tag Engine in your GCP project by following Tag Engine's [deployment guide](https://github.com/GoogleCloudPlatform/datacatalog-tag-engine/blob/cloud-run/README.md). 


6. Set environment variables:

``` 
export TAG_ENGINE_URL=`gcloud run services describe tag-engine --format="value(status.url)"`
export IAM_TOKEN=$(gcloud auth print-identity-token)
export OAUTH_TOKEN=$(gcloud auth application-default print-access-token)
```

7. Configure tag history:

```
curl -X POST $TAG_ENGINE_URL/configure_tag_history \
	-d '{"bigquery_region":"us-central1", "bigquery_project":"sdw-data-gov-b1927e-dd69", "bigquery_dataset":"tag_history_logs", "enabled":true}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
```

Replace the `bigquery_region`, `bigquery_project`, and `bigquery_dataset` with your own values. 


8. Create the tag engine configurations:

```
curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"	
```

```
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"		
```

```
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"		
```

```
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"	
```

```
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
```

```
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
```

```
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
	
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
```

#### Part 4: Tag update orchestration

9. 

 
