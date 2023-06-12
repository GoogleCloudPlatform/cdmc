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


# This script creates a pythnon virtual environment installs the dependencies and 
# then runs the script to create the tag templates.

# Install virtual environment and activate
python3 -m venv .venvtagging
source .venvdlp/bin/activate

# Install dependancies
pip install -r requirements.txt


# Run inspection 
cd tag_templates
pip install -r requirements.txt
python create_template.py PROJECT REGION cdmc_controls.yaml
python create_template.py PROJECT REGION completeness_template.yaml
python create_template.py PROJECT REGION correctness_template.yaml
python create_template.py PROJECT REGION cost_metrics.yaml
python create_template.py PROJECT REGION data_sensitivity.yaml
python create_template.py PROJECT REGION impact_assessment.yaml
python create_template.py PROJECT REGION security_policy.yaml
python create_template.py PROJECT REGION uniqueness_template.yaml
cd ..




  


