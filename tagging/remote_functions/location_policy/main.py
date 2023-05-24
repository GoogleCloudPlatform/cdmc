# pip install google-cloud-org-policy

from __future__ import print_function
from google.cloud import orgpolicy_v2
import base64
import json

def event_handler(request):
    request_json = request.get_json()
    #print('request_json:', request_json)
    
    project_id = request_json['calls'][0][0].strip()
    #print('project_id:', project_id)
    
    client = orgpolicy_v2.OrgPolicyClient()

    req = orgpolicy_v2.GetPolicyRequest(
        name="projects/" + project_id + "/policies/gcp.resourceLocations",
    )

    try:
        res = client.get_policy(request=req)
        #print('res:', res)
    
        if 'spec' in res:
            rules = res.spec.rules 
            for rule in rules:
                allowed_locations = [rule.values.allowed_values[0].split(':')[1]]
                print('allowed_locations:', allowed_locations)
                return json.dumps({"replies": allowed_locations})
    
    except Exception as e:
        print("Exception caught: " + str(e))
        return json.dumps({"errorMessage": str(e)}), 400

