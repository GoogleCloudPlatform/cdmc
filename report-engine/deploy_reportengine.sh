# Copyright 2023 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


## Initialise environment variables
pushd ../
source environment-variables.sh
popd

# Make sure operations happen on the governance project
gcloud config set project $PROJECT_ID_GOV

###########################
# Create a SA for cloud run
###########################
gcloud iam service-accounts create cdmc-reportengine \
    --description="A service account that runs the CDMC Controls Engines" \
    --display-name="cdmc-reportengine"

gcloud projects add-iam-policy-binding $BIGQUERY_PROJECT \
	--member=serviceAccount:$REPORTENGINE_SA \
	--role=roles/bigquery.dataEditor
	
gcloud projects add-iam-policy-binding $BIGQUERY_PROJECT \
	--member=serviceAccount:$REPORTENGINE_SA \
	--role=roles/bigquery.jobUser

gcloud projects add-iam-policy-binding $BIGQUERY_PROJECT \
	--member=serviceAccount:$REPORTENGINE_SA \
	--role=roles/bigquery.metadataViewer

gcloud projects add-iam-policy-binding $PROJECT_ID_GOV \
	--member=serviceAccount:$REPORTENGINE_SA \
	--role=roles/pubsub.editor

######################
## Deploy to cloud run
######################

# Generate token
gcloud auth application-default login
export OAUTH_TOKEN=$(gcloud auth application-default print-access-token)


# Create a job in Cloud Run. Note parameters have to be passed here
gcloud run deploy cdmc-reportengine \
    --image gcr.io/$PROJECT_ID_GOV/cdmc-reportengine \
    --region $REGION \
    --service-account=$REPORTENGINE_SA


# Export the endpoint in an environment variable (moved to env variables.sh)
export ENDPOINT="$(gcloud run services describe cdmc-reportengine --region $REGION --format='value(status.url)')"

# Grant access to the authenticated user
gcloud run services add-iam-policy-binding cdmc-reportengine --member=user:$AUTHENTICATED_USER --role=roles/run.invoker 