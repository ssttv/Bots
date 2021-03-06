from flask import Flask
from flask import request
from flask import jsonify
from view import View
from model import Model
import mics
from flask_sslify import SSLify


app = Flask(__name__)
model = Model()
view = View()


@app.route('/', methods=['GET'])
def default_answer():
    return '<h1>Bot working</h1>'


@app.route('/' + mics.token + '/', methods=['POST'])
def index():
    if request.method == 'POST':
        r = request.get_json()
        chat_id = r['message']['chat']['id']
        message = r['message']['text']

        if message == '/start':
            view.send_buttons()
        else:
            model.set_message(message)
            try:
                image_type = model.get_image()
            except NameError:
                view.send_message('Wrong input, try again')
            view.set_chat_id(chat_id)
            view.send_image(image_type)

        return jsonify(r)


if __name__ == '__main__':
    app.run()
