#!/usr/bin/python
from flask import Flask
from flask import request
from algo import *
import random

app = Flask(__name__)
setup()

# Upon receiving /restart?id=<id>, server will send the last badge back to arduino.
# If there is no nearby user or place so far, server will send the user's own badge.
@app.route('/restart', methods=['GET'])
def restart():
  print request.args
  if 'id' in request.args:
    user_id = int(request.args['id'])
    return user_restart(user_id)
  else:
    return "Please specify user ID."

# Upon receiving GPS location, 
#   server will send one badge if there is a new nearby user/place.
#   If there is no new user, server will send "no new badge".
# If either 'id' or 'loc' argument is not specified, 
#   server will return random 64x3 integers.
@app.route('/status', methods=['GET'])
def status():
  print 'args -------------'
  print request.args
  if 'id' in request.args and 'loc' in request.args:
    user_id = int(request.args['id'])
    loc = request.args['loc']
    return report_status(user_id,loc)
  else:
    array = [random.randint(0,255) for i in xrange(64*3)]
    return ','.join(str(x) for x in array)

# Another format to send GPS location (from iPhone)
@app.route('/status2', methods=['GET','POST'])
def status2():
  if 'id' in request.form and 'lat' in request.form and 'long' in request.form:
    user_id = int(request.form['id'])
    update_user(int(request.form['id']), \
                  [float(request.form['lat']), float(request.form['long'])])
  return """
  <!DOCTYPE html>
  <html>
  <body>
    <form  method="post">
      ID:<br>
      <input type="text" name="id"><br>
      Latitude:<br>
      <input type="text" name="lat"><br>
      Longtitude:<br>
      <input type="text" name="long"><br>
      <input type="submit" value="Submit" name="submit">
    </form>
    
  </body>
  </html>
  """

# Upload badge
@app.route('/badge', methods=['GET','POST'])
def badge():
  print request.form
  if 'id' in request.form and 'badge' in request.form:
    save_badge(int(request.form['id']),request.form['badge'])
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

# Upload personalized message
@app.route('/message', methods=['GET','POST'])
def message():
  print request.form
  print request.args
  if 'id' in request.form and 'message' in request.form:
    save_message(int(request.form['id']),request.form['message'])
  return """
  <!DOCTYPE html>
  <html>
  <body>
    <form  method="post">
      ID:<br>
      <input type="text" name="id"><br>
      Message:<br>
      <input type="text" name="message" size="50"><br>
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

