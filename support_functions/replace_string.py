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

import os
import re

def replace_region(directory, search_string, replace_string, file_type):
  for file_name in os.listdir(directory):
    if file_name.endswith(file_type):
      with open(os.path.join(directory, file_name), "r") as f:
        data = f.read()

      data = re.sub(search_string, replace_string, data)

      with open(os.path.join(directory, file_name), "w") as f:
        f.write(data)

if __name__ == "__main__":
  import sys
  directory = sys.argv[1]
  search_string = sys.argv[2]
  replace_string = sys.argv[3]
  file_type = sys.argv[4]

  replace_region(directory, search_string, replace_string, file_type)