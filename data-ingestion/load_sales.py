from google.cloud import bigquery
import datetime
import LineageManager as lineage

BIGQUERY_PROJECT = 'sdw-conf-b1927e-bcc1' # replace with your project
BIGQUERY_PROJECT_NUMBER = 707062315533    # replace with your project
BIGQUERY_REGION = 'us-central1'           # replace with your region
BIGQUERY_DATASET = 'sales'
TPCDI_URL = 'https://www.tpc.org'
GCS_PATH_PREFIX = 'gs://tpcdi-data'       # replace with your bucket

bq_client = bigquery.Client(project=BIGQUERY_PROJECT, location=BIGQUERY_REGION)

def create_dataset():
    
    bq_client.create_dataset(BIGQUERY_DATASET, exists_ok=True)

def create_load_job(uri, table_id, schema):
	
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE
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
    job_id = create_load_job(uri, table_id, schema)
    end_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    
    lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Data Download', 'load_sales.py', 'Data Download', start_time, end_time, TPCDI_URL, uri)
    lm.create_lineage()
    
    #lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Load Job', 'load_sales.py', job_id, start_time, end_time, uri, 'bigquery:' + table_id)
    #lm.create_lineage()
    
    #lm.retrieve_lineage()
 

def load_prospect():
    
    filename = 'Prospect*.csv'
    table = 'Prospect'
    schema = [
                bigquery.SchemaField('agencyID', 'STRING'),
                bigquery.SchemaField('lastName', 'STRING'),
                bigquery.SchemaField('firstName', 'STRING'),
                bigquery.SchemaField('middleInitial', 'STRING'),
                bigquery.SchemaField('gender', 'STRING'),
                bigquery.SchemaField('addressLine1', 'STRING'),
                bigquery.SchemaField('addressLine2', 'STRING'),
                bigquery.SchemaField('postalCode', 'STRING'),
                bigquery.SchemaField('city', 'STRING'),
                bigquery.SchemaField('state', 'STRING'),
                bigquery.SchemaField('country', 'STRING'),
                bigquery.SchemaField('phone', 'STRING'),
                bigquery.SchemaField('income', 'INTEGER'),
                bigquery.SchemaField('numberCars', 'INTEGER'),
                bigquery.SchemaField('numberChildren', 'INTEGER'),
                bigquery.SchemaField('maritalStatus', 'STRING'),
                bigquery.SchemaField('age', 'INTEGER'),
                bigquery.SchemaField('creditRating', 'INTEGER'),
                bigquery.SchemaField('ownOrRentFlag', 'STRING'),
                bigquery.SchemaField('employer', 'STRING'),
                bigquery.SchemaField('numberCreditCards', 'INTEGER'),
                bigquery.SchemaField('netWorth', 'INTEGER'),
            ]
    load_table(filename, table, schema)

    
if __name__ == '__main__':
    create_dataset()
    load_prospect()