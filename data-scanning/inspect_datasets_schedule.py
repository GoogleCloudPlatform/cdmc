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

from google.cloud import dlp_v2
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import os
import argparse
import subprocess
import requests


# Get project values from environment variables

region = os.getenv('REGION')
inspect_project = os.getenv('PROJECT_ID_DATA')
inspect_datasets = ['crm', 'hr', 'oltp','reference', 'sales']

result_project = os.getenv('PROJECT_ID_GOV')
result_datasets = ['crm_dlp','hr_dlp', 'oltp_dlp','reference_dlp', 'sales_dlp']

bq_client = bigquery.Client(project=inspect_project)
bq_client_results = bigquery.Client(project=result_project)
dlp_client = dlp_v2.DlpServiceClient()
parent = dlp_client.common_project_path(result_project)

def get_access_token():
    """
    Get the access token from Google Cloud.
    """

    command = ["gcloud", "auth", "print-access-token"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE)
    output, err = process.communicate()

    if err:
        raise Exception(err)

    return output.decode('utf-8').strip()

def inspect(scan_period_days):

    token = get_access_token()

    for index, inspect_dataset in enumerate(inspect_datasets):
        tables = bq_client.list_tables(inspect_project + '.' + inspect_dataset)

        for table in tables:
            print("scanning {}.{}.{}".format(table.project, table.dataset_id, table.table_id))
            start_job(inspect_dataset, table.table_id, result_datasets[index],scan_period_days, token)

def start_job(inspect_dataset, table, result_dataset,scan_period_days, token):

    recurrence_period_duration = scan_period_days * 60 * 60 * 24
    if recurrence_period_duration == 0: recurrence_period_duration = 86400 #min value for recurance is 1 day, 0 indicates run immediately

    inspect_job_data = {
        'storage_config': {
            'big_query_options': {
                'table_reference': {
                    'project_id': inspect_project,
                    'dataset_id': inspect_dataset,
                    'table_id': table
                }
            }
        },
        'inspect_config': {
            "info_types": [
              {
                "name": "CREDIT_CARD_NUMBER"
              },
              {
                "name": "EMAIL_ADDRESS"
              },
              {
                "name": "STREET_ADDRESS"
              },
              {
                "name": "PHONE_NUMBER"
              },
              {
                "name": "PERSON_NAME"
              },
              {
                "name": "FIRST_NAME"
              },
              {
                "name": "LAST_NAME"
              },
              {
                "name": "GENDER"
              },
              {
                "name": "DATE_OF_BIRTH"
              },
              {
                "name": "AGE"
              },
              {
                "name": "ETHNIC_GROUP"
              },
              {
                "name": "LOCATION_COORDINATES"
              },
              {
                "name": "IP_ADDRESS"
              }
            ],
             "min_likelihood": "LIKELY",
        },
        'actions': [
            {
                'save_findings': {
                    'output_config':{
                        'table':{
                            'project_id': result_project,
                            'dataset_id': result_dataset,
                            'table_id': table
                        }
                    }

                },
            },
        ]
    }

    schedule = {
        "recurrence_period_duration": {"seconds": recurrence_period_duration}
    }

    job_trigger = {
        "inspect_job": inspect_job_data,
        "display_name": table,
        "description": "CDMC inspection job",
        "triggers": [{"schedule": schedule}],
        "status": dlp_v2.JobTrigger.Status.HEALTHY,
    }

    # If jobs to run immediatly (days=0), run the jobs else create a trigger with schedule
    if scan_period_days == 0:
        response = dlp_client.create_dlp_job(parent=(parent), inspect_job=(inspect_job_data))
        print(f"Successfully started job {response.name}")
    else:
        response = dlp_client.create_job_trigger(
            request={"parent": parent, "job_trigger": job_trigger}
        )
        print(f"Successfully created trigger {response.name}")

def create_output_datasets():
    for dataset in result_datasets:
        try:
            bq_client_results.get_dataset(dataset)  # Checks if dataset exists.
            print(f'Dataset {dataset} already exists')
        except NotFound:
            bq_client_results.create_dataset(dataset)  # Creates dataset if it doesn't exist.
            print(f'Created results dataset {dataset}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--scan_period_days", help="The number of days to scan for data loss.", type=int)
    args = parser.parse_args()

    create_output_datasets()
    inspect(scan_period_days=args.scan_period_days)
