### Tagging

The tagging aspects of the solution consist of four parts:

1. Creating the Data Catalog tag templates and policy tag taxonomy
1. Create the policy tables in BigQuery and the remote BigQuery functions
1. Deploying and configuring Tag Engine
1. Deploying and scheduling the tag update orchestration workflow

This guide assumes that you have already completed the data ingestion deployment, the data scanning deployment, and the data quality deployment.

#### Part 1: Data Catalog tag templates and policy tag taxonomy

1. Create the Data Catalog tag templates by running these commands:

```
cd tag_templates
pip install -r requirements.txt
python create_template.py $PROJECT_ID_DATA $REGION cdmc_controls.yaml
python create_template.py $PROJECT_ID_DATA $REGION completeness_template.yaml
python create_template.py $PROJECT_ID_DATA $REGION correctness_template.yaml
python create_template.py $PROJECT_ID_DATA $REGION cost_metrics.yaml
python create_template.py $PROJECT_ID_DATA $REGION data_sensitivity.yaml
python create_template.py $PROJECT_ID_DATA $REGION impact_assessment.yaml
python create_template.py $PROJECT_ID_DATA $REGION security_policy.yaml
python create_template.py $PROJECT_ID_DATA $REGION uniqueness_template.yaml
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
bq mk --location=$REGION --dataset data_classification
bq mk --location=$REGION --dataset data_retention
bq mk --location=$REGION --dataset impact_assessment
bq mk --location=$REGION --dataset entitlement_management
bq mk --location=$REGION --dataset security_policy

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
	-d '{"bigquery_region":"$REGION", "bigquery_project":"$PROJECT_ID_GOV", "bigquery_dataset":"tag_history_logs", "enabled":true}' \
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

```
curl -X POST $TAG_ENGINE_URL/create_export_config \
	-d @tag_engine_configs/export_all_tags.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"
```

#### Part 4: Tag update orchestration

9. Enable the Cloud Workflows API.

10. Open each yaml file under the `/orchestration` folder, and replace the `config_uuid` values starting on line 9 with the actual values you received from the previous step when creating the configs. You'll also need to replace the project id values in the `caller_workflow.yaml` file.

10. Deploy the workflows:

To deploy a workflow, you need to specify a service account that you'd like the workflow to run as. We recommend you use the cloud run service account which you created for running Tag Engine. This will be referred to as CLOUD_RUN_SA in the commands below.

```
gcloud workflows deploy tag-updates-data-sensitivity --location=$REGION \
	--source=tag_updates_data_sensitivity.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy tag-updates-cdmc-controls --location=$REGION \
	--source=tag_updates_cdmc_controls.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy tag-updates-security-policy --location=$REGION \
	--source=tag_updates_security_policy.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy tag-updates-cost-metrics --location=$REGION \
	--source=tag_updates_cost_metrics.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy tag-updates-completeness --location=$REGION \
	--source=tag_updates_completeness.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy tag-updates-correctness --location=$REGION \
	--source=tag_updates_correctness.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy tag-updates-impact-assessment --location=$REGION \
	--source=tag_updates_impact_assessment.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy tag-exports-all-templates --location=$REGION \
	--source=tag_exports_all_templates.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy oauth-token --location=$REGION \
	--source=oauth_token.yaml --service-account=CLOUD_RUN_SA

gcloud workflows deploy caller_workflow --location=$REGION \
	--source=caller_workflow.yaml --service-account=CLOUD_RUN_SA
```

11. Open the Cloud Workflows UI and create a job trigger for the `caller_workflow`. The `caller_workflow` executes all of the other workflows in the right sequence. The `caller_workflow` takes about ~70 minutes to run. By creating the job trigger, you are scheduling the `caller_workflow` to run on a regular interval.

