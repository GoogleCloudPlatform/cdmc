bq mk --connection --display_name='remote function connection' --connection_type=CLOUD_RESOURCE --project_id=sdw-data-gov-b1927e-dd69 --location=us-central1 remote-function-connection

bq show --location=us-central1 --connection remote-function-connection


CREATE OR REPLACE FUNCTION `sdw-data-gov-b1927e-dd69`.remote_functions.get_bytes_transferred(mode STRING, 
											project STRING, dataset STRING, table STRING) RETURNS FLOAT64 
REMOTE WITH CONNECTION `sdw-data-gov-b1927e-dd69.us-central1.remote-function-connection` 
OPTIONS 
(endpoint = 'https://us-central1-sdw-data-gov-b1927e-dd69.cloudfunctions.net/get_bytes_transferred'
);
	
gcloud functions add-iam-policy-binding get_bytes_transferred \
	--member='serviceAccount:bqcx-309178569057-82zq@gcp-sa-bigquery-condel.iam.gserviceaccount.com' \
	--role='roles/cloudfunctions.invoker'
	
select `sdw-data-gov-b1927e-dd69`.remote_functions.get_bytes_transferred('bytes', 'sdw-conf-b1927e-bcc1', 'crm', 'AddAcct');

select `sdw-data-gov-b1927e-dd69`.remote_functions.get_bytes_transferred('cost', 'sdw-conf-b1927e-bcc1', 'crm', 'NewCust');
