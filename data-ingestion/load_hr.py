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
 

def load_employee():
    filename = 'HR.csv'
    table = 'Employee'
    dataset = 'hr'
    origin = 'load_hr.py'
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
    dl.load_table(filename, dataset, table, schema, origin)


if __name__ == '__main__':
    dl.delete_create_dataset('hr')
    load_employee()
    