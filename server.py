#!/usr/bin/python
from flask import Flask
from flask import request

import random

app = Flask(__name__)
#public_dir = "../express-server/public/"

@app.route('/status', methods=['GET'])
def status():
  print request.args
  array = [random.randint(0,255) for i in xrange(64*3)]
  return ','.join(str(x) for x in array)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)

