from flask import Flask, redirect, request, render_template, jsonify, make_response
from sendgrid import Mail, SendGridClient
import os

app = Flask('PostCards')
sg = SendGridClient(os.getenv('SG_USER'), os.getenv('SG_PWD'))

# Post Schema
# ID
# from
# image

posts = {}

@app.route('/', methods=['GET'])
def new_postcard():
    ID = len(posts)
    posts[ID] = {}
    return redirect('/edit/%s' % ID, code=302)

@app.route('/edit/<int:ID>', methods=['GET', 'PUT'])
def edit_handler(ID):
    if request.method == 'GET':
        return render_template('postcard.html', post=posts[ID], editor=True)
    else:
        posts[ID] = request.get_json()
        return jsonify(**posts[ID])

@app.route('/view/<int:ID>', methods=['GET'])
def view_handler(ID):
    return render_template('postcard.html', post=posts[ID])

@app.route('/send', methods=['POST'])
def send_postcard():
    payload = request.get_json()
    if payload['method'] == 'email':
        # Send SG Email
        return make_response(status_code=204)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
