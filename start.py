from sentanalysis import sentiment_search
from flask import Flask
from flask import render_template
from flask import request

app = Flask("start")

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/", methods=["POST"])
def search():
	text = request.form['query']
	overall,results = sentiment_search(text)
	print overall
	positive = results["positive"]	
	negative = results["negative"]
	neutral = results["neutral"]
	if(overall > -0.1 and overall < 0.1):
		return render_template("results.html",feeling="neutral",pos=positive,neg=negative,neut=neutral)
	elif(overall > 0.1):
		return render_template("results.html",feeling="positive",pos=positive,neg=negative,neut=neutral)
	else:
		return render_template("results.html",feeling="negative",pos=positive,neg=negative,neut=neutral)

app.run()