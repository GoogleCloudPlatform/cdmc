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


## Terraform setup
pushd terraform
## Create a copy of the terraform variables and substitute values
cp terraform.tfvars.template terraform.tfvars
sed -i "s/<PROJECT_ID_GOV>/$PROJECT_ID_GOV/" terraform.tfvars
sed -i "s/<ORGANIZATION_ID>/$ORGANIZATION_ID/" terraform.tfvars
sed -i "s/<REGION>/$REGION/" terraform.tfvars
popd

## Cloud run setup
pushd resources
## Create a copy of the config.ini.example and substitute values
cp config.ini.example config.ini
sed -i "s/<PROJECT_ID_GOV>/$PROJECT_ID_GOV/" config.ini
sed -i "s/<REGION>/$REGION/" config.ini
popd
#