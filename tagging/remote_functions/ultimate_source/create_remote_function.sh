CREATE OR REPLACE FUNCTION `sdw-data-gov-b1927e-dd69`.remote_functions.get_ultimate_source(project_id STRING, project_num INT64, region STRING, dataset STRING, table STRING) RETURNS STRING
REMOTE WITH CONNECTION `sdw-data-gov-b1927e-dd69.us-central1.remote-function-connection` 
OPTIONS 
(endpoint = 'https://us-central1-sdw-data-gov-b1927e-dd69.cloudfunctions.net/get_ultimate_source'
);

gcloud functions add-iam-policy-binding get_ultimate_source \
	--member='serviceAccount:bqcx-309178569057-82zq@gcp-sa-bigquery-condel.iam.gserviceaccount.com' \
	--role='roles/cloudfunctions.invoker'

export BIGQUERY_PROJECT="sdw-conf-b1927e-bcc1"

gcloud projects add-iam-policy-binding $BIGQUERY_PROJECT \
	--member='serviceAccount:tag-creator@sdw-data-gov-b1927e-dd69.iam.gserviceaccount.com' \
	--role='roles/datalineage.viewer'

select `sdw-data-gov-b1927e-dd69`.remote_functions.get_ultimate_source('sdw-conf-b1927e-bcc1', 707062315533, 'us-central1', 'crm', 'NewCust');

Note: you need to grant the TAG_CREATOR_SA the roles/datalineage.viewer on the BIGQUERY_PROJECT. Otherwise you will get this error:

'datalineage.locations.searchLinks' denied on resource '//datalineage.googleapis.com/projects/707062315533/locations/us-central1' (or it may not exist).", 'status': 'PERMISSION_DENIED', 'details': [{'@type': 'type.googleapis.com/google.rpc.ErrorInfo', 'reason': 'IAM_PERMISSION_DENIED', 'domain': 'datalineage.googleapis.com', 'metadata': {'resource': 'projects/707062315533/locations/us-central1', 'permission': 'datalineage.locations.searchLinks'}}]}}

