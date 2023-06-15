bq mk --connection --display_name='remote function connection' --connection_type=CLOUD_RESOURCE --project_id=cdmc-gov-388611 --location=us-central1 remote-function-connection

bq show --location=us-central1 --connection remote-function-connection

bq query --use_legacy_sql=false < create_function.sql
	
gcloud functions add-iam-policy-binding get_bytes_transferred \
	--member='serviceAccount:bqcx-440292903921-ha87@gcp-sa-bigquery-condel.iam.gserviceaccount.com' \
	--role='roles/cloudfunctions.invoker'
	
bq query --use_legacy_sql=false < test_get_bytes_transferred.sql

select `sdw-data-gov-b1927e-dd69`.remote_functions.get_bytes_transferred('cost', 'sdw-conf-b1927e-bcc1', 'crm', 'NewCust');
