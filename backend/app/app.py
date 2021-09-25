from flask import Flask
app = Flask(__name__)

DEBUG=True

@app.route('/')
def hello():
	return "<h1>Simens  - Track Bugscreen!</h1>"

@app.route('/failures')
def failure_summary():
	return {"msg":"no failures"}


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=DEBUG)
