from flask import Flask

app = Flask(__name__)


@app.route('/message_service', methods=['GET'])
def messages():
    return "messages-service is not implemented yet..."


if __name__ == '__main__':
    app.run(host="localhost", port=8082)
