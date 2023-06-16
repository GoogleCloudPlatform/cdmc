bq mk --connection --display_name='remote function connection' --connection_type=CLOUD_RESOURCE --project_id=cdmc-gov-388611 --location=us-central1 remote-function-connection

# Get the output of the `bq show` command.
output=$(bq show --location=us-central1 --connection remote-function-connection)
echo"$output"
properties=$(echo "$output" | grep "remote function connection" | awk -F'   ' '{print $NF}')
service_account_id=$(echo "$properties" | python3 -c "import sys, json; print(json.load(sys.stdin)['serviceAccountId'])")
service_account_string="$service_account_id"

bq query --use_legacy_sql=false < sql/create_function.sql
	
gcloud functions add-iam-policy-binding get_bytes_transferred \
	--member="serviceAccount:$service_account_string" \
	--role='roles/cloudfunctions.invoker'
	
bq query --use_legacy_sql=false < sql/test_get_bytes_transferred.sql

select `sdw-data-gov-b1927e-dd69`.remote_functions.get_bytes_transferred('cost', 'sdw-conf-b1927e-bcc1', 'crm', 'NewCust');
