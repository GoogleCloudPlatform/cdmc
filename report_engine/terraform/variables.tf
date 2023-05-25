/**
 * Copyright 2022 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

variable "organization" {
  type = string
  description = "The Organization ID"
  sensitive=false
}

variable "project" {
  type = string
  description = "The Project ID of the project where Report Engine will be deployed, not necessarily the inspected project"
  sensitive=false
}

variable "region" {
  type = string
  description = "The region where the Report Engine resources will be deployed"
  sensitive=false
}

variable "gcp_services" {
  type = list(string)
  default = [
    "datacatalog.googleapis.com",
    "bigquery.googleapis.com",
    "iam.googleapis.com",
    "pubsub.googleapis.com"
  ]
}