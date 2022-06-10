from flask import Flask
import hazelcast
import consul
import sys


app = Flask(__name__)
client = hazelcast.HazelcastClient()

service_name = "message_service"
port = int(sys.argv[1])
service_id = service_name + ":" + str(port)

session = consul.Consul(host='localhost', port=8500)
session.agent.service.register(service_name, port=port, service_id=service_id)

queue = client.get_queue(session.kv.get('mes-queue')[1]['Value'].decode("utf-8")).blocking()
messages_data = []


@app.route('/message_service', methods=['POST', 'GET'])
def messages():
    while not queue.is_empty():
        messages_data.append(queue.take())
        print("Received message:", messages_data[-1])

    return str(messages_data)


if __name__ == '__main__':
    app.run(host="localhost", port=port)
