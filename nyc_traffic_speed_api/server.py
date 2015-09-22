#!flask/bin/python
from flask import Flask, jsonify
import data_ingestion
from werkzeug import Response

app = Flask(__name__)



@app.route('/', methods=['GET'])
def get_current_traffic():
	traffic = data_ingestion.current_traffic()
	
	return jsonify({'traffic':traffic})
	
	
if __name__ == '__main__':
    app.run(debug=True)