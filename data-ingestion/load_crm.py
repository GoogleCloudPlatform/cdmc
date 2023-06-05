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

def load_crm_add_acct():
    filename = 'AddAcct.csv'
    table = 'AddAcct'
    dataset = 'crm'
    origin = 'load_crm.py'
    schema = [
        bigquery.SchemaField('action_ts', 'DATETIME'),
        bigquery.SchemaField('c_id', 'INTEGER'),
        bigquery.SchemaField('ca_id', 'INTEGER'),
        bigquery.SchemaField('ca_tax_st', 'INTEGER'),
        bigquery.SchemaField('ca_b_id', 'INTEGER'),
        bigquery.SchemaField('ca_name', 'STRING'),
    ]
    dl.load_table(filename, dataset, table, schema, origin)


def load_crm_inact_cust():
    filename = 'InactCust.csv'
    table = 'InactCust'
    dataset = 'crm'
    origin = 'load_crm.py'
    schema = [
        bigquery.SchemaField('action_ts', 'DATETIME'),
        bigquery.SchemaField('c_id', 'INTEGER'),
    ]
    dl.load_table(filename, dataset, table, schema, origin)


def load_crm_upd_acct():
    filename = 'UpdAcct.csv'
    table = 'UpdAcct'
    dataset = 'crm'
    origin = 'load_crm.py'
    schema = [
        bigquery.SchemaField('action_ts', 'DATETIME'),
        bigquery.SchemaField('c_id', 'INTEGER'),
        bigquery.SchemaField('ca_id', 'INTEGER'),
        bigquery.SchemaField('ca_tax_st', 'INTEGER'),
        bigquery.SchemaField('ca_b_id', 'INTEGER'),
        bigquery.SchemaField('ca_name', 'STRING'),
    ]
    dl.load_table(filename, dataset, table, schema, origin)


def load_crm_upd_cust():
    filename = 'UpdCust.csv'
    table = 'UpdCust'
    dataset = 'crm'
    origin = 'load_crm.py'
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
    dl.load_table(filename, dataset, table, schema, origin)


def load_crm_new_cust():
    filename = 'NewCust.csv'
    table = 'NewCust'
    dataset = 'crm'
    origin = 'load_crm.py'
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
    dl.load_table(filename, dataset, table, schema, origin)


if __name__ == '__main__':
    dl.delete_create_dataset('crm')
    load_crm_add_acct()
    load_crm_inact_cust()
    load_crm_upd_acct()
    load_crm_upd_cust()
    load_crm_new_cust()
