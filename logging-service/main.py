from flask import Flask, request
import hazelcast
import sys

app = Flask(__name__)
client = hazelcast.HazelcastClient()

messages = client.get_map('log-map').blocking()


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
    app.run(host="localhost", port=int(sys.argv[1]))
