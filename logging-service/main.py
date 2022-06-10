from flask import Flask, request
import hazelcast
import consul
import sys

app = Flask(__name__)
client = hazelcast.HazelcastClient()

service_name = "logging_service"
port = int(sys.argv[1])
service_id = service_name + ":" + str(port)

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register(service_name, port=port, service_id=service_id)

messages = client.get_map(session.kv.get('log-map')[1]['Value'].decode("utf-8")).blocking()


@app.route('/logging_service', methods=['POST', 'GET'])
def logging():
    if request.method == 'POST':
        msg = request.form["msg"]
        uuid = request.form["uuid"]

        print("Message:", msg, "UUID:", uuid)

        messages.lock(uuid)
        try:
            messages.put(uuid, msg)
        finally:
            messages.unlock(uuid)

        response = {
            "status_code": 200
        }

        return response

    if request.method == 'GET':
        return str(list(messages.values()))


if __name__ == '__main__':
    app.run(host="localhost", port=port)
