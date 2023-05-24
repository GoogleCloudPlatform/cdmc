import base64
import json
from google.cloud import bigquery
from google.cloud.bigquery import datapolicies

DATA_GOV_PROJECT = 'sdw-data-gov-b1927e-dd69'  # replace with your project id
BIGQUERY_REGION = 'us-central1'                # replace with your GCP region
TAG_HISTORY_TABLE = 'tag_history_logs'         # replace with your tag history table in Tag Engine

def event_handler(request):
    
    request_json = request.get_json()
    print('request_json:', request_json)
    
    project = request_json['calls'][0][0].strip()
    dataset = request_json['calls'][0][1].strip()
    table = request_json['calls'][0][2].strip()
    column = request_json['calls'][0][3].strip()
    
    print('project:', project)
    print('dataset:', dataset)
    print('table:', table)
    print('column:', column)
    
    try:
        masking_type = get_masking_type(project, dataset, table, column)
        print('masking_type:', masking_type)

        return json.dumps({"replies": [masking_type]})
    
    except Exception as e:
        print("Exception caught: " + str(e))
        return json.dumps({"errorMessage": str(e)}), 400


def get_masking_type(project, dataset, table, column):
    
    sensitive_type = None
    bq_client = bigquery.Client(project=project, location=BIGQUERY_REGION)
    
    try:
        sql = "select sensitive_type from `" + DATA_GOV_PROJECT + "." + TAG_HISTORY_TABLE + ".data_sensitivity` "
        sql += "where asset_name = '" + project + "/dataset/" + dataset + "/table/" + table + "/column/" + column + "' "
        sql += "order by DATE(event_time) desc "
        sql += "limit 1"
        print('sql:', sql)
        
        rows = bq_client.query(sql).result()
            
        for row in rows:
            sensitive_type = row['sensitive_type']
            print('sensitive_type:', sensitive_type)
    
    except Exception as e:
        print('Error occurred while querying tag history table:', e)
    
    if sensitive_type:
        masking_type = get_policy_type(sensitive_type)
    else:
        masking_type = 'None'
    
    return masking_type


def get_policy_type(sensitive_type):
    
    masking_type = None
    
    dp_client = datapolicies.DataPolicyServiceClient()
    dp_name = "projects/" + DATA_GOV_PROJECT + "/locations/" + BIGQUERY_REGION + "/dataPolicies/" + sensitive_type.lower() + "_policy"
    print("dp_name:", dp_name)

    request = datapolicies.GetDataPolicyRequest(
            name=dp_name,
        )

    try:
        data_policy = dp_client.get_data_policy(request=request)
        
    except Exception as e:
        
        print('Error occurred during get_data_policy:', e)
        masking_type = 'None'
        
        return masking_type
        
        
    if data_policy.data_masking_policy.predefined_expression == datapolicies.DataMaskingPolicy.PredefinedExpression.DEFAULT_MASKING_VALUE:
        masking_type = 'Default Masking Value'
    
    elif data_policy.data_masking_policy.predefined_expression == datapolicies.DataMaskingPolicy.PredefinedExpression.SHA256:
        masking_type = 'SHA256Hash'
        
    elif data_policy.data_masking_policy.predefined_expression == datapolicies.DataMaskingPolicy.PredefinedExpression.ALWAYS_NULL:
        masking_type = 'Nullify'
    
    else:
        making_type = 'None'
        
    return masking_type


if __name__ == '__main__':
    project = 'sdw-conf-b1927e-bcc1'
    dataset = 'sales'
    table = 'Prospect'
    column = 'lastName' 
    masking_type = get_masking_type(project, dataset, table, column)
    print('masking_type:', masking_type)
    
    column2 = 'middleInitial'
    masking_type = get_masking_type(project, dataset, table, column2)
    print('masking_type:', masking_type)
    
    table2 = 'FINWIRE1992Q1_CMP'
    column3 = 'city'
    masking_type = get_masking_type(project, dataset, table2, column3)
    print('masking_type:', masking_type)