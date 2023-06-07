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

FROM python:3.9

# Install production dependencies.
RUN pip install -U pip
RUN pip install             \
    dbt-bigquery>=1.3.0     \
    dbt-core>=1.3.1         \
    dbt-extractor>=0.4.1

# Copy files to the image
RUN mkdir /cloud-dq/
COPY . ./cloud-dq/
WORKDIR /cloud-dq/
RUN chmod +x run_dq_engine.sh

# Download cloud-dq binaries
ENV CLOUDDQ_RELEASE_VERSION "1.0.8"
ENV TARGET_OS "debian_11"
ENV TARGET_PYTHON_INTERPRETER "3.9"
RUN wget -O clouddq_executable.zip https://github.com/GoogleCloudPlatform/cloud-data-quality/releases/download/v"${CLOUDDQ_RELEASE_VERSION}"/clouddq_executable_v"${CLOUDDQ_RELEASE_VERSION}"_"${TARGET_OS}"_python"${TARGET_PYTHON_INTERPRETER}".zip

# Entrypoint to execute cloud dq
ENTRYPOINT ["./run_dq_engine.sh"]
