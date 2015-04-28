from PIL import Image
import random

class User:
  def __init__(self, user_id):
    self.locations = []
    self.datetime = None
    self.user_id = user_id
    self.nearby = []
    self.nearby_loc = []
    self.badge = None
    self.queue = []

  def ping(self,datetime, loc, nearby):
    self.locations.append(loc)
    self.datetime = datetime
    for user in nearby:
      if not (user.user_id == self.user_id) and not(user.user_id in self.nearby):
        self.nearby.append(user.user_id)
        self.nearby_loc.append(user.locations[-1])
        self.queue.append(user.badge)
        user.nearby.append(self.user_id)
        user.nearby_loc.append(self.locations[-1])
        user.queue.append(self.badge)
        # send badges one-by-one

    if len(self.queue) > 0:
      print "send badge to user %d" % (self.user_id)
      tmp = self.queue[0]
      self.queue = self.queue[1:]
      return tmp
    else:
      return "no new badge"

  def save_badge(self,badge):
    k = 5
    self.badge = badge
    arr = [int(x) for x in badge.split(',')]
    pixels = [0 for x in xrange(8*8*k*k)]
    for i in xrange(64):
      color = (arr[3*i],arr[3*i+1],arr[3*i+2])
      x = i % 8
      y = i / 8
      for a in xrange(k):
        for b in xrange(k):
          pixels[(y*k+a)*8*k + (x*k+b)] = color
    im = Image.new("RGB", (8*k,8*k))
    im.putdata(pixels)
    im.save('static/' + str(self.user_id) + '.png')

recent_users = []
id2user = {}

def parseGPS(x):
  tokens = x.split(',')
  date = int(tokens[9][:2])
  time = int(tokens[1][:6])

  latitude = tokens[3]
  latitude = int(latitude[:2]) + float(latitude[2:])/60.0
  if tokens[4] == 'S':
    latitude = -latitude

  longtitude = tokens[5]
  longtitude = int(longtitude[:3]) + float(longtitude[3:])/60.0
  if tokens[6] == 'W':
    longtitude = -longtitude
  return ([date, time], [latitude, longtitude])

def filter_recent(users, datetime):
  ret = []
  for x_user in users:
    x_datetime = x_user.datetime
    if datetime[0] == x_datetime[0]:
      if datetime[1] - x_datetime[1] < 100: # 1 minute
        ret.append(x_user)
    elif datetime[0] + 1 == x_datetime[0]:
      if (246000 - datetime[1]) + x_datetime[1] < 100:
        ret.append(x_user)
  return ret

def filter_near(users, my_loc):
  ret = []
  for user in users:
    loc = user.locations[-1]
    if abs(loc[0] - my_loc[0]) < 0.0005 and abs(loc[1] - my_loc[1]) < 0.0005:
      ret.append(user)
  return ret

def report_status(user_id, gps):
  if len(gps.split(',')) < 10:
    print "Invalid GPS data"
    return

  if not(user_id in id2user):
    id2user[user_id] = User(user_id)
  user = id2user[user_id]
  datetime, loc = parseGPS(gps)
  global recent_users
  recent_users = filter_recent(recent_users, datetime)
  nearby_users = filter_near(recent_users, loc)
  print "recent_users = ", [x.user_id for x in recent_users]
  print "nearby_users = ", [x.user_id for x in nearby_users]
  if not user in recent_users:
    recent_users.append(user)
  return user.ping(datetime, loc, nearby_users)

def save_badge(user_id, badge):
  if not(user_id in id2user):
    id2user[user_id] = User(user_id)
  user = id2user[user_id]
  user.save_badge(badge)

def get_map(user_id):
  if user_id in id2user:
    user = id2user[user_id]
    f = open('map.html','r')
    html = f.read()
    f.close()
    return html.replace('$1',str(user.locations))\
        .replace('$2',str(user.nearby_loc))\
        .replace('$3', ','.join(['"/static/' + str(x) + '.png"' for x in user.nearby]))
  else:
    return "user_id = %d not found" % (user_id)

def setup():
  print "set up..."
  save_badge(1,','.join(str(random.randint(0,255)) for x in xrange(64*3)))
  save_badge(2,','.join(str(0) for x in xrange(64*3)))
  print report_status(1,'$GPRMC,194509.000,A,3752.2247,N,12216.0287,W,2.03,221.11,260415,,,A*77')
  print report_status(1,'$GPRMC,194519.000,A,3752.3540,N,12215.6180,W,2.03,221.11,260415,,,A*77')
  print report_status(2,'$GPRMC,194520.000,A,3752.5482,N,12215.5005,W,2.03,221.11,260415,,,A*77')
  print report_status(1,'$GPRMC,194529.000,A,3752.5481,N,12215.5004,W,2.03,221.11,260415,,,A*77')
  # print report_status(2,'$GPRMC,194530.000,A,3752.5482,N,12215.7005,W,2.03,221.11,260415,,,A*77')
  # http://localhost:5001/status?id=2&loc=$GPRMC,194530.000,A,3752.5482,N,12215.7005,W,2.03,221.11,260415,,,A*77
  # http://localhost:5001/badge?id=2
  # 174,16,82,166,242,87,244,155,24,192,241,228,24,117,47,130,189,193,201,132,164,132,64,6,101,164,73,243,118,208,72,55,155,159,69,189,139,16,169,71,48,66,199,78,173,112,172,116,195,207,183,113,87,142,180,125,179,136,187,204,161,17,120,83,177,14,80,136,248,6,162,183,35,230,250,169,122,155,95,93,93,100,86,184,130,78,96,210,189,118,148,237,240,74,75,191,244,120,87,84,194,103,57,65,114,248,20,162,78,100,7,84,24,103,101,45,115,167,118,69,98,172,68,141,250,99,58,73,9,231,162,60,26,231,104,172,70,67,226,156,3,82,234,84,234,203,8,149,252,17,157,98,70,6,141,92,189,168,246,233,123,90,15,154,126,174,23,62,32,138,33,30,191,33,165,13,174,28,241,56,79,142,64,167,70,29,212,17,50,250,31,198

if __name__ == "__main__":
  setup()
  user = id2user[1]
  print user.locations
  print user.nearby
  print user.nearby_loc
