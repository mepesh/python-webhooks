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
#     response = death_global()
    intent = data['queryResult']['intent']['displayName']
    print (intent)

    if(intent == "nepal data int"):
      url = "https://nepalcorona.info/api/v1/data/nepal"
      response = requests.get(url)
      todos = json.loads(response.text)
      data = todos['tested_total']

      response = "In Nepal Total Cases : "+todos['tested_total']+ " among them "+todos["tested_negative"]+" tested negative and only "+todos["tested_positive"]+" tested positive and 0 death. "
      reply = { "fulfillmentText": response }
      

    elif(intent == "news-nepal-int"):
    	url = "https://nepalcorona.info/api/v1/news"
    	response = requests.get(url)
    	news = json.loads(response.text)
    	data = news['data']
    	data1 = data[0]
    	data2 = data[1]
    	data3 = data[2]
    	response1 = [
      {
        "payload": {
          "facebook": {
            "attachment": {
              "payload": {
                "elements": [
                  {
                    "image_url": data1['image_url'],
                    "title": data1['title'],
                    "default_action": {
                      "type": "web_url",
                      "webview_height_ratio": "tall",
                      "url": data1['url']
                    },
                    "buttons": [
                      {
                        "title": "Live Nepal Data",
                        "payload": "live nepal data",
                        "type": "postback"
                      }
                    ]
                    "subtitle": "Click here to view the full News."
                  },
                  {
                    "title": data2['title'],
                    "default_action": {
                      "type": "web_url",
                      "webview_height_ratio": "tall",
                      "url": data2['url']
                    },
                    "buttons": [
                      {
                        "title": "Self Isolation",
                        "payload": "self isolation",
                        "type": "postback"
                      }
                    ]
                    "subtitle": "Click here to view the full News.",
                    "image_url": data2['image_url']
                  },
                  {
                    "image_url": data3['image_url'],
                    "title": data3['title'],
                    "default_action": {
                      "type": "web_url",
                      "webview_height_ratio": "tall",
                      "url": data3['url']
                    },
                    "buttons": [
                      {
                        "title": "Symptoms",
                        "payload": "symptoms",
                        "type": "postback"
                      }
                    ]
                    "subtitle": "Click here to view the full News."
                  }
                ]
                "template_type": "generic"
              }
              "type": "template"
            }
          }
        },
        "platform": "FACEBOOK"
      }
    ]
      
      reply ={"fulfillmentMessages": response1 }
      
    # print (data)
    # query_text = data['queryResult']['queryText']
    # country_code = data['queryResult']['parameters']['geo-country-code']['name']
    # print (country_code)

    # if(query_text=="Live Corona Data"):
    #   response = death_global()

    # if (country =="world"):
    #   response = death_global()
    else:
      response = death_global()
      reply = { "fulfillmentText": response }   
      

    return jsonify(reply)
   

if __name__ == '__main__':
    app.run()

			