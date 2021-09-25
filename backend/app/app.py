import pandas as pd
from flask import Flask, jsonify
import json
app = Flask(__name__)

DEBUG=True

SHOW_FAILURES = True
HOST="localhost"
PORT="5000"
PROTOCOL="http"

# quick fix
# Must be a library for handling this
ROUTES = [	"/",
			"/failures",
			]

ENDPOINTS = [f"{PROTOCOL}://{HOST}:{PORT}{route}" for route in ROUTES] 
if DEBUG:
	print(ENDPOINTS)


def get_failures():
	"""return a list dictionaries with failure details"""	
	if SHOW_FAILURES:
		fpath = "./data/sample_frontend.json"
		with open(fpath,"r") as f:
			failures_json = json.load(f)
	
		# failures = "[{"DateTime": "2020-01-22 00:00:01", "ID": 0, "AreaNumber": 9, "Track": 5, "PositionNoLeap": 97437, "Latitude": 47.30485483760787, "Longitude": 8.049462113532206, "A1_TotalTel": 57595, "A1_ValidTel": 57572, "A2_RSSI": 1.58, "A2_TotalTel": 57231, "A2_ValidTel": 57159, "fault_actual": true, "fault_predicted": true, "fault_probability": 0.050632911392405056}, {"DateTime": "2020-01-22 01:00:01", "ID": 1, "AreaNumber": 9, "Track": 5, "PositionNoLeap": 97437, "Latitude": 47.30485483760787, "Longitude": 8.049462113532206, "A1_TotalTel": 59192, "A1_ValidTel": 59169, "A2_RSSI": 1.58, "A2_TotalTel": 58485, "A2_ValidTel": 58371, "fault_actual": true, "fault_predicted": true, "fault_probability": 0.050632911392405056}, {"DateTime": "2020-01-22 02:00:01", "ID": 2, "AreaNumber": 9, "Track": 5, "PositionNoLeap": 97437, "Latitude": 47.30485483760787, "Longitude": 8.049462113532206, "A1_TotalTel": 59192, "A1_ValidTel": 59169, "A2_RSSI": 1.58, "A2_TotalTel": 58485, "A2_ValidTel": 58371, "fault_actual": true, "fault_predicted": true, "fault_probability": 0.050632911392405056}, {"DateTime": "2020-01-22 03:00:01", "ID": 3, "AreaNumber": 9, "Track": 5, "PositionNoLeap": 97437, "Latitude": 47.30485483760787, "Longitude": 8.049462113532206, "A1_TotalTel": 59192, "A1_ValidTel": 59169, "A2_RSSI": 1.58, "A2_TotalTel": 58485, "A2_ValidTel": 58371, "fault_actual": true, "fault_predicted": true, "fault_probability": 0.050632911392405056}, {"DateTime": "2020-01-22 04:00:01", "ID": 4, "AreaNumber": 9, "Track": 5, "PositionNoLeap": 97437, "Latitude": 47.30485483760787, "Longitude": 8.049462113532206, "A1_TotalTel": 59192, "A1_ValidTel": 59169, "A2_RSSI": 1.58, "A2_TotalTel": 58485, "A2_ValidTel": 58371, "fault_actual": true, "fault_predicted": true, "fault_probability": 0.050632911392405056}, {"DateTime": "2020-01-22 05:00:01", "ID": 5, "AreaNumber": 9, "Track": 5, "PositionNoLeap": 97437, "Latitude": 47.30485483760787, "Longitude": 8.049462113532206, "A1_TotalTel": 10559, "A1_ValidTel": 10559, "A2_RSSI": 1.44, "A2_TotalTel": 5458, "A2_ValidTel": 5426, "fault_actual": true, "fault_predicted": true, "fault_probability": 0.05555555555555555}, ]
		# failures = []
		return failures_json
	else:
		return []



@app.route('/')
def hello():
	

	return """
	<h1>Siemens  - Track Bugscreen</h1>
	<img src="http://hackzurich.siemens.cool/2021/2021-website/img/LeimbachZetzwilMuffe_delay120_loop0.c037c005.gif" height=400></img>
	
	"""


@app.route('/api')
def api_root():
	
	
	routes_el_list = ""
	for endpoint, route in zip(ENDPOINTS,ROUTES):
		routes_el_list += f"<li><a href={endpoint}>{route}</a></li>"
	

	return f"<h1>Enpoints</h1><ul>{routes_el_list}</ul>"


@app.route('/failures')
def failure_summary():
	
	failures_json = get_failures()

	if failures_json:
		return jsonify(results=failures_json)
	else:
		return {"msg":"no failures"}


if __name__ == '__main__':
	app.run(host=HOST,port=PORT, debug=DEBUG)
