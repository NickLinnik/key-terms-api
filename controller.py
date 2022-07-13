from flask import Flask, request

from key_terms import KeyTerms

app = Flask(__name__)


@app.route('/key-terms-api/from-json')
def hello_world():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        json = request.json
        print(json)
        print(type(json))
        return '42'

    else:
        return 'Content-Type not supported!'


if __name__ == '__main__':
    app.run()
