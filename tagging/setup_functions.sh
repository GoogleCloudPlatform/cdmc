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


# This script creates a Python Cloud Function with requirements.txt and main.py
# in each of the subfolder in the /remote_functions folder.
# Function names are consistent with folder names

# Environment variables
pushd remote_functions/bytes_transferred
#Create the Cloud Function
gcloud functions deploy get_bytes_transferred \
--runtime python37 \
--trigger-http \
--no-allow-unauthenticated \
--ingress-settings internal-and-gclb \
--entry-point event_handler \
--source ./function \
--set-env-vars REGION=$REGION,PROJECT_ID_DATA=$PROJECT_ID_DATA

source ./create_remote_function.sh
popd

pushd remote_functions/location_policy
#Create the Cloud Function
gcloud functions deploy get_location_policy \
--runtime python37 \
--trigger-http \
--no-allow-unauthenticated \
--ingress-settings internal-and-gclb \
--entry-point event_handler \
--source ./function \
--set-env-vars REGION=$REGION,PROJECT_ID_DATA=$PROJECT_ID_DATA

source ./create_remote_function.sh
popd

pushd remote_functions/masking_rule
#Create the Cloud Function
gcloud functions deploy get_masking_rule \
--runtime python37 \
--trigger-http \
--no-allow-unauthenticated \
--ingress-settings internal-and-gclb \
--entry-point event_handler \
--source ./function \
--set-env-vars REGION=$REGION,PROJECT_ID_DATA=$PROJECT_ID_DATA

source ./create_remote_function.sh
popd

pushd remote_functions/table_encryption_method
#Create the Cloud Function
gcloud functions deploy get_table_encryption_method \
--runtime python37 \
--trigger-http \
--no-allow-unauthenticated \
--ingress-settings internal-and-gclb \
--entry-point event_handler \
--source ./function \
--set-env-vars REGION=$REGION,PROJECT_ID_DATA=$PROJECT_ID_DATA

source ./create_remote_function.sh
popd

pushd remote_functions/ultimate_source
#Create the Cloud Function
gcloud functions deploy get_ultimate_source \
--runtime python37 \
--trigger-http \
--no-allow-unauthenticated \
--ingress-settings internal-and-gclb \
--entry-point process_request \
--source ./function \
--set-env-vars REGION=$REGION,PROJECT_ID_DATA=$PROJECT_ID_DATA

source ./create_remote_function.sh
popd
