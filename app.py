import sys
import logging

from flask import Flask, request, jsonify

from projects.rec_serv.routes import bp_rec_serv

app = Flask(__name__)

handler = logging.StreamHandler(sys.stdout)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

app.register_blueprint( bp_rec_serv )

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run( debug=True )
