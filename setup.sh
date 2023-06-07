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

# Activate the required APIs for all the projects)
gcloud config set project $PROJECT_ID
gcloud services enable datalineage.googleapis.com
gcloud services enable cloudkms.googleapis.com
gcloud services enable resourcesettings.googleapis.com
gcloud services enable dlp.googleapis.com 

gcloud config set project $PROJECT_ID_GOV
gcloud services enable dlp.googleapis.com

# Create the required components
gcloud config set project ${PROJECT_ID}
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

  


