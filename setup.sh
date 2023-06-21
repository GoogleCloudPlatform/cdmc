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

# Activate the required APIs for all the projects
declare -a PROJECTS=($PROJECT_ID $PROJECT_ID_GOV)
for p in "${PROJECTS[@]}"
do
    :
    echo -e "\nActivating APIs in $p"
    gcloud config set project $p
    gcloud services enable bigquery.googleapis.com
    gcloud services enable datalineage.googleapis.com
    gcloud services enable cloudkms.googleapis.com
    gcloud services enable resourcesettings.googleapis.com 
    gcloud services enable artifactregistry.googleapis.com 
    gcloud services enable cloudbuild.googleapis.com
    gcloud services enable run.googleapis.com
    gcloud services enable dataplex.googleapis.com
    gcloud services enable containerregistry.googleapis.com
    gcloud services enable iam.googleapis.com
    # Required for tag engine
    gcloud services enable cloudresourcemanager.googleapis.com
    gcloud services enable firestore.googleapis.com
    gcloud services enable cloudtasks.googleapis.com
    gcloud services enable datacatalog.googleapis.com
    gcloud services enable cloudscheduler.googleapis.com
done

#####################################
# Infrastructure for the DATA project
#####################################
gcloud config set project $PROJECT_ID

# Create the GCS bucket for data
gcloud storage buckets create gs://${GCS_BUCKET_TPCDI}

# Create the KMS
gcloud kms keyrings create ${KMS_KEYRING} --location ${REGION}
gcloud kms keys create ${KMS_KEYNAME} \
    --keyring ${KMS_KEYRING} \
    --location ${REGION} \
    --purpose "encryption"
    #--protection-level "hsm" #uncomment for HSM

# Grant permission to the BQ SA
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:bq-${PROJECT_NUMBER}@bigquery-encryption.iam.gserviceaccount.com \
  --role=roles/cloudkms.cryptoKeyEncrypterDecrypter

###########################################
# Infrastructure for the GOVERNANCE project
###########################################
gcloud config set project $PROJECT_ID_GOV

# Create the CloudDQ dataset
bq --location=${REGION} mk ${PROJECT_ID_GOV}:${CLOUDDQ_BIGQUERY_DATASET}

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

# Grant the CE Data Governance SA access to the Data project
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${PROJECT_NUMBER_GOV}-compute@developer.gserviceaccount.com \
  --role=roles/bigquery.user
gcloud projects add-iam-policy-binding ${PROJECT_ID} \
  --member=serviceAccount:${PROJECT_NUMBER_GOV}-compute@developer.gserviceaccount.com \
  --role=roles/bigquery.dataViewer
