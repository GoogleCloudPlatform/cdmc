bq mk --connection --display_name='remote function connection' --connection_type=CLOUD_RESOURCE --project_id=sdw-data-gov-b1927e-dd69 --location=us-central1 remote-function-connection

bq show --location=us-central1 --connection remote-function-connection


CREATE OR REPLACE FUNCTION `sdw-data-gov-b1927e-dd69`.remote_functions.get_encryption_type(project STRING, dataset STRING, table STRING) RETURNS STRING 
REMOTE WITH CONNECTION `sdw-data-gov-b1927e-dd69.us-central1.remote-function-connection` 
OPTIONS 
(endpoint = 'https://us-central1-sdw-data-gov-b1927e-dd69.cloudfunctions.net/get_encryption_type'
);

gcloud functions add-iam-policy-binding get_encryption_type \
	--member='serviceAccount:bqcx-309178569057-82zq@gcp-sa-bigquery-condel.iam.gserviceaccount.com' \
	--role='roles/cloudfunctions.invoker'

select `sdw-data-gov-b1927e-dd69`.remote_functions.get_encryption_type('sdw-conf-b1927e-bcc1', 'crm', 'NewCust');
select `sdw-data-gov-b1927e-dd69`.remote_functions.get_encryption_type('sdw-conf-b1927e-bcc1', 'hr', 'Employee');


Make sure you grant TAG_CREATOR_SA the Cloud KMS Viewer role. Otherwise you will get this error:

Received response code 400 from endpoint https://us-central1-sdw-data-gov-b1927e-dd69.cloudfunctions.net/get_encryption_type with response {"errorMessage": "403 Permission 'cloudkms.cryptoKeys.get' denied on resource 'projects/sdw-data-gov-b1927e-dd69/locations/us-central1/keyRings/cmek-keyring-bigquery/cryptoKeys/cmek-bigquery-hsm-key' (or it may not exist)."}.