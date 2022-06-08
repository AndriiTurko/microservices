from flask import Flask, request

app = Flask(__name__)

messages = {}


@app.route('/logging_service', methods=['POST', 'GET'])
def logging():
    if request.method == 'POST':
        msg = request.form["msg"]
        uuid = request.form["uuid"]
        messages[uuid] = msg

        print("Message:", msg, "UUID:", uuid)

        response = {
            "status_code": 200
        }

        return response

    if request.method == 'GET':
        return str(list(messages.values()))


if __name__ == '__main__':
    app.run(host="localhost", port=8081)
