export TAG_ENGINE_PROJECT="sdw-data-gov-b1927e-dd69" 
gcloud config set project $TAG_ENGINE_PROJECT

export TAG_ENGINE_URL=`gcloud run services describe tag-engine --format="value(status.url)"`

# Bearer token
export IAM_TOKEN=$(gcloud auth print-identity-token)

# OAuth TOKEN
gcloud auth application-default login
export OAUTH_TOKEN=$(gcloud auth application-default print-access-token)

# configure tag history
curl -X POST $TAG_ENGINE_URL/configure_tag_history \
	-d '{"bigquery_region":"us-central1", "bigquery_project":"sdw-data-gov-b1927e-dd69", "bigquery_dataset":"tag_history_logs", "enabled":true}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

##########################################
# sensitive column tags (controls 6 and 7)
##########################################

# crm
curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"SENSITIVE_TAG_COLUMN","config_uuid":"45394c58eaa811ed8b314fc3e703935d"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"d6ddfc94eaa811edac56691325c5401e"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# hr
curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"SENSITIVE_TAG_COLUMN","config_uuid":"7406daa8eaaa11ed96bb691325c5401e"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"8c308c0aeaaa11ed8a22bb38d4c64047"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# oltp
curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"SENSITIVE_TAG_COLUMN","config_uuid":"27b8aa4aeaab11ed95ce41aca72ee75f"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"2f8935f0eaab11ed95ce41aca72ee75f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# sales
curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"SENSITIVE_TAG_COLUMN","config_uuid":"60201a08eaab11ed8a22bb38d4c64047"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"71ef48eeeaab11ed95ce41aca72ee75f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# finwire
curl -X POST $TAG_ENGINE_URL/create_sensitive_column_config \
	-d @tag_engine_configs/data_sensitivity_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"SENSITIVE_TAG_COLUMN","config_uuid":"df0448eeeaab11ed8a22bb38d4c64047"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"e621935ceaab11ed97a641aca72ee75f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"


##########################################
# cdmc controls table tags 
##########################################

# crm
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"91cba1c0eaac11edbff041aca72ee75f"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"6c3e8692ec1f11ed90c73b34c5f7469f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# hr
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"f3ee8084eaac11ed893341aca72ee75f"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"fcd3d3f2eaac11edac0041aca72ee75f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# oltp
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"435542c0eaad11edbff041aca72ee75f"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"4c0679e8eaad11edbad5bb38d4c64047"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# sales
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"84cb05d2eaad11edac0041aca72ee75f"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"8cf5fdc0eaad11ed81a541aca72ee75f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# finwire
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cdmc_controls_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"b3ee0c88eaad11ed81a541aca72ee75f"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"bcad48fceaad11edb9ec41aca72ee75f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

##########################################
# security policy column tags (control 9)
##########################################

# crm
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"365f07feec2411ed92b79bd64615ec44"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"55fe2220ec2411ed8008776f6836df56"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# hr
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"096fc7f0ec2511eda40051c428bb776e"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"8d2ed49cec2911ed91641955a42f5c5c"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# oltp
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"c5f52e52ec2911eda736e55a872784bf"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"cd4c14e0ec2911edbd5ee55a872784bf"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# sales
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"fba9bcf2ec2911edbd5ee55a872784bf"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"02201194ec2a11edbd5ee55a872784bf"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# finwire
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/security_policy_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"33111500ec2a11edbd5ee55a872784bf"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"3bea78b0ec2a11edabec0dc46da40d74"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

##########################################
# cost metrics table tags (control 13)
##########################################

# crm
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"feb5e302ec3911edb70be53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"b6571b08ec2a11eda5114fe45a4aa04b"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# hr
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"0b62801aec3a11ed9bb9e53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"07c62664ec2b11ed9d244fe45a4aa04b"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# oltp
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"170f7288ec3a11eda957e53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"ef014684ec2c11eda02545512d704741"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# sales
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"23fe69feec3a11eda786e53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"19c2cebaec2d11edaf3045512d704741"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# finwire
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/cost_metrics_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"2e9e76ecec3a11edb216e53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"b8c58678ef7111edb553ebd5bdaf14c8"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

##########################################
# completeness column tags (control 12)
##########################################

# crm
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"697b875cec3811edb4dee53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"70a13f5eec3811eda957e53d32969c2c"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# hr
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"ab63848aec3811edb4dee53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"b2f515e2ec3811eda957e53d32969c2c"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# oltp
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"0e833a56ec3911edae1b95ab8013e17f"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"156265ccec3911edb71995ab8013e17f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# sales
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"3b53291aec3911eda786e53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"41d2e7eeec3911edae1b95ab8013e17f"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# finwire
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/completeness_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"631efc80ec3911edb4dee53d32969c2c"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"6f399566ec3911edb22ce53d32969c2c"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

##########################################
# correctness column tags (control 12)
##########################################

# crm
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"248860aeec3b11ed934ca358983f7773"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"2b25aff2ec3b11ed8c51a358983f7773"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# hr
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"0f60ff6aec3b11ed8c51a358983f7773"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"1602666aec3b11eda8b213c3e101226b"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# oltp
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"48c4d8d0ec3b11edbfb6a358983f7773"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"531d0186ec3b11edb80513c3e101226b"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# sales
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"730c4038ec3b11ed8c51a358983f7773"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"7a479ed8ec3b11edb80513c3e101226b"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# finwire
curl -X POST $TAG_ENGINE_URL/create_dynamic_column_config \
	-d @tag_engine_configs/correctness_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_COLUMN","config_uuid":"b03d7d64ec3b11edbfb6a358983f7773"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"b636b000ec3b11ed8a4d13c3e101226b"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

#############################################
# impact assessment column tags (control 10)
#############################################

# crm
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_crm.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"1054d42cec3c11ed8d1ba358983f7773"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"5aa514b2ec3f11edab371b64f289f46e"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# hr
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_hr.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"ec18085aec3f11ed96316f77626f7884"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"f367aff2ec3f11ed9dc7ebb7a31975c4"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# oltp
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_oltp.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"15eb2842ec4011ed9dc7ebb7a31975c4"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"1c5febf4ec4011ed96316f77626f7884"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# sales
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_sales.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"527f8820ec4011eda16aebb7a31975c4"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"5a28bc9aec4011ed8b3d6f77626f7884"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

# finwire
curl -X POST $TAG_ENGINE_URL/create_dynamic_table_config \
	-d @tag_engine_configs/impact_assessment_finwire.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"DYNAMIC_TAG_TABLE","config_uuid":"84182842ec4011eda16aebb7a31975c4"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"8ba17c6cec4011ed9ef2ebb7a31975c4"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

###################################################
# export all data catalog tags to bq for reporting 
###################################################

curl -X POST $TAG_ENGINE_URL/create_export_config \
	-d @tag_engine_configs/export_all_tags.json \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

curl -i -X POST $TAG_ENGINE_URL/trigger_job \
  -d '{"config_type":"TAG_EXPORT","config_uuid":"2423082aec4111ed9bafebb7a31975c4"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"

curl -X POST $TAG_ENGINE_URL/get_job_status -d '{"job_uuid":"52507dccec4111ed88116f77626f7884"}' \
	-H "Authorization: Bearer $IAM_TOKEN" \
	-H "oauth_token: $OAUTH_TOKEN"

###################################################
# cleanup 
###################################################
curl -i -X POST $TAG_ENGINE_URL/purge_inactive_configs \
  -d '{"config_type":"ALL"}' \
  -H "Authorization: Bearer $IAM_TOKEN" \
  -H "oauth_token: $OAUTH_TOKEN"