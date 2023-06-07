#!/bin/bash

# Copyright 2023 The Reg Reporting Blueprint Authors

# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

pushd ../
source environment-variables.sh
popd

# [OPTIONAL] Build the container locally
# docker build -t cloud-dq .

# [OPTIONAL] Run the container locally mapping the folder with the ADC token
# Note you have to provide parameters as follows
#  1: project_id where the data resides
#  2: project_id of the data governance, where DQ runs 
#  3: region where DQ runs 
#  4: dataset used to store the DQ results
# docker run -v $HOME/.config/gcloud:/root/.config/gcloud cloud-dq $PROJECT_ID $PROJECT_ID_GOV $REGION $CLOUDDQ_BIGQUERY_DATASET

# Submit to the registry on GCP and deploy to cloud run

# Make sure operations happen on the governance project
gcloud config set project $PROJECT_ID_GOV

# Build a cloud-dq image and send to GCR
gcloud builds submit --tag gcr.io/$PROJECT_ID_GOV/cdmc-dq .

# Create a job in Cloud Run. Note parameters have to be passed here
gcloud run jobs delete cloud-dq --region $REGION --quiet
gcloud run jobs create cloud-dq --image gcr.io/$PROJECT_ID_GOV/cdmc-dq --region $REGION --args $PROJECT_ID,$PROJECT_ID_GOV,$REGION,$CLOUDDQ_BIGQUERY_DATASET

# Execute on cloud run
gcloud run jobs execute cloud-dq --region $REGION