from flask import Flask, request
from random import choice
import hazelcast
import requests
import uuid

app = Flask(__name__)
client = hazelcast.HazelcastClient()

queue = client.get_queue("mes-queue").blocking()

message_service = (
    "http://localhost:8082/message_service",
    "http://localhost:8083/message_service"
)
logging_service = (
    "http://localhost:8084/logging_service",
    "http://localhost:8085/logging_service",
    "http://localhost:8086/logging_service"
)


@app.route('/facade_service', methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        data = {
            "msg": request.get_json(),
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
    app.run(host="localhost", port=8081)
