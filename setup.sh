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


## This script performs the basic setup for the projects 
## Including creating the required GCP services and setting up the 
## environment with the required dependencies
source environment-variables.sh
export GOOGLE_PROJECT=$PROJECT_ID_GOV


## Grant the service account used to run the setup the `serviceusage.services.enable` role.
#gcloud projects add-iam-policy-binding $PROJECT_ID \
#    --member="user:$AUTHENTICATED_USER" \
#    --role="roles/serviceusage.serviceUsageAdmin"
#
#gcloud projects add-iam-policy-binding $PROJECT_ID_GOV \
#    --member="user:$AUTHENTICATED_USER" \
#    --role="roles/serviceusage.serviceUsageAdmin"


# Activate the required APIs for all the projects
declare -a PROJECTS=($PROJECT_ID $PROJECT_ID_GOV)
for p in "${PROJECTS[@]}"
do
    :
    echo -e "\nActivating APIs in $p"
    gcloud config set project $p
    gcloud services enable datalineage.googleapis.com
    gcloud services enable cloudkms.googleapis.com
    gcloud services enable resourcesettings.googleapis.com 
    gcloud services enable artifactregistry.googleapis.com 
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable dataplex.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    gcloud services enable dlp.googleapis.com 
    gcloud services enable bigquerydatapolicy.googleapis.com
    gcloud services enable cloudfunctions.googleapis.com
    gcloud services enable bigqueryconnection.googleapis.com
    gcloud services enable datacatalog.googleapis.com
    #gcloud services enable organization-policy.googleapis.com
done

#################################
# Infrastructure for data project
#################################
gcloud config set project $PROJECT_ID

# Create the storage bucket
gcloud storage buckets create gs://${GCS_BUCKET_TPCDI} --location ${REGION} # Region is required otherwise it will default to us-central1 location

# Create the KMS
gcloud kms keyrings create ${KMS_KEYRING} --location ${REGION}
gcloud kms keys create ${KMS_KEYNAME} \
    --keyring ${KMS_KEYRING} \
    --location ${REGION} \
    --purpose "encryption"
    #--protection-level "hsm" #uncomment for HSM

# Trigger SA creation & grant permission to the BQ SA
bq show --encryption_service_account --project_id=$PROJECT_ID
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:bq-${PROJECT_NUMBER}@bigquery-encryption.iam.gserviceaccount.com \
  --role=roles/cloudkms.cryptoKeyEncrypterDecrypter


############################################
# Infrastructure for data governance project
############################################
gcloud config set project $PROJECT_ID_GOV

# Create a service account for tagging \
gcloud iam service-accounts create tag-creator \
    --description="Service account to manage tagging" \
    --display-name="Tag Engine SA"

# Create a service account for cloud run \
gcloud iam service-accounts create cloud-run \
    --description="Service account to manage cloud run service" \
    --display-name="Cloud Run SA"
    
gcloud config set project $PROJECT_ID

# Grant the CE Data Governance SA access to the Data project
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${PROJECT_NUMBER_GOV}-compute@developer.gserviceaccount.com \
  --role=roles/bigquery.user
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${PROJECT_NUMBER_GOV}-compute@developer.gserviceaccount.com \
  --role=roles/bigquery.dataViewer

# Trigger DLP SA creation & grant permission to the DLP SA
curl --request POST \
  "https://dlp.googleapis.com/v2/projects/$PROJECT_ID_GOV/locations/us-central1/content:inspect" \
  --header "X-Goog-User-Project: $PROJECT_ID_GOV" \
  --header "Authorization: Bearer $(gcloud auth print-access-token)" \
  --header 'Accept: application/json' \
  --header 'Content-Type: application/json' \
  --data '{"item":{"value":"google@google.com"}}' \
  --compressed

  gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:service-${PROJECT_NUMBER_GOV}@dlp-api.iam.gserviceaccount.com \
  --role=roles/bigquery.admin

# Create the CloudDQ dataset
bq --location=${REGION} mk ${PROJECT_ID_GOV}:${CLOUDDQ_BIGQUERY_DATASET}

# Create the Tag History dataset
bq --location=${REGION} mk ${PROJECT_ID_GOV}:${TAG_HISTORY_BIGQUERY_DATASET}

# Grant permission to the CEs service accounts in the governance project
gcloud projects add-iam-policy-binding ${PROJECT_ID_GOV} \
  --member=serviceAccount:${PROJECT_NUMBER_GOV}-compute@developer.gserviceaccount.com \
  --role=roles/logging.logWriter
gcloud projects add-iam-policy-binding ${PROJECT_ID_GOV} \
  --member=serviceAccount:${PROJECT_NUMBER_GOV}-compute@developer.gserviceaccount.com \
  --role=roles/bigquery.admin
gcloud projects add-iam-policy-binding ${PROJECT_ID_GOV} \
  --member=serviceAccount:${PROJECT_NUMBER_GOV}-compute@developer.gserviceaccount.com \
  --role=roles/serviceusage.serviceUsageConsumer