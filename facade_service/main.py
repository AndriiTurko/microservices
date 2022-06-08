from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

logging_service = "http://localhost:8081/logging_service"
message_service = "http://localhost:8082/message_service"


@app.route('/facade_service', methods=['POST', 'GET'])
def facade():
    if request.method == 'POST':
        data = {
            "msg": request.get_data(),
            "uuid": str(uuid.uuid4())
        }
        log_response = requests.post(logging_service, data=data)

        return str(log_response.status_code) + '\n'

    elif request.method == 'GET':
        log_response = requests.get(logging_service).text
        msg_response = requests.get(message_service).text

        response = "logging-service response: " + log_response + "\n" + "messages-service response: " + msg_response
        return response


if __name__ == '__main__':
    app.run(host="localhost", port=8080)
