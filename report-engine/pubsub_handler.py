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

import avro
from avro.io import BinaryEncoder, DatumWriter
import io
import json
from google.api_core.exceptions import NotFound
from google.cloud.pubsub import PublisherClient
from google.cloud import pubsub_v1
from google.pubsub_v1.types import Encoding
import time
from concurrent import futures

def publishPubSubAvro(project_id,topic_id,avsc_file, message):
    publisher_client = PublisherClient()
    topic_path = publisher_client.topic_path(project_id, topic_id)

    avro_schema = avro.schema.parse(open(avsc_file, "rb").read())
    writer = DatumWriter(avro_schema)
    bout = io.BytesIO()
    record = message
    try:

        topic = publisher_client.get_topic(request={"topic": topic_path})
        encoding = topic.schema_settings.encoding

        if encoding == Encoding.BINARY:
            encoder = BinaryEncoder(bout)
            writer.write(record, encoder)
            data = bout.getvalue()

        elif encoding == Encoding.JSON:
            data_str = json.dumps(record)
            data = data_str.encode("utf-8")
        else:
            print(f"No encoding specified in {topic_path}. Abort.")
            exit(0)

        data_str = json.dumps(record)
        data = data_str.encode("utf-8")
        future = publisher_client.publish(topic_path, data)

    except NotFound:
        print(f"{topic_id} not found.")



def publishPubSubAvroBatch(project_id,topic_id,avsc_file, max_messages,max_bytes, max_latency, messages):
    
    batch_settings = pubsub_v1.types.BatchSettings(
        max_messages=int(max_messages),  
        max_bytes=int(max_bytes),  
        max_latency=int(max_latency),  
    )
    
    publisher_client = PublisherClient(batch_settings)
    topic_path = publisher_client.topic_path(project_id, topic_id)
    publish_futures = []

    # Prepare to write Avro records to the binary output stream.
    avro_schema = avro.schema.parse(open(avsc_file, "rb").read())
    writer = DatumWriter(avro_schema)
    bout = io.BytesIO()
    # Prepare data using a Python dictionary that matches the Avro schema
    for record in messages:
        try:

            topic = publisher_client.get_topic(request={"topic": topic_path})
            encoding = topic.schema_settings.encoding

            if encoding == Encoding.BINARY:
                encoder = BinaryEncoder(bout)
                writer.write(record, encoder)
                data = bout.getvalue()

            elif encoding == Encoding.JSON:
                data_str = json.dumps(record)
                data = data_str.encode("utf-8")
            else:
                print(f"No encoding specified in {topic_path}. Abort.")
                exit(0)

            data_str = json.dumps(record)
            data = data_str.encode("utf-8")
            publish_future = publisher_client.publish(topic_path, data)
            publish_futures.append(publish_future)

        except NotFound:
            print(f"{topic_id} not found.")
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)