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
import datetime
import LineageManager as lineage

BIGQUERY_PROJECT = 'sdw-conf-b1927e-bcc1' # replace with your project
BIGQUERY_PROJECT_NUMBER = 707062315533    # replace with your project
BIGQUERY_REGION = 'us-central1'           # replace with your region
BIGQUERY_DATASET = 'hr'
TPCDI_URL = 'https://www.tpc.org'
GCS_PATH_PREFIX = 'gs://tpcdi-data'      # replace with your bucket

KMS_KEY = 'projects/sdw-data-gov-b1927e-dd69/locations/us-central1/keyRings/cmek-keyring-bigquery/cryptoKeys/cmek-bigquery-key' 
           # replace with your key name 

bq_client = bigquery.Client(project=BIGQUERY_PROJECT, location=BIGQUERY_REGION)


def delete_create_dataset():
    
    try:
        bq_client.delete_dataset(BIGQUERY_DATASET, delete_contents=True, not_found_ok=True)
        bq_client.create_dataset(BIGQUERY_DATASET, exists_ok=False)
        
    except Exception as e:
        print('Error occurred during delete_create_dataset:', e)


def create_table(table_id):
    
    table = bigquery.Table(table_id)
    table.encryption_configuration = bigquery.EncryptionConfiguration(
        kms_key_name=KMS_KEY
    )
    table = bq_client.create_table(table)

    print(f"Created {table_id}.")


def create_load_job(uri, table_id, schema):
	
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE,
        destination_encryption_configuration=bigquery.EncryptionConfiguration(kms_key_name=KMS_KEY),
    )

    load_job = bq_client.load_table_from_uri(uri, table_id, job_config=job_config) 
    job_id = load_job.job_id
    load_job.result()  
    destination_table = bq_client.get_table(table_id)  
    print('Loaded {} rows'.format(destination_table.num_rows), 'with job_id', job_id)
    
    return job_id

def load_table(filename, table, schema):
    
    start_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    uri = GCS_PATH_PREFIX + '/' + BIGQUERY_DATASET + '/' + filename
    table_id = BIGQUERY_PROJECT + '.' + BIGQUERY_DATASET + '.' + table
    create_table(table_id)
    job_id = create_load_job(uri, table_id, schema)
    end_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    
    lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Data Download', 'load_hr.py', 'Data Download', start_time, end_time, TPCDI_URL, uri)
    lm.create_lineage()
    
    #lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Load Job', 'load_hr.py', job_id, start_time, end_time, uri, 'bigquery:' + table_id)
    #lm.create_lineage()
    
    #lm.retrieve_lineage()
 

def load_employee():
    
    filename = 'HR.csv'
    table = 'Employee'
    schema = [
                bigquery.SchemaField('employeeID', 'INTEGER'),
                bigquery.SchemaField('managerID', 'INTEGER'),
                bigquery.SchemaField('employeeFirstName', 'STRING'),
                bigquery.SchemaField('employeeLastName', 'STRING'),
                bigquery.SchemaField('employeeMI', 'STRING'),
                bigquery.SchemaField('employeeJobCode', 'INTEGER'),
                bigquery.SchemaField('employeeBranch', 'STRING'),
                bigquery.SchemaField('employeeOffice', 'STRING'),
                bigquery.SchemaField('employeePhone', 'STRING'),
            ]
    load_table(filename, table, schema)


if __name__ == '__main__':
    delete_create_dataset()
    load_employee()