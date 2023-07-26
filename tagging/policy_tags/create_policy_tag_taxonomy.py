#!/usr/bin/python
#
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import yaml

from google.cloud import datacatalog
#from google.cloud.bigquery import datapolicies
from google.cloud import bigquery_datapolicies
from google.iam.v1 import iam_policy_pb2
from google.cloud import bigquery
from google.cloud.bigquery import schema

ptm = datacatalog.PolicyTagManagerClient()

def process_request(yaml_file):
        
    with open(yaml_file) as f:
        file_contents = yaml.full_load(f)
        taxonomy_contents = file_contents.get("taxonomy")
        #print(taxonomy_contents)
        
        name = taxonomy_contents.get("name").strip()
        project = taxonomy_contents.get("project").strip()
        region = taxonomy_contents.get("region").strip()
        
        taxonomy = get_or_create_taxonomy(project, region, name)
        
        policy_tags = taxonomy_contents.get("policy_tags")
        #print(policy_tags)
        process_policy_tags(project, region, taxonomy, policy_tags, None)
        
                   
def get_or_create_taxonomy(project, region, name):
    
    parent = "projects/{0}/locations/{1}".format(project, region)

    list_request = datacatalog.ListTaxonomiesRequest(parent=parent)
    resp = ptm.list_taxonomies(request=list_request)

    for taxonomies in resp:
        if taxonomies.display_name == name:
            print('taxonomy already exists')
            return taxonomies.name
    
    print('taxonomy does not exist')        
    taxonomy = datacatalog.Taxonomy()
    taxonomy.display_name = name
    
    create_request = datacatalog.CreateTaxonomyRequest(parent=parent, taxonomy=taxonomy)
    resp = ptm.create_taxonomy(request=create_request)
    print('created taxonomy', resp.name)

    return resp.name


def process_policy_tags(project, region, taxonomy, policy_tags, parent):
    
    #print('enter process_policy_tags: taxonomy:', taxonomy, ', policy_tags:', policy_tags, ', parent:', parent)
    
    protected_columns = []
    
    for node, subtree in policy_tags.items():
        #print('node:', node, ', subtree:', subtree)
        
        if node == 'fine_grained_readers':
            set_fine_grained_readers(parent, subtree)

        elif node == 'masking_rules':
            #print('found masking rules')
            #print('masking_rules subtree:', subtree)
            for masking_rule in subtree:
                create_update_masking_rule(project, region, parent, masking_rule)
        else:
            policy_tag = get_or_create_policy_tag(taxonomy, node, parent)
            #print('returned policy tag:', policy_tag)
 
            if subtree != None:
                process_policy_tags(project, region, taxonomy, subtree, policy_tag) 
    
 
def get_or_create_policy_tag(taxonomy, node, parent=None):
    
    list_request = datacatalog.ListPolicyTagsRequest(parent=taxonomy)
    list_resp = ptm.list_policy_tags(request=list_request)
    #print('list resp:', list_resp)
    
    for policy_tag in list_resp:
        if policy_tag.display_name == node:
            print('found policy tag for', node)
            return policy_tag.name
    
    print('policy tag for', node, 'not found')
    policy_tag = datacatalog.PolicyTag()
    policy_tag.display_name = node
    
    if parent != None:
        policy_tag.parent_policy_tag = parent
    
    create_request = datacatalog.CreatePolicyTagRequest(parent=taxonomy, policy_tag=policy_tag) 
    create_resp = ptm.create_policy_tag(request=create_request)
    print('created policy tag', create_resp.name)
    
    return create_resp.name


def set_fine_grained_readers(policy_tag, fine_grained_readers):
    
    formatted_readers = []
    
    for reader in fine_grained_readers:
        if reader.strip().endswith('gserviceaccount.com'):
            if reader.strip().startswith('serviceAccount:') == False: 
                formatted_readers.append('serviceAccount:' + reader)
        else:
            if reader.strip().startswith('user:') == False:
                formatted_readers.append('user:' + reader)  
    
    print('formatted_readers:', formatted_readers)
    
    iam_req = iam_policy_pb2.GetIamPolicyRequest(resource=policy_tag)
    iam_resp = ptm.get_iam_policy(request=iam_req)
    #print('iam_resp:', iam_resp)
        
    policy = {
     "bindings": [
     {
      "role": "roles/datacatalog.categoryFineGrainedReader",
      "members": formatted_readers
      }],
      "etag": iam_resp.etag
    }

    #print('policy:', policy)
    
    iam_req = iam_policy_pb2.SetIamPolicyRequest(resource=policy_tag, policy=policy)
    iam_resp = ptm.set_iam_policy(iam_req)
    print('set fine grained readers')
    
    #print('iam_resp:', iam_resp)

 
