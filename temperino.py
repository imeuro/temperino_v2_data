import urllib, json, ast
from pprint import pprint

# READ REMOTE JSON:
url = "https://nas.imeuro.io/temperino_v2_data/readings.json"
response = urllib.urlopen(url)
d = json.loads(response.read())
d = ast.literal_eval(json.dumps(d))
#print(d)

Program = d["program"]["mode"]
Cur_temp = d["inside"]["temp"]

# Target Temp
if d["program"]["mode"] == "MANUAL" :
	T_temp = d["program"]["temp"]
elif d["program"]["mode"] == "T3" :
	T_temp = 20.5
elif d["program"]["mode"] == "T2" :
	T_temp = 17.5
else : # AUTO or OFF: never below 8 C
	T_temp = 8


# pprint('Program: ' + Program + 'Target temp:' + T_temp + 'Current temp:' + Cur_temp)
# print("Program:\t" + Program + "\r\nTarget temp:\t" + T_temp)
# print('Current temp:' + Cur_temp)

if Cur_temp <= T_temp :
	# Relay: off --> heating ON
	print('heating ON')
else :
	# Relay: on --> heating OFF
	print('heating OFF')
