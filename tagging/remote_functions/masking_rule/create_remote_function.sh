export GOOGLE_APPLICATION_CREDENTIALS="/Users/scohen/keys/sdw-data-gov-tag-creator.json"
export OAUTH_TOKEN=$(gcloud auth application-default print-access-token)

bq mk --connection --display_name='remote function connection' --connection_type=CLOUD_RESOURCE --project_id=sdw-data-gov-b1927e-dd69 --location=us-central1 remote-function-connection

bq show --location=us-central1 --connection remote-function-connection


CREATE OR REPLACE FUNCTION `sdw-data-gov-b1927e-dd69`.remote_functions.get_masking_rule(project STRING, dataset STRING, table STRING, column STRING) RETURNS STRING 
REMOTE WITH CONNECTION `sdw-data-gov-b1927e-dd69.us-central1.remote-function-connection` 
OPTIONS 
(endpoint = 'https://us-central1-sdw-data-gov-b1927e-dd69.cloudfunctions.net/get_masking_rule'
);


gcloud functions add-iam-policy-binding get_masking_rule \
	--member='serviceAccount:bqcx-309178569057-82zq@gcp-sa-bigquery-condel.iam.gserviceaccount.com' \
	--role='roles/cloudfunctions.invoker'

gcloud projects add-iam-policy-binding $BIGQUERY_PROJECT \
	--member='serviceAccount:tag-creator@sdw-data-gov-b1927e-dd69.iam.gserviceaccount.com' \
	--role='roles/bigquery.dataOwner'

select `sdw-data-gov-b1927e-dd69`.remote_functions.get_masking_policy('sdw-conf-b1927e-bcc1', 'crm', 'NewCust', 'c_l_name');
select `sdw-data-gov-b1927e-dd69`.remote_functions.get_masking_policy('sdw-conf-b1927e-bcc1', 'oltp', 'Customer', 'c_f_name');
select `sdw-data-gov-b1927e-dd69`.remote_functions.get_masking_policy('sdw-conf-b1927e-bcc1', 'sales', 'Prospect', 'addressLine1');


