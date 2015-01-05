import twitter
import json
import requests
import grequests
import gevent
import time
import semantria

api = twitter.Api(consumer_key='',
                      consumer_secret='',
                      access_token_key='',
                      access_token_secret='')

SEMANTRIA_KEY = ''
SEMANTRIA_SECRET = ''

def onError(sender, result):
    print("\n", "ERROR: ", result)

def sentiment_search(parameter):
	search = api.GetSearch(term=parameter,result_type="recent",count=5)
	responses = []
	tweets = []

	session = semantria.Session(SEMANTRIA_KEY,SEMANTRIA_SECRET,use_compression=True)
	session.Error += onError

	for s in search:
		base = "https://app.viralheat.com/social/api/sentiment"
		apikey = "Ha2EFFlX0vwr3y2Ctlyk"
		text = s.text
		time_zone = s.user.time_zone
		
		#Code for viralheat API
		"""
		url = base + "?api_key=" + apikey +"&text=" +text
		resp = requests.get(url)
		responses += [json.loads(resp.text)]
		time.sleep(6)
		"""
		tweets += [text]
	
	#Code for Semantria API
	results = {"positive":0,"negative":0,"neutral":0}
	average = 0.0

	i = 1
	for t in tweets:
		doc = {"id" :str(i),"text":t}
		status = session.queueDocument(doc)
		i +=1

	while len(responses) < len(tweets):
		status = session.getProcessedDocuments()
		for item in status:
			responses.append(item)

	for x in responses:
		value = x["sentiment_score"]
		polarity = x["sentiment_polarity"]
		average += value
		if(polarity == "positive"):
			results["positive"] += 1
		elif(polarity == "negative"):
			results["negative"] += 1
		elif(polarity == "neutral"):
			results["neutral"] += 1
		else:
			continue

	overall = float(average)/float(len(responses))
	return overall,results
	