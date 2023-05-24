from google.cloud import bigquery
import LineageManager as lineage
import datetime

BIGQUERY_PROJECT = 'sdw-conf-b1927e-bcc1' # replace with your project
BIGQUERY_PROJECT_NUMBER = 707062315533    # replace with your project
BIGQUERY_REGION = 'us-central1'           # replace with your region
BIGQUERY_DATASET = 'crm'

TPCDI_URL = 'https://www.tpc.org'
GCS_PATH_PREFIX = 'gs://tpcdi-data'       # replace with your bucket
KMS_KEY = 'projects/sdw-data-gov-b1927e-dd69/locations/us-central1/keyRings/cmek-keyring-bigquery/cryptoKeys/cmek-bigquery-hsm-key'  # replace with your key name

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
        destination_encryption_configuration=bigquery.EncryptionConfiguration(kms_key_name=KMS_KEY)
    )

    load_job = bq_client.load_table_from_uri(uri, table_id, job_config=job_config) 
    job_id = load_job.job_id
    load_job.result()  
    destination_table = bq_client.get_table(table_id)  
    print('*** Loaded {} rows'.format(destination_table.num_rows), 'with job_id', job_id, '***')
    
    return job_id

def load_table(filename, table, schema):
    
    start_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    uri = GCS_PATH_PREFIX + '/' + BIGQUERY_DATASET + '/' + filename
    table_id = BIGQUERY_PROJECT + '.' + BIGQUERY_DATASET + '.' + table
    create_table(table_id)
    job_id = create_load_job(uri, table_id, schema)
    end_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    
    lmd = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Data Download', 'load_crm.py', 'Data Download', start_time, end_time, \
                                 TPCDI_URL, uri)
    lmd.create_lineage()
    lmd = None
    
    #lml = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Load Job', 'script_job_' + job_id, start_time, end_time, uri, 'bigquery:' + table_id)
    #lml.create_lineage()
    #lml = None
    #lm.retrieve_lineage()
 

def load_crm_add_acct():
    
    filename = 'AddAcct.csv'
    table = 'AddAcct'
    schema = [
                bigquery.SchemaField('action_ts', 'DATETIME'),
                bigquery.SchemaField('c_id', 'INTEGER'),
                bigquery.SchemaField('ca_id', 'INTEGER'),
                bigquery.SchemaField('ca_tax_st', 'INTEGER'),
                bigquery.SchemaField('ca_b_id', 'INTEGER'),
                bigquery.SchemaField('ca_name', 'STRING'),
            ]
    load_table(filename, table, schema)


def load_crm_inact_cust():
    
    filename = 'InactCust.csv'
    table = 'InactCust'
    schema = [
                bigquery.SchemaField('action_ts', 'DATETIME'),
                bigquery.SchemaField('c_id', 'INTEGER'),
            ]
    load_table(filename, table, schema)


def load_crm_upd_acct():
    
    filename = 'UpdAcct.csv'
    table = 'UpdAcct'
    schema = [
                bigquery.SchemaField('action_ts', 'DATETIME'),
                bigquery.SchemaField('c_id', 'INTEGER'),
                bigquery.SchemaField('ca_id', 'INTEGER'),
                bigquery.SchemaField('ca_tax_st', 'INTEGER'),
                bigquery.SchemaField('ca_b_id', 'INTEGER'),
                bigquery.SchemaField('ca_name', 'STRING'),
            ]
    load_table(filename, table, schema)


def load_crm_upd_cust():
    
    filename = 'UpdCust.csv'
    table = 'UpdCust'
    schema = [
                bigquery.SchemaField('action_ts', 'DATETIME'),
                bigquery.SchemaField('c_id', 'INTEGER'),
                bigquery.SchemaField('c_tier', 'STRING'),
                bigquery.SchemaField('c_adline1', 'STRING'),
                bigquery.SchemaField('c_zipcode', 'STRING'),
                bigquery.SchemaField('c_city', 'STRING'),
                bigquery.SchemaField('c_state_prov', 'STRING'),
                bigquery.SchemaField('c_ctry', 'STRING'),
                bigquery.SchemaField('c_prim_email', 'STRING'),
                bigquery.SchemaField('c_phone_1_ctry_code', 'STRING'),
                bigquery.SchemaField('c_phone_1_area_code', 'STRING'),
                bigquery.SchemaField('c_phone_1_c_local', 'STRING'),
                bigquery.SchemaField('c_phone_2_ctry_code', 'STRING'),
                bigquery.SchemaField('c_phone_2_area_code', 'STRING'),
                bigquery.SchemaField('c_phone_2_c_local', 'STRING'),
                bigquery.SchemaField('c_phone_3_ctry_code', 'STRING'),
                bigquery.SchemaField('c_phone_3_area_code', 'STRING'),
                bigquery.SchemaField('c_phone_3_c_local', 'STRING'),
            ]
    load_table(filename, table, schema)


def load_crm_new_cust():
    
    filename = 'NewCust.csv'
    table = 'NewCust'
    schema = [
                bigquery.SchemaField('action_ts', 'DATETIME'),
                bigquery.SchemaField('c_dob', 'DATE'),
                bigquery.SchemaField('c_gndr', 'STRING'),
                bigquery.SchemaField('c_id', 'INTEGER'),
                bigquery.SchemaField('c_tax_id', 'STRING'),
                bigquery.SchemaField('c_tier', 'STRING'),
                bigquery.SchemaField('c_l_name', 'STRING'),
                bigquery.SchemaField('c_f_name', 'STRING'),
                bigquery.SchemaField('c_m_name', 'STRING'),
                bigquery.SchemaField('c_adline1', 'STRING'),
                bigquery.SchemaField('c_adline2', 'STRING'),
                bigquery.SchemaField('c_zipcode', 'STRING'),
                bigquery.SchemaField('c_city', 'STRING'),
                bigquery.SchemaField('c_state_prov', 'STRING'),
                bigquery.SchemaField('c_ctry', 'STRING'),
                bigquery.SchemaField('c_prim_email', 'STRING'),
                bigquery.SchemaField('c_alt_email', 'STRING'),
                bigquery.SchemaField('c_ctry_code_1', 'STRING'),
                bigquery.SchemaField('c_area_code_1', 'STRING'),
                bigquery.SchemaField('c_local_1', 'STRING'),
                bigquery.SchemaField('c_ctry_code_2', 'STRING'),
                bigquery.SchemaField('c_area_code_2', 'STRING'),
                bigquery.SchemaField('c_local_2', 'STRING'),
                bigquery.SchemaField('c_ctry_code_3', 'STRING'),
                bigquery.SchemaField('c_area_code_3', 'STRING'),
                bigquery.SchemaField('c_local_3', 'STRING'),
                bigquery.SchemaField('c_lcl_tx_id', 'STRING'),
                bigquery.SchemaField('c_nat_tx_id', 'STRING'),
                bigquery.SchemaField('ca_id', 'STRING'),
                bigquery.SchemaField('ca_tax_st', 'STRING'),
                bigquery.SchemaField('ca_b_id', 'STRING'),
                bigquery.SchemaField('ca_name', 'STRING'),
                bigquery.SchemaField('card', 'STRING'),
            ]
    load_table(filename, table, schema)


def load_crm():
    delete_create_dataset()
    load_crm_add_acct()
    load_crm_inact_cust()
    load_crm_upd_acct()
    load_crm_upd_cust()
    load_crm_new_cust()
    
if __name__ == '__main__':
    load_crm()