output=$(bq show --location=$REGION --connection remote-function-connection)
echo"$output"
properties=$(echo "$output" | grep "remote function connection" | awk -F'   ' '{print $NF}')
service_account_id=$(echo "$properties" | python3 -c "import sys, json; print(json.load(sys.stdin)['serviceAccountId'])")
service_account_string="$service_account_id"

# Chnage placeholder for region and project and run sql to create remote connection.
sed -i '' "s/PROJECT_ID_GOV/$PROJECT_ID_GOV/g" sql/create_function.sql
sed -i '' "s/REGION/$REGION/g" sql/create_function.sql
bq query --use_legacy_sql=false < sql/create_function.sql
sed -i '' "s/$PROJECT_ID_GOV/PROJECT_ID_GOV/g" sql/create_function.sql
sed -i '' "s/$REGION/REGION/g" sql/create_function.sql

gcloud projects add-iam-policy-binding $PROJECT_NUMBER_DATA \
	--member=serviceAccount:$TAG_CREATOR_SA \
	--role='roles/orgpolicy.policyViewer'

gcloud functions add-iam-policy-binding get_location_policy \
	--member="serviceAccount:$service_account_string" \
	--role='roles/cloudfunctions.invoker'


#select `sdw-data-gov-b1927e-dd69`.remote_functions.get_location_policy('sdw-conf-b1927e-bcc1');
