from flask import Flask, request

from key_terms import KeyTerms

app = Flask(__name__)


@app.route('/key-terms-api/from-json/single_text', methods=['POST'])
def keywords_from_text():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        key_words_num = request.json['key_words_num']
        texts = {'text': request.json['text']}

        key_terms = KeyTerms(texts, key_words_num).keywords
        print(key_terms)
        return key_terms

    else:
        return 'Content-Type not supported!'


@app.route('/key-terms-api/from-json/titled_texts', methods=['POST'])
def keywords_from_labeled_texts():
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        key_words_num = request.json['key_words_num']
        texts = request.json['texts']
        print(texts)

        key_terms = KeyTerms(texts, key_words_num).keywords
        print(key_terms)
        return key_terms

    else:
        return 'Content-Type not supported!'


if __name__ == '__main__':
    app.run()
