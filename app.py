from flask import Flask, jsonify, request
from pymongo import Connection
import datetime
app = Flask(__name__)

db = Connection()['thewall']


@app.route("/api/messages")
def list_messages():	
	messages = db.messages.find().sort([('date_sent', -1)])
	result = []
	for message in messages:
			result.append({
				"name": message.get("name"),
				"message": message.get("message"),
				"date_sent": message.get('date_sent')
			})
	return jsonify(messages=result)

@app.route("/api/message", methods=['POST'])
def post_message():
	data =	{
			"name": request.form.get('name'),
			"message": request.form.get('message'),
			'date_sent' : datetime.datetime.now(),
			}
	db.messages.insert(data)
	del data['_id']		
	return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
