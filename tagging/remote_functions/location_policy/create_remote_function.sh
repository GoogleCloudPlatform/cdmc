export TAG_CREATOR_SA="tag-creator@sdw-data-gov-b1927e-dd69.iam.gserviceaccount.com"
export BIGQUERY_PROJECT="sdw-conf-b1927e-bcc1"

Enable Organization Policy API: https://console.developers.google.com/apis/api/orgpolicy.googleapis.com/overview?project=309178569057

TAG_CREATOR_SA needs orgpolicy.policy.get permission.  

bq mk --connection --display_name='remote function connection' --connection_type=CLOUD_RESOURCE --project_id=sdw-data-gov-b1927e-dd69 --location=us-central1 remote-function-connection

bq show --location=us-central1 --connection remote-function-connection


CREATE OR REPLACE FUNCTION `sdw-data-gov-b1927e-dd69`.remote_functions.get_location_policy(project STRING) RETURNS STRING 
REMOTE WITH CONNECTION `sdw-data-gov-b1927e-dd69.us-central1.remote-function-connection` 
OPTIONS 
(endpoint = 'https://us-central1-sdw-data-gov-b1927e-dd69.cloudfunctions.net/get_location_policy'
);

gcloud projects add-iam-policy-binding $BIGQUERY_PROJECT \
	--member=serviceAccount:$TAG_CREATOR_SA \
	--role='roles/orgpolicy.policyViewer'

gcloud functions add-iam-policy-binding get_location_policy \
	--member='serviceAccount:bqcx-309178569057-82zq@gcp-sa-bigquery-condel.iam.gserviceaccount.com' \
	--role='roles/cloudfunctions.invoker'


select `sdw-data-gov-b1927e-dd69`.remote_functions.get_location_policy('sdw-conf-b1927e-bcc1');
