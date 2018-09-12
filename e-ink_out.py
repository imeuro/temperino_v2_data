#!/usr/bin/python
# text encoding: utf-8

#pimoroni inkyphat: 212x104 pixels e-ink screen
from time import strftime
from datetime import datetime, timedelta
import urllib, json, ast

from PIL import Image, ImageFont
import inkyphat

# rounds time to 5min
def roundTime(dt=None, dateDelta=timedelta(minutes=1)):
    roundTo = dateDelta.total_seconds()
    if dt == None : dt = datetime.now()
    seconds = (dt - dt.min).seconds
    # // is a floor division, not a comment on following line:
    rounding = (seconds+roundTo/2) // roundTo * roundTo
    return dt + timedelta(0,rounding-seconds,-dt.microsecond)

# read local JSON file // OLD
# readings = '/var/www/html/temperino_v2/data/readings.json'
# with open(readings, 'r') as json_data:
#     d = json.load(json_data)

# READ REMOTE JSON:
url = "https://nas.imeuro.io/temperino_v2/data/readings.json"
response = urllib.urlopen(url)
d = json.loads(response.read())
d = ast.literal_eval(json.dumps(d))
#print(d)

Rtime = roundTime(datetime.now(),timedelta(minutes=5))
Rdate = strftime('%a, %d %b', Rtime.timetuple())
Rhour = strftime('%H:%M', Rtime.timetuple())

degSign= u'\N{DEGREE SIGN}'

inkyphat.set_colour('red')
inkyphat.set_border(inkyphat.BLACK)


# Partial update if using Inky pHAT display v1
if inkyphat.get_version() == 1:
    inkyphat.show()

# FONTS
font10 = ImageFont.truetype('/var/www/html/temperino_v2_data/fonts/Bitter-Regular.ttf', 10)
font10b = ImageFont.truetype('/var/www/html/temperino_v2_data/fonts/Bitter-Bold.ttf', 10)
font22 = ImageFont.truetype('/var/www/html/temperino_v2_data/fonts/Bitter-Bold.ttf', 22)
font28 = ImageFont.truetype('/var/www/html/temperino_v2_data/fonts/Bitter-Bold.ttf', 28)


# TOP infos
Rdatew, Rdateh = font10.getsize(Rdate)
inkyphat.text((3,-2), str(Rhour), inkyphat.RED, font22)
inkyphat.text((inkyphat.WIDTH-Rdatew-6, 6), str(Rdate+' '), inkyphat.BLACK, font10)
inkyphat.line((3, 23, inkyphat.WIDTH-3, 23), inkyphat.BLACK) # Horizontal separator



# INSIDE readings
insideT = str(d["inside"]["temp"])
insideH = str(d["inside"]["humi"])
inkyphat.text((6,30), "IN: ", inkyphat.RED, font10)
inkyphat.text((35,25), insideT+degSign, inkyphat.RED, font28)
inkyphat.text((35,50), insideH+'%', inkyphat.BLACK, font22)


# OUTSUDE readings
outsideT = str(d["outside"]["temp"])
outsideP = str(d["outside"]["press"])
outsideD = str(d["outside"]["timestamp"])
OUTpressw, OUTpressh = font22.getsize(outsideP)
inkyphat.text((6,80), "OUT: ", inkyphat.RED, font10)
inkyphat.text((35,75), outsideT+degSign, inkyphat.BLACK, font22)
inkyphat.text((90,75), outsideD, inkyphat.BLACK, font10)
#inkyphat.text((100+OUTpressw,82), 'mbar', inkyphat.BLACK, font10)


# HEATER status
Pmode = str(d["program"]["mode"])
if Pmode == 'MANUAL':
	Pmode = 'MAN'
Ptemp = str(d["program"]["temp"])
inkyphat.rectangle((120, 26, inkyphat.WIDTH-3, inkyphat.HEIGHT-3), fill=inkyphat.BLACK, outline=inkyphat.BLACK)
inkyphat.text((130,30), "MODE ", inkyphat.WHITE, font10b)
inkyphat.text((130,45), Pmode, inkyphat.RED, font22)
inkyphat.text((130,80), Ptemp+' ', inkyphat.WHITE, font10b)



inkyphat.show()
