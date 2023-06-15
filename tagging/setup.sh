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


# This script installs the dependencies and 
# then runs the script to create the tag templates.

# Environment variables
pushd ../
source environment-variables.sh
popd

# Create Data Catalog tag templates and policy tag taxonomy
echo -e "#### Part 1: Data Catalog tag templates and policy tag taxonomy"
echo -e "1. Create the Data Catalog tag templates"

pushd tag_templates
pip install -r requirements.txt
python create_template.py $PROJECT_ID $REGION cdmc_controls.yaml
python create_template.py $PROJECT_ID $REGION completeness_template.yaml
python create_template.py $PROJECT_ID $REGION correctness_template.yaml
python create_template.py $PROJECT_ID $REGION cost_metrics.yaml
python create_template.py $PROJECT_ID $REGION data_sensitivity.yaml
python create_template.py $PROJECT_ID $REGION impact_assessment.yaml
python create_template.py $PROJECT_ID $REGION security_policy.yaml
python create_template.py $PROJECT_ID $REGION uniqueness_template.yaml
popd

echo -e "2. Create the policy tag taxonomy"
pushd policy_tags

## Create a copy of the taxonomy.yaml variables and substitute variables
cp taxonomy.yaml.example taxonomy.yaml
sed -i "s/<PROJECT_ID_GOV>/$PROJECT_ID_GOV/" taxonomy.yaml
sed -i "s/<REGION>/$REGION/" taxonomy.yaml
sed -i "s/<AUTHENTICATED_USER>/$AUTHENTICATED_USER/" taxonomy.yaml

# Execute scripts
pip install -r requirements.txt
python create_policy_tag_taxonomy.py taxonomy.yaml
popd


echo -e "#### Part 2: Policy tables and remote functions"
echo -e "Create and populate the policy tables"

# Appply the tax templates
gcloud config set project $PROJECT_ID_GOV
bq mk --location=$REGION --dataset data_classification
bq mk --location=$REGION --dataset data_retention
bq mk --location=$REGION --dataset impact_assessment
bq mk --location=$REGION --dataset entitlement_management
bq mk --location=$REGION --dataset security_policy
bq mk --location=$REGION --dataset remote_functions

# Create the tables
pushd ddl
bq query --use_legacy_sql=false < create_data_classification_tables.sql
bq query --use_legacy_sql=false < create_data_retention_tables.sql
bq query --use_legacy_sql=false < create_impact_assessment_tables.sql
bq query --use_legacy_sql=false < create_populate_entitlement_tables.sql
bq query --use_legacy_sql=false < create_security_policy_tables.sql
bq query --use_legacy_sql=false < information_schema_view.sql
popd