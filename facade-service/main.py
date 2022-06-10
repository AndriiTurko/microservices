from flask import Flask, request
from random import choice
import hazelcast
import requests
import consul
import uuid
import sys


app = Flask(__name__)
client = hazelcast.HazelcastClient()

service_name = "facade_service"
port = int(sys.argv[1])
service_id = service_name + ":" + str(port)

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register(service_name, port=port, service_id=service_id)

queue = client.get_queue("mes-queue").blocking()

message_service = []
logging_service = []

for key, val in session.agent.services().items():
    url = "http://localhost:" + str(val['Port']) + "/"
    if key.startswith("message"):
        message_service.append(url + "message_service")
    elif key.startswith("logging"):
        logging_service.append(url + "logging_service")

client = hazelcast.HazelcastClient(cluster_members=session.kv.get('hz-nodes')[1]['Value'].decode("utf-8").split())
queue = client.get_queue(session.kv.get('mes-queue')[1]['Value'].decode("utf-8")).blocking()


@app.route('/facade_service', methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        data = {
            "msg": request.get_data(),
            "uuid": str(uuid.uuid4())
        }

        queue.put(data)
        log_response = requests.post(choice(logging_service), data=data)

        return log_response.text

    elif request.method == 'GET':
        log_response = requests.get(choice(logging_service)).text
        msg_response = requests.get(choice(message_service)).text

        response = "logging-service response: " + log_response + "\n" + "messages-service response: " + msg_response

        return response


if __name__ == '__main__':
    app.run(host="localhost", port=port)
