from flask import Flask
import hazelcast
import sys


app = Flask(__name__)
client = hazelcast.HazelcastClient()

queue = client.get_queue("mes-queue").blocking()
messages_data = []


@app.route('/message_service', methods=['POST', 'GET'])
def messages():
    while not queue.is_empty():
        messages_data.append(queue.take())
        print("Received message:", messages_data[-1])

    return str(messages_data)


if __name__ == '__main__':
    app.run(host="localhost", port=int(sys.argv[1]))
