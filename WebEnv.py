from flask import Flask
from flask import request
from flask import render_template

info = {'first':'', 'second':''}

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template("forms.html")

@app.route('/', methods=['POST'])
def my_form_post():

    text = request.form['text']
    info['first'] = text.upper()

    print info
    return 'I hate to say it, but you need to get out more...'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)