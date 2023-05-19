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

terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.64.0"
    }
  }
}

resource "google_project_service" "project-services" {
  project = var.project
  count   = length(var.gcp_services)
  service = var.gcp_services[count.index]
  disable_dependent_services = true
}

data "google_project" "project" {}

resource "google_service_account" "sa-report-engine" {
  account_id = "sa-report-engine"
  display_name = "sa-report-engine"
  description = "SA used for CDMC report engine execution"
  project = var.project
}

resource "google_organization_iam_binding" "organization-bq-resourceViewer" {
  org_id  = var.organization
  role    = "roles/bigquery.resourceViewer"
  members  = ["serviceAccount:${google_service_account.sa-report-engine.email}"]
}

resource "google_organization_iam_binding" "organization-bq-metadataViewer" {
  org_id  = var.organization
  role    = "roles/bigquery.metadataViewer"
  members  = ["serviceAccount:${google_service_account.sa-report-engine.email}"]
}

resource "google_organization_iam_binding" "organization-datacatalog-viewer" {
  org_id  = var.organization
  role    = "roles/datacatalog.viewer"
  members  = ["serviceAccount:${google_service_account.sa-report-engine.email}"]
}

resource "google_organization_iam_binding" "organization-datalineage-viewer" {
  org_id  = var.organization
  role    = "roles/datalineage.viewer"
  members  = ["serviceAccount:${google_service_account.sa-report-engine.email}"]
}

resource "google_project_iam_member" "project-bigquery-dataEditor" {
  project = var.project
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.sa-report-engine.email}"
}

resource "google_project_iam_member" "project-bigquery-jobUser" {
  project = var.project
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.sa-report-engine.email}"
}

resource "google_project_iam_member" "project-pubsub-publisher" {
  project = var.project
  role    = "roles/pubsub.publisher"
  member  = "serviceAccount:${google_service_account.sa-report-engine.email}"
}

resource "google_project_iam_member" "default-pubsub-bq-viewer" {
  project = var.project
  role   = "roles/bigquery.metadataViewer"
  member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

resource "google_project_iam_member" "default-pubsub-bq-editor" {
  project = var.project
  role   = "roles/bigquery.dataEditor"
  member = "serviceAccount:service-${data.google_project.project.number}@gcp-sa-pubsub.iam.gserviceaccount.com"
}

resource "google_pubsub_schema" "pubsub-schema-cdmc-event" {
  name = "CDMC_Event"
  type = "AVRO"
  definition = "{\"type\": \"record\",\"name\": \"CDMC_Event\",\"fields\": [{\"name\": \"reportMetadata\",\"type\": {\"type\": \"record\",\"name\": \"Identifier\",\"fields\": [{\"name\": \"uuid\",\"type\": \"string\"},{\"name\": \"Controls\",\"type\": \"string\"}]}},{\"name\": \"CdmcControlNumber\",\"type\": \"int\"},{\"name\": \"Findings\",\"type\": \"string\"},{\"name\": \"DataAsset\",\"type\": \"string\"},{\"name\": \"RecommendedAdjustment\",\"type\": \"string\"},{\"name\": \"ExecutionTimestamp\",\"type\": \"string\"}]}"
}

resource "google_pubsub_topic" "cdmc-controls-topic" {
  name = "cdmc-controls-topic"

  depends_on = [google_pubsub_schema.pubsub-schema-cdmc-event]
  schema_settings {
    schema = join("/",["projects",var.project,"schemas","CDMC_Event"])
    encoding = "JSON"
  }
}

resource "google_pubsub_schema" "pubsub-schema-cdmc-data-assets" {
  name = "CDMC_Data_Assets"
  type = "AVRO"
  definition = "{\"type\": \"record\",\"name\": \"CDMC_Data_Assets\",\"fields\": [{\"name\": \"event_uuid\",\"type\": \"string\"},{\"name\": \"asset_name\",\"type\": \"string\"},{\"name\": \"sensitive\",\"type\": \"boolean\"},{\"name\": \"event_timestamp\",\"type\": \"string\"}]}"
}

resource "google_pubsub_topic" "cdmc-data-assets-topic" {
  name = "cdmc-data-assets-topic"

  depends_on = [google_pubsub_schema.pubsub-schema-cdmc-data-assets]
  schema_settings {
    schema = join("/",["projects",var.project,"schemas","CDMC_Data_Assets"])
    encoding = "JSON"
  }
}

resource "google_bigquery_dataset" "dataset-cdmc-report" {
  dataset_id                  = "cdmc_report"
  friendly_name               = "cdmc_report"
  description                 = "Dataset that stores report engine findings and data assets log"
  location                    = "us-central1"
  project = var.project

  labels = {
    env = "cdmc"
  }
}

resource "google_bigquery_table" "table-events" {
  dataset_id = google_bigquery_dataset.dataset-cdmc-report.dataset_id
  table_id   = "events"
  project = var.project

  time_partitioning {
    type = "DAY"
    field = "ExecutionTimestamp"
  }

  labels = {
    env = "cdmc"
  }

  schema = <<EOF
[
  {
    "fields": [
      {
        "name": "uuid",
        "type": "STRING"
      },
      {
        "name": "Controls",
        "type": "STRING"
      }
    ],
    "name": "reportMetadata",
    "type": "RECORD"
  },
  {
    "name": "CdmcControlNumber",
    "type": "INTEGER"
  },
  {
    "name": "Findings",
    "type": "STRING"
  },
  {
    "name": "DataAsset",
    "type": "STRING"
  },
  {
    "name": "RecommendedAdjustment",
    "type": "STRING"
  },
  {
    "name": "ExecutionTimestamp",
    "type": "TIMESTAMP"
  }
]
EOF

}

resource "google_bigquery_table" "table-data-assets" {
  dataset_id = google_bigquery_dataset.dataset-cdmc-report.dataset_id
  table_id   = "data_assets"
  project = var.project

  time_partitioning {
    type = "DAY"
    field="event_timestamp"
  }

  labels = {
    env = "cdmc"
  }

  schema = <<EOF
[
  {
    "mode": "NULLABLE",
    "name": "event_uuid",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "asset_name",
    "type": "STRING"
  },
  {
    "mode": "NULLABLE",
    "name": "event_timestamp",
    "type": "TIMESTAMP"
  },
  {
    "mode": "NULLABLE",
    "name": "sensitive",
    "type": "BOOLEAN"
  }
]
EOF

}

resource "google_pubsub_subscription" "cdmc-controls-topic-bq-sub" {
  name  = "cdmc-controls-topic-bq-sub"
  topic = google_pubsub_topic.cdmc-controls-topic.name

  bigquery_config {
    table = "${google_bigquery_table.table-events.project}.${google_bigquery_table.table-events.dataset_id}.${google_bigquery_table.table-events.table_id}"
    use_topic_schema = true
  }

  depends_on = [google_project_iam_member.default-pubsub-bq-viewer, google_project_iam_member.default-pubsub-bq-editor]
}

resource "google_pubsub_subscription" "cdmc-data-assets-topic-bq-sub" {
  name  = "cdmc-data-assets-topic-bq-sub"
  topic = google_pubsub_topic.cdmc-data-assets-topic.name

  bigquery_config {
    table = "${google_bigquery_table.table-data-assets.project}.${google_bigquery_table.table-data-assets.dataset_id}.${google_bigquery_table.table-data-assets.table_id}"
    use_topic_schema = true
  }

  depends_on = [google_project_iam_member.default-pubsub-bq-viewer, google_project_iam_member.default-pubsub-bq-editor]
}
