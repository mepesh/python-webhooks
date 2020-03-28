from flask import Flask, jsonify, request
import requests, json
from bs4 import BeautifulSoup

# page = requests.get("https://www.worldometers.info/coronavirus/")
# soup = BeautifulSoup(page.content, 'html.parser')

# Initialize application
app = Flask(__name__)


@app.route("/")
def hello():
		return "Flask setup"

def death_global():
	page = requests.get("https://www.worldometers.info/coronavirus/")
	soup = BeautifulSoup(page.content, 'html.parser')
	
	result = soup.find_all("div", {"class":"maincounter-number"})
	cases_list = []

	active = soup.find("div", {"class":"number-table-main"})
	active_cases = active.text

	for res in result:
		cases_list.append(res.text)

	return "There are"+cases_list[0]+" Total cases out of which"+cases_list[1]+" have died and"+cases_list[2]+" have recovered . There are still "+active_cases+" active cases."

app.route("/death/global", methods=['POST'])
def death_global_api():
	data = request.get_json(silent=True)
	page = requests.get("https://www.worldometers.info/coronavirus/")
	response = death_global()
	reply = { "fulfillmentText": response }    
	return jsonify(reply)
	

def death_country(id):
		idu = id.upper()
		page = requests.get("https://www.worldometers.info/coronavirus/country/"+id+"/")
		soup = BeautifulSoup(page.content, 'html.parser')
		result = soup.find_all("div", {"class":"maincounter-number"})
		
		active = soup.find("div", {"class":"number-table-main"})
		active_cases = active.text
		cases_list = []
		for res in result:
			cases_list.append(res.text)

		return "In " +idu+" There are"+cases_list[0]+"Total cases out of which"+cases_list[1]+"are dead and"+cases_list[2]+"have already recovered . There are still "+active_cases+ " active cases ."

@app.route('/get_country_detail', methods=['POST'])
def get_country_detail():
		data = request.get_json(silent=True)
# 		response = death_global()
		intent = data['queryResult']['intent']['displayName']
		print (intent)

		if(intent == "nepal data int"):
			url = "https://nepalcorona.info/api/v1/data/nepal"
			response = requests.get(url)
			todos = json.loads(response.text)
			data = todos['tested_total']

			response = "In Nepal Total Cases : "+todos['tested_total']+ " among them "+todos["tested_negative"]+" tested negative and only "+todos["tested_positive"]+" tested positive and 0 death. "
			reply = { "fulfillmentMessages": response }
			

		elif(intent == "news-nepal-int"):
			response = [
      {
        "payload": {
          "facebook": {
            "attachment": {
              "payload": {
                "elements": [
                  {
                    "image_url": "https://assets-cdn-usad.kantipurdaily.com/uploads/source/news/kantipur/2020/third-party/corona-1712020080544-600x0.jpg",
                    "title": "सिड्नीमा ४ नेपाली विद्यार्थीमा कोर",
                    "default_action": {
                      "type": "web_url",
                      "webview_height_ratio": "tall",
                      "url": "https://ekantipur.com/diaspora/2020/03/28/158537088723791264.html?fbclid=IwAR2MMgwa179CvFYdC6N3iq0QDIZe43yJRGFwV0gekHOyAFC62gdhIvmhi2g"
                    },
                    "buttons": [
                      {
                        "title": "Live Nepal Data",
                        "payload": "live nepal data",
                        "type": "postback"
                      }
                    ],
                    "subtitle": "Here goes your subtitle."
                  },
                  {
                    "title": "कर्णालीको क्वारेन्टाइन : एउटै बेडमा दुईजना, मास्कको सट्टा गलब",
                    "default_action": {
                      "type": "web_url",
                      "webview_height_ratio": "tall",
                      "url": "https://ekantipur.com/pradesh-6/2020/03/28/15853746010691926.html"
                    },
                    "buttons": [
                      {
                        "title": "Self Isolation",
                        "payload": "self isolation",
                        "type": "postback"
                      }
                    ],
                    "subtitle": "Here goes your subtitle.",
                    "image_url": "https://assets-cdn-usad.kantipurdaily.com/uploads/source/news/kantipur/2020/miscellaneous/karnali-2832020064857-600x0.jpg"
                  }
                ],
                "template_type": "generic"
              },
              "type": "template"
            }
          }
        },
        "platform": "FACEBOOK"
      }
    ]
    			reply ={"fulfillmentMessages": response }
    	
		# print (data)
		# query_text = data['queryResult']['queryText']
		# country_code = data['queryResult']['parameters']['geo-country-code']['name']
		# print (country_code)

		# if(query_text=="Live Corona Data"):
		# 	response = death_global()

		# if (country =="world"):
		# 	response = death_global()
		else:
			response = death_global()
			reply = { "fulfillmentMessages": response }   
			

		return jsonify(reply)

		
		

if __name__ == '__main__':
		app.run()
