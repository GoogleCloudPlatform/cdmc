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
 

def load_account():
    filename = 'Account*.txt'
    table = 'Account'
    dataset = 'oltp'
    origin = 'load_oltp.py'
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
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_cash_tx_historical():
    filename = 'CashTransactionHistorical.txt'
    table = 'CashTransactionHistorical'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('ct_ca_id', 'INTEGER'),
                bigquery.SchemaField('ct_dts', 'DATETIME'),
                bigquery.SchemaField('ct_amt', 'NUMERIC'),
                bigquery.SchemaField('ct_name', 'STRING'),
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_cash_tx_incremental():
    filename = 'CashTransactionIncremental*.txt'
    table = 'CashTransactionIncremental'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('ct_ca_id', 'INTEGER'),
                bigquery.SchemaField('ct_dts', 'DATETIME'),
                bigquery.SchemaField('ct_amt', 'NUMERIC'),
                bigquery.SchemaField('ct_name', 'STRING'),
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_customer():
    filename = 'Customer*.txt'
    table = 'Customer'
    dataset = 'oltp'
    origin = 'load_oltp.py'
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
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_daily_market_historical():
    filename = 'DailyMarketHistorical.txt'
    table = 'DailyMarketHistorical'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('dm_date', 'DATE'),
                bigquery.SchemaField('dm_s_symb', 'STRING'),
                bigquery.SchemaField('dm_close', 'NUMERIC'),
                bigquery.SchemaField('dm_high', 'NUMERIC'),
                bigquery.SchemaField('dm_low', 'NUMERIC'),
                bigquery.SchemaField('dm_vol', 'INTEGER'),               
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_daily_market_incremental():
    filename = 'DailyMarketIncremental*.txt'
    table = 'DailyMarketIncremental'
    dataset = 'oltp'
    origin = 'load_oltp.py'
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
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_holding_history_historical():
    filename = 'HoldingHistoryHistorical.txt'
    table = 'HoldingHistoryHistorical'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('hh_h_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_before_qty', 'INTEGER'),
                bigquery.SchemaField('hh_after_qty', 'INTEGER'),               
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_holding_history_incremental():
    filename = 'HoldingHistoryIncremental*.txt'
    table = 'HoldingHistoryIncremental'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('hh_h_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_t_id', 'INTEGER'),
                bigquery.SchemaField('hh_before_qty', 'INTEGER'),
                bigquery.SchemaField('hh_after_qty', 'INTEGER'),               
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_trade_historical():
    filename = 'TradeHistorical.txt'
    table = 'TradeHistorical'
    dataset = 'oltp'
    origin = 'load_oltp.py'
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
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_trade_incremental():
    filename = 'TradeIncremental*.txt'
    table = 'TradeIncremental'
    dataset = 'oltp'
    origin = 'load_oltp.py'
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
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_trade_history():
    filename = 'TradeHistory.txt'
    table = 'TradeHistory'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('th_t_id', 'INTEGER'),
                bigquery.SchemaField('th_dts', 'DATETIME'),
                bigquery.SchemaField('th_st_id', 'STRING'),               
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_watch_history_historical():
    filename = 'WatchHistoryHistorical.txt'
    table = 'WatchHistoryHistorical'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('w_c_id', 'INTEGER'),
                bigquery.SchemaField('w_s_symb', 'STRING'),
                bigquery.SchemaField('w_dts', 'DATETIME'), 
                bigquery.SchemaField('w_action', 'STRING'),              
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


def load_watch_history_incremental():
    filename = 'WatchHistoryIncremental*.txt'
    table = 'WatchHistoryIncremental'
    dataset = 'oltp'
    origin = 'load_oltp.py'
    schema = [
                bigquery.SchemaField('cdc_flag', 'STRING'),
                bigquery.SchemaField('cdc_dsn', 'INTEGER'),
                bigquery.SchemaField('w_c_id', 'INTEGER'),
                bigquery.SchemaField('w_s_symb', 'STRING'),
                bigquery.SchemaField('w_dts', 'DATETIME'),
                bigquery.SchemaField('w_action', 'STRING'),
            ]
    dl.load_table(filename, dataset, table, schema, origin, field_delimiter='|')


if __name__ == '__main__':
    dl.delete_create_dataset('oltp')
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
  