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
from DataLoader import DataLoader


# Create a DataLoader object. 
dl = DataLoader()
 

def load_date():
    filename = 'Date.txt'
    table = 'Date'
    dataset = 'reference'
    origin = 'load_reference.py'
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
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_industry():
    filename = 'Industry.txt'
    table = 'Industry'
    dataset = 'reference'
    origin = 'load_reference.py'
    schema = [
                bigquery.SchemaField('in_id', 'STRING'),
                bigquery.SchemaField('in_name', 'STRING'),
                bigquery.SchemaField('in_sc_id', 'STRING'),
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_status_type():
    filename = 'StatusType.txt'
    table = 'StatusType'
    dataset = 'reference'
    origin = 'load_reference.py'
    schema = [
                bigquery.SchemaField('st_id', 'STRING'),
                bigquery.SchemaField('st_name', 'STRING'),
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_tax_rate():
    filename = 'TaxRate.txt'
    table = 'TaxRate'
    dataset = 'reference'
    origin = 'load_reference.py'
    schema = [
                bigquery.SchemaField('tx_id', 'STRING'),
                bigquery.SchemaField('tx_name', 'STRING'),
                bigquery.SchemaField('tx_rate', 'STRING'),
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_time():
    filename = 'Time.txt'
    table = 'Time'
    dataset = 'reference'
    origin = 'load_reference.py'
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
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')

    
if __name__ == '__main__':
    dl.delete_create_dataset('reference')
    load_date()
    load_industry()
    load_status_type()
    load_tax_rate()
    load_time()