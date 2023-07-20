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
# then runs the script to run the DLP inspection immediately.

# Install virtual environment and activate
python3 -m venv .venvdlp
source .venvdlp/bin/activate

# Install dependancies
pip install -r requirements.txt


# Run Inspection now
python3 inspect_datasets_schedule.py --scan_period_days 0




  


