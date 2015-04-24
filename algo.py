class User:
  def __init__(self, user_id):
    self.locations = []
    self.loc = None
    self.datetime = None
    self.user_id = user_id

  def ping(self,datetime, loc):
    self.locations.append(loc)
    self.datetime = datetime
    self.loc = loc

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

def filter_recent(lst, datetime):
  ret = []
  for x_id in lst:
    x_user = id2user[x_id]
    x_datetime = x_user.datetime
    if datetime[0] == x_datetime[0]:
      if datetime[1] - x_datetime[1] < 100: # 1 minute
        ret.append(x_id)
    elif datetime[0] + 1 == x_datetime[0]:
      if (246000 - datetime[1]) + x_datetime[1] < 100:
        ret.append(x_id)
  return ret

def nearby_users(lst, my_id, my_loc):
  pass
    

def report_status(user_id, gps):
  print "gps = ", gps.split(',')
  if len(gps.split(',')) < 10:
    print "Invalid GPS data"
    return
  if not(user_id in id2user):
    id2user[user_id] = User(user_id)
  user = id2user[user_id]
  datetime, loc = parseGPS(gps)
  user.ping(datetime, loc)
  #recent_users = filter_recent(recent_users, datetime)
  # incomplete

def get_map(user_id):
  if user_id in id2user:
    user = id2user[user_id]
    print "#locs = ", len(user.locations)
    f = open('map.html','r')
    html = f.read()
    f.close()
    return html.replace('$1',str(user.locations))
  else:
    return "user_id = %d not found" % (user_id)

def setup():
  print "set up..."
  id2user[1] = User(1)
  report_status(1,'$GPRMC,194509.000,A,4042.6142,N,07400.4168,W,2.03,221.11,160412,,,A*77')
  report_status(1,'$GPRMC,194510.000,A,4042.7142,N,07400.4168,W,2.03,221.11,160412,,,A*77')
  report_status(1,'$GPRMC,194511.000,A,4042.7142,N,07400.5168,W,2.03,221.11,160412,,,A*77')

