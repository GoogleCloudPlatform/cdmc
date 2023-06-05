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

from google.cloud import bigquery
import LineageManager as lineage
import datetime
import os

class DataLoader():
    """
    Utility class that allows to load the data to BigQuery, recording lineage events during the load.
    The following environment variables have to be set for this to work correctly:
     * BIGQUERY_PROJECT: The GCP project where the data is loaded
     * BIGQUERY_PROJECT_NUMBER: The GCP Project Number where the data is loaded
     * BIGQUERY_REGION: The BQ region where the data is loaded
     * GCS_PATH_PREFIX: A GCS bucket address
     * KMS_KEY: a valid KMS key to encrypt the data
    
    """
    def __init__(self):
        # Read main config from environment variables
        self.BIGQUERY_PROJECT = os.getenv('PROJECT_ID')
        self.BIGQUERY_PROJECT_NUMBER = os.getenv('PROJECT_NUMBER')
        self.BIGQUERY_REGION = os.getenv('REGION')
        self.GCS_PATH_PREFIX = f"gs://{os.getenv('GCS_BUCKET_TPCDI')}/staging"
        self.KMS_KEY = os.getenv('KMS_KEY')

        # Static variables
        self.TPCDI_URL = 'https://www.tpc.org'

        # Initialise the BQ client
        self.bq_client = bigquery.Client(project=self.BIGQUERY_PROJECT, 
                                         location=self.BIGQUERY_REGION)

    def delete_create_dataset(self, dataset_name:str):
        try:
            self.bq_client.delete_dataset(
                dataset_name, 
                delete_contents=True, 
                not_found_ok=True)
            self.bq_client.create_dataset(dataset_name, 
                                          exists_ok=False)
        except Exception as e:
            print('Error occurred during delete_create_dataset:', e)


    def create_table(self, table_id):
        table = bigquery.Table(table_id)
        table.encryption_configuration = bigquery.EncryptionConfiguration(
            kms_key_name=self.KMS_KEY
        )
        table = self.bq_client.create_table(table)
        print(f"\n\nCreated {table_id}.")


    def create_load_job(self, uri, table_id, schema, field_delimiter=","):
        job_config = bigquery.LoadJobConfig(
            schema=schema,
            source_format=bigquery.SourceFormat.CSV,
            field_delimiter=field_delimiter,
            write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE,
            destination_encryption_configuration=bigquery.EncryptionConfiguration(
                kms_key_name=self.KMS_KEY)
        )

        load_job = self.bq_client.load_table_from_uri(uri, 
                                                      table_id, 
                                                      job_config=job_config)
        job_id = load_job.job_id
        load_job.result()
        destination_table = self.bq_client.get_table(table_id)
        print('*** Loaded {} rows '.format(destination_table.num_rows),
            'with job_id', job_id, '***')

        return job_id


    def load_table(self,
                   filename:str,
                   dataset:str,
                   table:str,
                   schema:str,
                   origin_name:str,
                   process_name="Data Download",
                   job_id='Data Download',
                   field_delimiter=','):
        """_summary_

        Args:
            filename (str): the file to load the data from
            table (str): the table to load the data to
            schema (str): the schema of the table
            origin_name (str): the origin of the data to store in the lineage
            process_name (str, optional): Name of the process that loaded the data. Defaults to "Data Download".
            job_id (str, optional): JobID for the data load. Defaults to 'Data Download'.
            field_delimiter (str, optional): the field delimiter to use 
        """
        start_time = datetime.datetime.now().replace(
            tzinfo=datetime.timezone.utc).isoformat()
        uri = self.GCS_PATH_PREFIX + '/' + dataset + '/' + filename
        table_id = self.BIGQUERY_PROJECT + '.' + dataset + '.' + table
        self.create_table(table_id)

        job_id = self.create_load_job(uri, table_id, schema, field_delimiter=field_delimiter)
        end_time = datetime.datetime.now().replace(
            tzinfo=datetime.timezone.utc).isoformat()

        lmd = lineage.LineageManager(project_number=self.BIGQUERY_PROJECT_NUMBER, 
                                     storage_region=self.BIGQUERY_REGION, 
                                     process_name=process_name, 
                                     origin_name=origin_name, 
                                     job_id=job_id, 
                                     start_time=start_time, 
                                     end_time=end_time,
                                     source=self.TPCDI_URL, 
                                     target=uri)
        lmd.create_lineage()
        lmd = None


