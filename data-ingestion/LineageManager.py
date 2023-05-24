import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account
from google.cloud import bigquery
from google.protobuf.timestamp_pb2 import Timestamp

import requests, json, os
import datetime

DL_API = 'https://us-central1-datalineage.googleapis.com/v1'    # replace with your region
SA_KEY = '/Users/keys/cdmc-sa.json'                             # replace with your key file
SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

class LineageManager:
    
    project_number = None
    storage_region = None
    process_name = None
    origin_name = None
    job_id = None
    start_time = None
    end_time = None
    source = None
    target = None
    
    def __init__(self, project_number, storage_region, process_name, origin_name, job_id, start_time, end_time, source, target):
        
        self.project_number = project_number
        self.storage_region = storage_region
        self.process_name = process_name
        self.origin_name = origin_name
        self.job_id = job_id
        self.start_time = start_time
        self.end_time = end_time
        self.source = source
        self.target = target
               
    
    def create_lineage(self):
        
        print('create_lineage for', self.source, '->', self.target)
        
        process = self._create_process()
        
        if process == None:
            print('Error: create_process failed.')
        else:   
            print('process:', process)
            run = self._create_run(process)
            print('run:', run)
            
            if run == None:
                print('Error: create_run failed.')
            else:
                event = self._create_event(run)
                print('event:', event)
                
                if event == None:
                    print('Error: create_event failed.')

                
    def retrieve_lineage(self):
        
        self._get_links_by_source(self.source)
        self._get_links_by_target(self.target)
    
    ######## Internal methods ########

    def _get_credentials(self):

        credentials = service_account.Credentials.from_service_account_file(SA_KEY, scopes=SCOPES)
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
             
        return credentials.token

    
    def _create_process(self):
    
        url = '{0}/projects/{1}/locations/{2}/processes'.format(DL_API, self.project_number, self.storage_region)
        headers = {'Authorization' : 'Bearer ' + self._get_credentials()}
        payload = {'displayName': self.process_name, 'origin': {'sourceType': 'CUSTOM', 'name': 'data_ingestion/' + self.origin_name}}
        res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    
        if 'name' in res:
            process = res['name']
        else:
            process = None
    
        return process

    
    def _create_run(self, process):
    
        url = '{0}/{1}/runs'.format(DL_API, process)
        headers = {'Authorization' : 'Bearer ' + self._get_credentials()}
        
        if self.job_id:
            payload = {'displayName': self.job_id, 'startTime': self.start_time, 'endTime': self.end_time, 'state': 'COMPLETED'}
        else:
            payload = {'displayName': 'Manual', 'startTime': self.start_time, 'endTime': self.end_time, 'state': 'COMPLETED'}
            
        res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
    
        if 'name' in res:
            run = res['name']
        else:
            run = None
        
        return run
    
    
    def _create_event(self, run):
    
        url = '{0}/{1}/lineageEvents'.format(DL_API, run)
        headers = {'Authorization' : 'Bearer ' + self._get_credentials()}
    
        payload = {'links': [{'source': {'fullyQualifiedName': self.source}, 'target': {'fullyQualifiedName': self.target}}], 'startTime': self.start_time}
        print(payload)
        
        res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
        
        if 'name' in res:
            event = res['name']
        else:
            event = None
        
        return event
    

    def _get_links_by_source(self, source):

        url = '{0}/projects/{1}/locations/{2}:searchLinks'.format(DL_API, self.project_number, self.storage_region)
        headers = {'Authorization' : 'Bearer ' + self._get_credentials()}
        payload = {'source': {'fully_qualified_name': source, 'location': self.storage_region}}

        res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
        #print(res)
    
        if 'links' in res:
            links = res['links']
   
            for link in links:
                print('Source:', source, '-> Target:', link['target']['fullyQualifiedName'])
                self._get_links_by_source(link['target']['fullyQualifiedName'])
        else:
            return

 
    def _get_links_by_target(self, target):

        url = '{0}/projects/{1}/locations/{2}:searchLinks'.format(DL_API, self.project_number, self.storage_region)
        headers = {'Authorization' : 'Bearer ' + self._get_credentials()}
        payload = {'target': {'fully_qualified_name': target, 'location': self.storage_region}}

        res = requests.post(url, headers=headers, data=json.dumps(payload)).json()
        #print(res)
    
        if 'links' in res:
            links = res['links']
    
            for link in links:
                print('Target:', target, '<- Source:', link['source']['fullyQualifiedName'])
                self._get_links_by_target(link['source']['fullyQualifiedName'])
        else:
            return
    
 
if __name__ == '__main__':
    project_number = 998146089570  # project number for solution-workspace project
    storage_region = 'us-central1'
    process_name = 'Manual'
    job_id = 'Manual'
    start_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    end_time = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
    source = 'https://www.tpc.org/'
    target = 'gs://tpc-di/staging/crm/AddAcct.csv'
    lm = LineageManager(project_number, storage_region, process_name, job_id, start_time, end_time, source, target)
    lm.create_lineage()
    