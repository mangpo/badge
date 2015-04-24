#!/usr/bin/python
from flask import Flask
from flask import request
from algo import *
import random

app = Flask(__name__)
setup()
#public_dir = "../express-server/public/"

@app.route('/status', methods=['GET'])
def status():
  print 'args -------------'
  print request.args
  if 'id' in request.args and 'loc' in request.args:
    user_id = int(request.args['id'])
    loc = request.args['loc']
    # print user_id, loc
    report_status(user_id,loc)
  array = [random.randint(0,255) for i in xrange(64*3)]
  return ','.join(str(x) for x in array)


@app.route('/badge', methods=['GET','POST'])
def badge():
  print request.form
  return """
  <!DOCTYPE html>
  <html>
  <body>
    <form  method="post">
      ID:<br>
      <input type="text" name="id"><br>
      Sequence of 64 x 3:<br>
      <input type="text" name="badge" size="100"><br>
      <input type="submit" value="Submit" name="submit">
    </form>
    
  </body>
  </html>
  """


@app.route('/map', methods=['GET'])
def map():
  user_id = int(request.args['id'])
  return get_map(user_id)

# request.form
# ImmutableMultiDict([('badge', u'1,2,2,3'), ('submit', u'Submit')])
@app.route('/test', methods=['GET','POST'])
def test():
  print 'get_data -------------'
  print len(request.get_data())
  print 'args -------------'
  print request.args
  print 'files -------------'
  print request.files
  print 'data -------------'
  print len(request.data)
  print 'form -------------'
  print request.form
  print 'encoding -------------'
  print request.content_encoding
  print request.content_length
  print request.content_type
  print 'host -------------'
  print request.host
  print '-------------'
  return """
  <!DOCTYPE html>
  <html>
  <body>
    <form  method="post">
      Sequence of 64 x 3:<br>
      <input type="text" name="badge" size="100"><br>
      <input type="submit" value="Submit" name="submit">
    </form>
    
  </body>
  </html>
  """

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001, debug=True)

