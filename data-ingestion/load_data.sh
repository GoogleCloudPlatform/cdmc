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

## This script performs the basic setup for the projects 
## Including creating the required GCP services and setting up the 
## environment with the required dependencies


# Ensure environment variables are set
pushd
source environment-variables.sh
popd

# Unzip the data and load to GCS
echo -e "Loading TPC-DI data to gsutil: "
pushd tpcdi-data
declare -a DATASETS=(crm finwire hr oltp reference sales)
for d in "${DATASETS[@]}"
do
    :
    gsutil -m cp -r ${d}/ gs://${GCS_BUCKET_TPCDI}/staging/
done

# Remove the unzipped files 
#rm -r unzipped
popd

# Install python dependencies 
echo -e "\nInstalling python dependencies: "
python3 -m pip install -r requirements.txt 

# Load the data
echo -e "\nLoading data into BigQuery: "
python3 load_crm.py
python3 load_finwire.py
python3 load_hr.py
python3 load_oltp.py
python3 load_reference.py
python3 load_sales.py