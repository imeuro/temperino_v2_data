import sys
import Adafruit_DHT as dht
import urllib, json, ast
#import os

humi,temp = dht.read_retry(22, 4)
print ('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temp, humi))

# READ REMOTE JSON:
#url = "http://nas.imeuro.io/temperino_v2_data/readings.json"
#response = urllib.urlopen(url)
#d = json.loads(response.read())
#d = ast.literal_eval(json.dumps(d))

#filename = 'http://nas.imeuro.io/temperino_v2_data/readings.json'
#with open(filename, 'r') as json_data:
#    d = json.load(json_data)
#d["inside"]["temp"] = round(temp, 1)
#d["inside"]["humi"]	= round(humi, 1)

saveurl = "http://nas.imeuro.io/temperino_v2/data/savedata.php"
urllib.urlopen(saveurl+'?temp_in='+str(round(temp, 1))+'&humi_in='+str(round(humi, 1)))

#os.remove(filename)
#with open(filename, 'w') as json_data:
#    json.dump(d, json_data, indent=4)
