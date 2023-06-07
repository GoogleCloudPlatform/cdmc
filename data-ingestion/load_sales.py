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
 

def load_prospect():
    filename = 'Prospect*.csv'
    table = 'Prospect'
    dataset = 'sales'
    origin = 'load_reference.py'
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
    dl.load_table(filename, dataset, table, schema, origin)

    
if __name__ == '__main__':
    dl.delete_create_dataset('sales')
    load_prospect()