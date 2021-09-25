import pandas as pd
from flask import Flask, jsonify
import json
app = Flask(__name__)
from csv_to_geojson_converter import convert_csv_to_geojson

DEBUG=True

SHOW_FAILURES = True
SHOW_HORIZON = True
HOST="localhost"
PORT="5000"
PROTOCOL="http"
MODEL_CSV = "./data/aneesh.csv"

# quick fix
# Must be a library for handling this
ROUTES = [	"/",
			"/api",
			"/api/failures",
			"/api/horizon"
			]

ENDPOINTS = [f"{PROTOCOL}://{HOST}:{PORT}{route}" for route in ROUTES] 
if DEBUG:
	print(ENDPOINTS)


def convert():
	convert_csv_to_geojson(MODEL_CSV)


def get_horizon():
	"""return a list of predicted failure points in the next seven days"""
	if SHOW_HORIZON:
		convert()
		horizon_geojson = "./data/horizon.geojson"

		with open(horizon_geojson, "r") as f:
			horizon_geojson = json.load(f)
		return horizon_geojson
	else:
		return []
		

def get_failures():
	"""return a list dictionaries with failure details"""	
	if SHOW_FAILURES:
		fpath = "./data/sample_frontend.json"
		with open(fpath,"r") as f:
			failures_json = json.load(f)

		# failures = []
		return failures_json
	else:
		return []


def render_endpoint_list():

	routes_el_list = ""
	
	for endpoint, route in zip(ENDPOINTS,ROUTES):
		routes_el_list += f"<li><a href={endpoint}>{route}</a></li>"
	
	return f"""<h4>Enpoints</h4>
				<ul>{routes_el_list}</ul>
			"""


@app.route('/')
def hello():
	

	return """
	<h1>Siemens  - Track Bugscreen</h1>
	<img src="http://hackzurich.siemens.cool/2021/2021-website/img/LeimbachZetzwilMuffe_delay120_loop0.c037c005.gif" height=400></img>
	
	""" + render_endpoint_list()



@app.route('/api')
def api_root():
	
	return render_endpoint_list()

@app.route('/api/horizon')
def horizon_summary():
	horizon_summary = get_horizon()

	if horizon_summary:
		return jsonify(results=horizon_summary)
	else:
		return {"msg":"oracle not available"}


@app.route('/api/failures')
def failure_summary():
	
	failures_json = get_failures()

	if failures_json:
		return jsonify(results=failures_json)
	else:
		return {"msg":"no failures"}


if __name__ == '__main__':
	app.run(host=HOST,port=PORT, debug=DEBUG)
