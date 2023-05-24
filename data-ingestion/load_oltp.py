from google.cloud import bigquery
import LineageManager as lineage
import datetime

BIGQUERY_PROJECT = 'sdw-conf-b1927e-bcc1' # replace with your project
BIGQUERY_PROJECT_NUMBER = 707062315533    # replace with your project
BIGQUERY_REGION = 'us-central1'
BIGQUERY_DATASET = 'oltp'
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
        field_delimiter='|',
        write_disposition=bigquery.job.WriteDisposition.WRITE_TRUNCATE,
        destination_encryption_configuration=bigquery.EncryptionConfiguration(kms_key_name=KMS_KEY)
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
    
    lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Data Download', 'load_oltp.py', 'Data Download', start_time, end_time, TPCDI_URL, uri)
    lm.create_lineage()
    
    #lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Load Job', job_id, start_time, end_time, uri, 'bigquery:' + table_id)
    #lm.create_lineage()
    
    #lm.retrieve_lineage()
 

def load_account():
    
    filename = 'Account*.txt'
    table = 'Account'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('ca_id', 'INTEGER'),
                bigquery.SchemaField('ca_b_id', 'INTEGER'),
                bigquery.SchemaField('ca_c_id', 'INTEGER'),
                bigquery.SchemaField('ca_name', 'STRING'),
                bigquery.SchemaField('ca_tax_st', 'INTEGER'),
                bigquery.SchemaField('ca_st_id', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_cash_tx_historical():
    
    filename = 'CashTransactionHistorical.txt'
    table = 'CashTransactionHistorical'
    schema = [
                bigquery.SchemaField('ct_ca_id', 'INTEGER'),
                bigquery.SchemaField('ct_dts', 'DATETIME'),
                bigquery.SchemaField('ct_amt', 'NUMERIC'),
                bigquery.SchemaField('ct_name', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_cash_tx_incremental():
    
    filename = 'CashTransactionIncremental*.txt'
    table = 'CashTransactionIncremental'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('ct_ca_id', 'INTEGER'),
                bigquery.SchemaField('ct_dts', 'DATETIME'),
                bigquery.SchemaField('ct_amt', 'NUMERIC'),
                bigquery.SchemaField('ct_name', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_customer():
    
    filename = 'Customer*.txt'
    table = 'Customer'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('c_id', 'INTEGER'),
                bigquery.SchemaField('c_tax_id', 'STRING'),
                bigquery.SchemaField('c_st_id', 'STRING'),
                bigquery.SchemaField('c_l_name', 'STRING'),
                bigquery.SchemaField('c_f_name', 'STRING'),
                bigquery.SchemaField('c_m_name', 'STRING'),
                bigquery.SchemaField('c_gndr', 'STRING'),
                bigquery.SchemaField('c_tier', 'INTEGER'),
                bigquery.SchemaField('c_dob', 'DATE'),
                bigquery.SchemaField('c_adline1', 'STRING'),
                bigquery.SchemaField('c_adline2', 'STRING'),
                bigquery.SchemaField('c_zipcode', 'STRING'),
                bigquery.SchemaField('c_city', 'STRING'),
                bigquery.SchemaField('c_state_prov', 'STRING'),
                bigquery.SchemaField('c_cntry', 'STRING'),
                bigquery.SchemaField('c_cntry1', 'STRING'),
                bigquery.SchemaField('c_area1', 'STRING'),
                bigquery.SchemaField('c_local1', 'STRING'),
                bigquery.SchemaField('c_ext1', 'STRING'),
                bigquery.SchemaField('c_cntry2', 'STRING'),
                bigquery.SchemaField('c_area2', 'STRING'),
                bigquery.SchemaField('c_local2', 'STRING'),
                bigquery.SchemaField('c_ext2', 'STRING'),
                bigquery.SchemaField('c_cntry3', 'STRING'),
                bigquery.SchemaField('c_area3', 'STRING'),
                bigquery.SchemaField('c_local3', 'STRING'),
                bigquery.SchemaField('c_ext3', 'STRING'),
                bigquery.SchemaField('c_email1', 'STRING'),
                bigquery.SchemaField('c_email2', 'STRING'),
                bigquery.SchemaField('c_lcl_tax_id', 'STRING'),
                bigquery.SchemaField('c_nat_tax_id', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_daily_market_historical():
    
    filename = 'DailyMarketHistorical.txt'
    table = 'DailyMarketHistorical'
    schema = [
                bigquery.SchemaField('dm_date', 'DATE'),
                bigquery.SchemaField('dm_s_symb', 'STRING'),
                bigquery.SchemaField('dm_close', 'NUMERIC'),
                bigquery.SchemaField('dm_high', 'NUMERIC'),
                bigquery.SchemaField('dm_low', 'NUMERIC'),
                bigquery.SchemaField('dm_vol', 'INTEGER'),               
            ]
            
    load_table(filename, table, schema)


def load_daily_market_incremental():
    
    filename = 'DailyMarketIncremental*.txt'
    table = 'DailyMarketIncremental'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('dm_date', 'DATE'),
                bigquery.SchemaField('dm_s_symb', 'STRING'),
                bigquery.SchemaField('dm_close', 'NUMERIC'),
                bigquery.SchemaField('dm_high', 'NUMERIC'),
                bigquery.SchemaField('dm_low', 'NUMERIC'),
                bigquery.SchemaField('dm_vol', 'INTEGER'),               
            ]
            
    load_table(filename, table, schema)


def load_holding_history_historical():
    
    filename = 'HoldingHistoryHistorical.txt'
    table = 'HoldingHistoryHistorical'
    schema = [
                bigquery.SchemaField('hh_h_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_before_qty', 'INTEGER'),
                bigquery.SchemaField('hh_after_qty', 'INTEGER'),               
            ]
            
    load_table(filename, table, schema)


def load_holding_history_incremental():
    
    filename = 'HoldingHistoryIncremental*.txt'
    table = 'HoldingHistoryIncremental'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('hh_h_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_before_qty', 'INTEGER'),
                bigquery.SchemaField('hh_after_qty', 'INTEGER'),               
            ]
            
    load_table(filename, table, schema)


def load_trade_historical():
    
    filename = 'TradeHistorical.txt'
    table = 'TradeHistorical'
    schema = [
                bigquery.SchemaField('t_id', 'INTEGER'),
                bigquery.SchemaField('t_dts', 'DATETIME'),
                bigquery.SchemaField('t_st_id', 'STRING'),
                bigquery.SchemaField('t_tt_id', 'STRING'),
                bigquery.SchemaField('t_is_cash', 'BOOLEAN'),
                bigquery.SchemaField('t_s_symb', 'STRING'),
                bigquery.SchemaField('t_qty', 'INTEGER'),
                bigquery.SchemaField('t_bid_price', 'NUMERIC'),
                bigquery.SchemaField('t_ca_id', 'INTEGER'),
                bigquery.SchemaField('t_exec_name', 'STRING'),
                bigquery.SchemaField('t_trade_price', 'NUMERIC'),
                bigquery.SchemaField('t_chrg', 'NUMERIC'),
                bigquery.SchemaField('t_comm', 'NUMERIC'),
                bigquery.SchemaField('t_tax', 'NUMERIC'),
            ]
            
    load_table(filename, table, schema)


def load_trade_incremental():
    
    filename = 'TradeIncremental*.txt'
    table = 'TradeIncremental'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('t_id', 'INTEGER'),
                bigquery.SchemaField('t_dts', 'DATETIME'),
                bigquery.SchemaField('t_st_id', 'STRING'),
                bigquery.SchemaField('t_tt_id', 'STRING'),
                bigquery.SchemaField('t_is_cash', 'BOOLEAN'),
                bigquery.SchemaField('t_s_symb', 'STRING'),
                bigquery.SchemaField('t_qty', 'INTEGER'),
                bigquery.SchemaField('t_bid_price', 'NUMERIC'),
                bigquery.SchemaField('t_ca_id', 'INTEGER'),
                bigquery.SchemaField('t_exec_name', 'STRING'),
                bigquery.SchemaField('t_trade_price', 'NUMERIC'),
                bigquery.SchemaField('t_chrg', 'NUMERIC'),
                bigquery.SchemaField('t_comm', 'NUMERIC'),
                bigquery.SchemaField('t_tax', 'NUMERIC'),
            ]
            
    load_table(filename, table, schema)


def load_trade_history():
    
    filename = 'TradeHistory.txt'
    table = 'TradeHistory'
    schema = [
                bigquery.SchemaField('th_t_id', 'INTEGER'),
                bigquery.SchemaField('th_dts', 'DATETIME'),
                bigquery.SchemaField('th_st_id', 'STRING'),               
            ]
            
    load_table(filename, table, schema)


def load_watch_history_historical():
    
    filename = 'WatchHistoryHistorical.txt'
    table = 'WatchHistoryHistorical'
    schema = [
                bigquery.SchemaField('w_c_id', 'INTEGER'),
                bigquery.SchemaField('w_s_symb', 'STRING'),
                bigquery.SchemaField('w_dts', 'DATETIME'), 
                bigquery.SchemaField('w_action', 'STRING'),              
            ]
            
    load_table(filename, table, schema)


def load_watch_history_incremental():
    
    filename = 'WatchHistoryIncremental*.txt'
    table = 'WatchHistoryIncremental'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('w_c_id', 'INTEGER'),
                bigquery.SchemaField('w_s_symb', 'STRING'),
                bigquery.SchemaField('w_dts', 'DATETIME'),
                bigquery.SchemaField('w_action', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_oltp():
    delete_create_dataset()
    load_account()
    load_cash_tx_historical()
    load_cash_tx_incremental()
    load_customer()
    load_daily_market_historical()
    load_daily_market_incremental()
    load_holding_history_historical()
    load_trade_historical()
    load_trade_incremental()
    load_trade_history()
    load_watch_history_historical()
    load_watch_history_incremental()
  
    
if __name__ == '__main__':
    load_oltp()