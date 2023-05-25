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

import os
from generate_report import generateReport
from flask import Flask, request, Response
import uuid

app = Flask(__name__)


@app.route("/")
def hello_world():
    return Response ("CDMC Reports running", status=200)


@app.route("/generate", methods= ["POST"])
def generate():

    projectNumber=''

    if(request.args.get('orgId')): orgId = request.args.get('orgId')
    else: return Response ("orgId parameter not set", status=400)

    if(request.args.get('projectId')): projectId = request.args.get('projectId')
    else: return Response ("projectId parameter not set", status=400)

    if(request.args.get('topicProjectId')): topicProjectId = request.args.get('topicProjectId')
    else: return Response ("topicProjectId parameter not set", status=400)

    if(request.args.get('topic')): topic = request.args.get('topic')
    else: return Response ("topic parameter not set", status=400)

    if(request.args.get('projectNumber')): projectNumber = request.args.get('projectNumber')
    else: 
        if(request.args.get('controls').find("14")>-1):return Response ("projectNumber parameter not set for Control 14", status=400)
        else: projectNumber = ""

    if(request.args.get('assetsScope')): 
        if request.args.get('assetsScope').upper()=="FALSE": assetsScope= False
        else: assetsScope = True
    else: assetsScope = True

    if(request.args.get('controls')): controls = request.args.get('controls')
    else: controls="all"

    uuid_str = str(uuid.uuid4())

    report_metadata = {"uuid":uuid_str,"Controls":controls}

    generateReport(orgId,projectId,topicProjectId,topic,report_metadata,projectNumber,assetsScope, controls)
    return Response({"uuid":uuid_str,
                     "status":"RUNNING",
                     "organization_id": orgId,
                     "project_id":projectId,
                     "controls": controls,
                     "result_project":topicProjectId, 
                     "result_topic":topic}, 
                     status=200)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))