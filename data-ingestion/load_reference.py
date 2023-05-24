from google.cloud import bigquery
import LineageManager as lineage
import datetime

BIGQUERY_PROJECT = 'sdw-conf-b1927e-bcc1' # replace with your project
BIGQUERY_PROJECT_NUMBER = 707062315533    # replace with your project
BIGQUERY_REGION = 'us-central1'           # replace with your region
BIGQUERY_DATASET = 'reference'
TPCDI_URL = 'https://www.tpc.org'
GCS_PATH_PREFIX = 'gs://tpcdi-data'       # replace with your bucket

bq_client = bigquery.Client(project=BIGQUERY_PROJECT, location=BIGQUERY_REGION)

def create_dataset():
    
    bq_client.create_dataset(BIGQUERY_DATASET, exists_ok=True)

def create_load_job(uri, table_id, schema):
	
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        source_format=bigquery.SourceFormat.CSV,
        field_delimiter='|',
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
    
    lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Data Download', 'load_reference.csv', 'Data Download', start_time, end_time, TPCDI_URL, uri)
    lm.create_lineage()
    
    #lm = lineage.LineageManager(BIGQUERY_PROJECT_NUMBER, BIGQUERY_REGION, 'Load Job', 'load_reference.csv', job_id, start_time, end_time, uri, 'bigquery:' + table_id)
    #lm.create_lineage()
    
    #lm.retrieve_lineage()
 

def load_date():
    
    filename = 'Date.txt'
    table = 'Date'
    schema = [
                bigquery.SchemaField('SK_DateID', 'INTEGER'),
                bigquery.SchemaField('DateValue', 'STRING'),
                bigquery.SchemaField('DateDesc', 'STRING'),
                bigquery.SchemaField('CalendarYearID', 'INTEGER'),
                bigquery.SchemaField('CalendarYearDesc', 'STRING'),
                bigquery.SchemaField('CalendarQtrID', 'INTEGER'),
                bigquery.SchemaField('CalendarQtrDesc', 'STRING'),
                bigquery.SchemaField('CalendarMonthID', 'INTEGER'),
                bigquery.SchemaField('CalendarMonthDesc', 'STRING'),
                bigquery.SchemaField('CalendarWeekID', 'INTEGER'),
                bigquery.SchemaField('CalendarWeekDesc', 'STRING'),
                bigquery.SchemaField('DayOfWeekNum', 'INTEGER'),
                bigquery.SchemaField('DayOfWeekDesc', 'STRING'),
                bigquery.SchemaField('FiscalYearID', 'INTEGER'),
                bigquery.SchemaField('FiscalYearDesc', 'STRING'),
                bigquery.SchemaField('FiscalQtrID', 'INTEGER'),
                bigquery.SchemaField('FiscalQtrDesc', 'STRING'),
                bigquery.SchemaField('HolidayFlag', 'BOOLEAN'), 
            ]
            
    load_table(filename, table, schema)


def load_industry():
    
    filename = 'Industry.txt'
    table = 'Industry'
    schema = [
                bigquery.SchemaField('in_id', 'STRING'),
                bigquery.SchemaField('in_name', 'STRING'),
                bigquery.SchemaField('in_sc_id', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_status_type():
    
    filename = 'StatusType.txt'
    table = 'StatusType'
    schema = [
                bigquery.SchemaField('st_id', 'STRING'),
                bigquery.SchemaField('st_name', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_tax_rate():
    
    filename = 'TaxRate.txt'
    table = 'TaxRate'
    schema = [
                bigquery.SchemaField('tx_id', 'STRING'),
                bigquery.SchemaField('tx_name', 'STRING'),
                bigquery.SchemaField('tx_rate', 'STRING'),
            ]
            
    load_table(filename, table, schema)


def load_time():
    
    filename = 'Time.txt'
    table = 'Time'
    schema = [
                bigquery.SchemaField('SK_TimeID', 'INTEGER'),
                bigquery.SchemaField('TimeValue', 'STRING'),
                bigquery.SchemaField('HourID', 'INTEGER'),
                bigquery.SchemaField('HourDesc', 'STRING'),
                bigquery.SchemaField('MinuteID', 'INTEGER'),
                bigquery.SchemaField('MinuteDesc', 'STRING'),
                bigquery.SchemaField('SecondID', 'INTEGER'),
                bigquery.SchemaField('SecondDesc', 'STRING'),
                bigquery.SchemaField('MarketHoursFlag', 'BOOLEAN'),
                bigquery.SchemaField('OfficeHoursFlag', 'BOOLEAN'),
            ]
            
    load_table(filename, table, schema)


def load_reference():
    create_dataset()
    load_date()
    load_industry()
    load_status_type()
    load_tax_rate()
    load_time()
    
if __name__ == '__main__':
    load_reference()