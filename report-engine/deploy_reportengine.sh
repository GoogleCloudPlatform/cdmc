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

## Cloud run setup
pushd resources
## Create a copy of the config.ini.template and substitute values
cp config.ini.template config.ini
sed -i "s/<PROJECT_ID_GOV>/$PROJECT_ID_GOV/" config.ini
sed -i "s/<REGION>/$REGION/" config.ini
popd


## Deploy to cloud run
# Make sure operations happen on the governance project
gcloud config set project $PROJECT_ID_GOV

# Create a job in Cloud Run. Note parameters have to be passed here
gcloud run deploy cdmc-reportengine --image gcr.io/$PROJECT_ID_GOV/cdmc-reportengine --region $REGION --allow-unauthenticated

# Export the endpoint in an environment variable (moved to env variables.sh)
#export ENDPOINT="$(gcloud run services describe cdmc-reportengine --region $REGION --format='value(status.url)')"

# Grant access to the authenticated user
gcloud beta run services add-iam-policy-binding --region=us-central1 --member=user:$AUTHENTICATED_USER --role=roles/run.invoker cdmc-reportengine