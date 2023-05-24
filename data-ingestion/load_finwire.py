from google.cloud import bigquery
from google.cloud import storage
import LineageManager as lineage
import datetime

BIGQUERY_PROJECT = 'sdw-conf-b1927e-bcc1' # replace with your project
BIGQUERY_PROJECT_NUMBER = 707062315533    # replace with your project
BIGQUERY_REGION = 'us-central1'           # replace with your region
BIGQUERY_DATASET = 'finwire'
TPCDI_URL = 'https://www.tpc.org'
GCS_BUCKET = 'tpcdi-data'                 # replace with bucket
GCS_FOLDERS = 'finwire'                   # replace with folder path

bq_client = bigquery.Client(project=BIGQUERY_PROJECT, location=BIGQUERY_REGION)
gcs_client = storage.Client()

def create_dataset():
    
    bq_client.create_dataset(BIGQUERY_DATASET, exists_ok=True)

def create_load_job(uri, table_id, schema):
	
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        field_delimiter=',',
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
    uri = 'gs://' + GCS_BUCKET + '/' + filename
    table_id = BIGQUERY_PROJECT + '.' + BIGQUERY_DATASET + '.' + table
    job_id = create_load_job(uri, table_id, schema)
    end_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    
    lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Data Download', 'load_finwire.csv', 'Data Download', start_time, end_time, TPCDI_URL, uri)
    lm.create_lineage()
    
    #lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Load Job', 'load_finwire.csv', job_id, start_time, end_time, uri, 'bigquery:' + table_id)
    #lm.create_lineage()
    
    #lm.retrieve_lineage()
 

def load_sec_tables():
    
    blobs = gcs_client.list_blobs(GCS_BUCKET, prefix=GCS_FOLDERS)

    for blob in blobs:
        
        if blob.name.endswith('_SEC.csv') == False:
            continue
            
        filename = blob.name
        table = blob.name.split('/')[1].replace('_SEC.csv', '_SEC')
        schema = [
                    bigquery.SchemaField('pts', 'STRING'),
                    bigquery.SchemaField('recType', 'STRING'),
                    bigquery.SchemaField('issueType', 'STRING'),
                    bigquery.SchemaField('status', 'STRING'),
                    bigquery.SchemaField('name', 'STRING'),
                    bigquery.SchemaField('exId', 'STRING'),
                    bigquery.SchemaField('shOut', 'STRING'),
                    bigquery.SchemaField('firstTradeDate', 'DATE'),
                    bigquery.SchemaField('firstTradeExchg', 'STRING'),
                    bigquery.SchemaField('dividend', 'NUMERIC'),
                    bigquery.SchemaField('coNameOrCIK', 'STRING'),
                ]
         
        load_table(filename, table, schema)


def load_fin_tables():
    
    blobs = gcs_client.list_blobs(GCS_BUCKET, prefix=GCS_FOLDERS)

    for blob in blobs:
        
        if blob.name.endswith('_FIN.csv') == False:
            continue
            
        filename = blob.name
        table = blob.name.split('/')[1].replace('_FIN.csv', '_FIN')
        schema = [
                    bigquery.SchemaField('pts', 'STRING'),
                    bigquery.SchemaField('recType', 'STRING'),
                    bigquery.SchemaField('year', 'INTEGER'),
                    bigquery.SchemaField('quarter', 'INTEGER'),
                    bigquery.SchemaField('qtrStartDate', 'DATE'),
                    bigquery.SchemaField('postingDate', 'DATE'),
                    bigquery.SchemaField('revenue', 'NUMERIC'),
                    bigquery.SchemaField('earnings', 'NUMERIC'),
                    bigquery.SchemaField('eps', 'NUMERIC'),
                    bigquery.SchemaField('diluted_eps', 'NUMERIC'),
                    bigquery.SchemaField('margin', 'NUMERIC'),
                    bigquery.SchemaField('inventory', 'NUMERIC'),
                    bigquery.SchemaField('assets', 'NUMERIC'),
                    bigquery.SchemaField('liabilities', 'NUMERIC'),
                    bigquery.SchemaField('shOut', 'NUMERIC'),
                    bigquery.SchemaField('dilutedShOut', 'NUMERIC'),
                    bigquery.SchemaField('coNameOrCIK', 'STRING'),
                ]
         
        load_table(filename, table, schema)


def load_cmp_tables():
    
    blobs = gcs_client.list_blobs(GCS_BUCKET, prefix=GCS_FOLDERS)

    for blob in blobs:
        
        if blob.name.endswith('_CMP.csv') == False:
            continue
            
        filename = blob.name
        table = blob.name.split('/')[1].replace('_CMP.csv', '_CMP')
        schema = [
                    bigquery.SchemaField('pts', 'STRING'),
                    bigquery.SchemaField('recType', 'STRING'),
                    bigquery.SchemaField('companyName', 'STRING'),
                    bigquery.SchemaField('cik', 'STRING'),
                    bigquery.SchemaField('status', 'STRING'),
                    bigquery.SchemaField('industryID', 'STRING'),
                    bigquery.SchemaField('spRating', 'STRING'),
                    bigquery.SchemaField('foundingDate', 'DATE'),
                    bigquery.SchemaField('addr_line1', 'STRING'),
                    bigquery.SchemaField('addr_line2', 'STRING'),
                    bigquery.SchemaField('postalCode', 'STRING'),
                    bigquery.SchemaField('city', 'STRING'),
                    bigquery.SchemaField('stateProvince', 'STRING'),
                    bigquery.SchemaField('country', 'STRING'),
                    bigquery.SchemaField('ceoName', 'STRING'),
                    bigquery.SchemaField('description', 'STRING'),
                ]
         
        load_table(filename, table, schema)


def load_finwire():
    create_dataset()
    load_sec_tables()
    load_fin_tables()
    load_cmp_tables()
        
        
if __name__ == '__main__':
    load_finwire()