def create_update_masking_rule(project, region, policy_tag, masking_rule):
    
    print('policy_tag:', policy_tag)
    print('masking_rule:', masking_rule)
    
    parent = 'projects/{0}/locations/{1}'.format(project, region)
    policy_name = masking_rule.get("policy_name")
    policy_name_qualified = 'projects/{0}/locations/{1}/dataPolicies/{2}'.format(project, region, policy_name)
    masking_type = masking_rule.get("masking_type")
    masked_readers = masking_rule.get("masked_readers")

    #dpsc = datapolicies.DataPolicyServiceClient()
    dpsc = bigquery_datapolicies.DataPolicyServiceClient()

    #list_req = datapolicies.ListDataPoliciesRequest(parent=parent)
    list_req = bigquery_datapolicies.ListDataPoliciesRequest(parent=parent)
    list_res = dpsc.list_data_policies(request=list_req)
    
    masking_rule_exists = False
    
    for res in list_res:
        # data policy names must be unique under a project and location, 
        # when a policy tag taxonomy gets deleted, the data policies remain
        # they must be deleted separately
        if res.name == policy_name_qualified:
            print('masking rule', policy_name, 'already exists')
            masking_rule_exists = True
            policy_tag = res.policy_tag
            break
    
    if 'hash' in masking_type.lower() or 'SHA256' in masking_type:
        predefined_expression = 'SHA256'
    elif 'nullify' in masking_type.lower() or 'null' in masking_type.lower():
        predefined_expression = 'ALWAYS_NULL'
    else:
        predefined_expression = 'DEFAULT_MASKING_VALUE'

    #dp = datapolicies.DataPolicy()
    dp = bigquery_datapolicies.DataPolicy()
    dp.name = policy_name_qualified
    dp.data_policy_id = policy_name
    dp.data_policy_type = 'DATA_MASKING_POLICY'
    dp.policy_tag = policy_tag
    dp.data_masking_policy.predefined_expression = predefined_expression
    
    if masking_rule_exists:
        
        #dp_req = datapolicies.UpdateDataPolicyRequest(data_policy=dp)
        dp_req = bigquery_datapolicies.UpdateDataPolicyRequest(data_policy=dp)
        #print('dp_req:', dp_req)
    
        dp_res = dpsc.update_data_policy(request=dp_req)
        #print('dp_res:', dp_res)
        
        print('updated data policy ', policy_name)
        
    else:
        dp_req = bigquery_datapolicies.CreateDataPolicyRequest(
            parent=parent,
            data_policy=dp)
        #print('dp_req:', dp_req)
    
        dp_res = dpsc.create_data_policy(request=dp_req)
        #print('dp_res:', dp_res)
        
        print('created data policy ', policy_name)
        
    # set permissions on the created or updated policy
    set_masked_readers(dp_res.name, masked_readers)


def set_masked_readers(data_policy, masked_readers):
    
    #dpsc = datapolicies.DataPolicyServiceClient()
    dpsc = bigquery_datapolicies.DataPolicyServiceClient()
    formatted_readers = []
    
    for reader in masked_readers:
        if reader.strip().endswith('gserviceaccount.com'):
            if reader.strip().startswith('serviceAccount:') == False: 
                formatted_readers.append('serviceAccount:' + reader)
        else:
            if reader.strip().startswith('user:') == False:
                formatted_readers.append('user:' + reader)  
    
    print('formatted_readers:', formatted_readers)
    
    iam_req = iam_policy_pb2.GetIamPolicyRequest(resource=data_policy)
    iam_resp = dpsc.get_iam_policy(request=iam_req)
    #print('iam_resp:', iam_resp)
        
    policy = {
     "bindings": [
     {
      "role": "roles/bigquerydatapolicy.maskedReader",
      "members": formatted_readers
      }],
      "etag": iam_resp.etag
    }

    #print('policy:', policy)
    
    iam_req = iam_policy_pb2.SetIamPolicyRequest(resource=data_policy, policy=policy)
    iam_resp = dpsc.set_iam_policy(iam_req)
    print('set masked readers')
    
    #print('iam_resp:', iam_resp)
        

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description="Creates taxonomy, policy tags, masking rules, and associations.")
    parser.add_argument('yaml_file', help='The yaml file containing the specification')
    args = parser.parse_args()
    process_request(args.yaml_file)
    