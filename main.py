from flask import Flask, jsonify, request
import requests, json, random
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# page = requests.get("https://www.worldometers.info/coronavirus/")
# soup = BeautifulSoup(page.content, 'html.parser')
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

# Initialize application
app = Flask(__name__)


@app.route("/")
def hello():
    return "Flask setup"

def sheets_row_writer(data_list):
  print("sheets method invoked")
  credentials = ServiceAccountCredentials.from_json_keyfile_name('mechnepal-test-54c4387178d9.json', scope)
  client = gspread.authorize(credentials)
  sh = client.open('corona-help-resource-management')
  worksheet = sh.get_worksheet(1)
  # worksheet = client.open('corona-help-resource-management').BloodPal
  worksheet.append_row(data_list) 
  print("Write complete")


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

      response2 = "In Nepal Total Tested : "+str(todos['tested_total'])+ " among them "+str(todos["tested_negative"])+" tested negative and only "+str(todos["tested_positive"])+" tested positive  "+str(todos["in_isolation"])+" are in isolation and "+str(todos["deaths"])+" deaths. "
      print (response2)
      response = [
      {
        "quickReplies": {
          "title": response2,
          "quickReplies": [
            "World Corona Data",
            "Online Risk Assement"
          ]
        },
        "platform": "FACEBOOK"
      },
        {
          "text":{"text":["Dummy text"]}
        }
        
        ]

      reply = { "fulfillmentMessages": response }
      

    elif(intent == "news-nepal-int"):
      url = "https://nepalcorona.info/api/v1/news"
      response = requests.get(url)
      news = json.loads(response.text)
      data = news['data']
      data1 = data[0]
      data2 = data[1]
      data3 = data[2]
      # response1 = "Here are the latest news \n"+data1['url']+"\n"+data2['url']+"\n"+data3['url']
      response2 = [{
        "card":{
        "title":data1['title'],
        "subtitle":"Source: "+data1['source']+" >>",
        "imageUri":data1['image_url'],
        "buttons":[
        {
        "text":"Read Full Story",
        "postback":data1['url']
        },
        {
        "text":"Corona Symptoms",
        "postback":"symptoms"
        }
        ]
        },
        "platform":"FACEBOOK"
        },
        {
          "text":{"text":["Dummy text"]}
        },
        {
        "card":{
        "title":data2['title'],
        "subtitle":"Source "+data2['source']+" >>",
        "imageUri":data2['image_url'],
        "buttons":[
        {
        "text":"Read Full Story",
        "postback":data2['url']
        },
        {
        "text":"Live Nepal Data",
        "postback":"live-nepal-data"
        }
        ]
        },
        "platform":"FACEBOOK"
        },
        {
          "text":{"text":["Dummy text"]}
        },
        {
        "card":{
        "title":data3['title'],
        "subtitle":"Source "+data3['source']+" >>",
        "imageUri":data3['image_url'],
        "buttons":[
        {
        "text":"Read Full Story",
        "postback":data3['url']
        },
        {
        "text":"Self Isolation",
        "postback":"self isolation"
        }
        ]
        },
        "platform":"FACEBOOK"
        },
        {
          "text":{"text":["Dummy text"]}
        }

      ]

      reply = { "fulfillmentMessages": response2 }

    elif(intent == "i need help main int - yes"):
      print (intent)
      name = data['queryResult']['parameters']['name-people']
      place = data['queryResult']['parameters']['name-place']
      item_required = data['queryResult']['parameters']['help-ent']
      phone = data['queryResult']['parameters']['phone-number']
      ilist = [item_required[0],name[0],phone[0],place[0]]
      for v in ilist:
        print (v)


      sheets_row_writer(ilist)

      # response =" Info updated Will contact u asap !"
      response2 = "Hello "+name[0]+" so you are looking for "+item_required[0]+" Your location is "+place[0]+" One of our Team will contact you @ " +phone[0]+" soon !"
      response = [

      {
        "quickReplies": {
          "title": response2,
          "quickReplies": [
            "Call a Doctor",
            "Get Online Support"
          ]
        },
        "platform": "FACEBOOK"
      },
        {
          "text":{"text":["Dummy text"]}
        }
        
        ]

      reply = { "fulfillmentMessages": response }

    elif(intent=="test-custom-int"):
      print(intent)

      response = [
      # {
      # "card":{
      #   "title":"Death Total in Nepal",
      #   "subtitle":"As of Now  ",
      #   "imageUri":"http://exceltech.com.np/wp-content/uploads/2020/03/csm_corona_live_27eedc0a5d.jpg",
      #   },
      #   "platform":"FACEBOOK"
      #   },
      #   {
      #     "text":{"text":["Dummy text"]}
      #   },

      {
        "quickReplies": {
          "title": "More Video about Corona Prevention Here is a video from NDFN Here is a video from NDFN Here is a video from NDFN ",
          "quickReplies": [
            "Self Isolation",
            "Live Corona Data"
          ]
        },
        "platform": "FACEBOOK"
      },
        {
          "text":{"text":["Dummy text"]}
        }
        
        ]
      reply = { "fulfillmentMessages": response }
 
    elif(intent=="online-risk-assement"):
      # ff = data['queryResult']['fulfillmentMessages']['card']['buttons']['text']
      print(intent)
      # print(ff[0])

      response = [{
        "card":{
        "title":"What is your Body Temperature",
        "subtitle":"Give honest answer",
        "imageUri":"http://exceltech.com.np/wp-content/uploads/2020/03/csm_corona_live_27eedc0a5d.jpg",
        "buttons":[
        {
        "text":"Normal [98F - 98.6F]",
        "postback":"ora-temperature-int"
        },
        {
        "text":"Mild [98.6F -102F]",
        "postback":"ora-temperature-int"
        }
        ]
        },
        "platform":"FACEBOOK"
        },
        {
          "text":{"text":["Dummy text"]}
        }
        
        ]

      reply = { "fulfillmentMessages" : response }
# Find the temperature from here
    # elif(intent=="ora-temperature-int"):
    #   global temp 
    #   ff = data['originalDetectIntentRequest']['payload']['data']['postback']['title']
    #   if(ff=="Normal [98F - 98.6F]"):
    #     temp = 1
    #   else:
    #     temp=2
      
    #   # response = "Your temperature is ",temp," !."
    #   print("temp inside ora-temperature-int")
    #   print(temp)
      # response2 = [{
      #   "card":{
      #   "title":"What is your Body Temperature",
      #   "subtitle":"Give honest answer",
      #   "imageUri":"http://exceltech.com.np/wp-content/uploads/2020/03/csm_corona_live_27eedc0a5d.jpg",
      #   "buttons":[
      #   {
      #   "text":"Male",
      #   "postback":"ora-sex-int"
      #   },
      #   {
      #   "text":"Female",
      #   "postback":"ora-sex-int"
      #   },
      #   {
      #   "text":"Others",
      #   "payload":"ora-sex-int"
      #   }
      #   ]
      #   },
      #   "platform":"FACEBOOK"
      #   },
      #   {
      #     "text":{"text":["Dummy text"]}
      #   }
        
      #   ]




    #   reply = { "fulfillmentMessages": response2 }


    # Find the sex from here
    elif(intent=="ora-sex-int" or intent=="ora-temperature-int"):
      global temp
      if(intent=="ora-temperature-int"):
        ff = data['originalDetectIntentRequest']['payload']['data']['postback']['title']
        if(ff=="Normal [98F - 98.6F]"):
          temp=1
        else:
          temp=2
        
        response2 = [{
        "card":{
        "title":"What is your Body Temperature",
        "subtitle":"Give honest answer",
        "imageUri":"http://exceltech.com.np/wp-content/uploads/2020/03/csm_corona_live_27eedc0a5d.jpg",
        "buttons":[
        {
        "text":"Male",
        "postback":"ora-sex-int"
        },
        {
        "text":"Female",
        "postback":"ora-sex-int"
        },
        {
        "text":"Others",
        "payload":"ora-sex-int"
        }
        ]
        },
        "platform":"FACEBOOK"
        },
        {
          "text":{"text":["Dummy text"]}
        }
        
        ]
        reply = { "fulfillmentMessages" : response2}
        return jsonify(reply)

      else:
        global sex
        ff = data['originalDetectIntentRequest']['payload']['data']['postback']['title']
        if(ff=="Male"):
          sex=1
        elif(ff=="Female"):
          sex=2
        else:
          sex=3

        response = "The returened values are "+str(temp)+"."+str(sex)+"."
        reply = { "fulfillmentText" : response}
        return jsonify(reply)


    elif(intent=="faq-que-ans-int"):
      print (data)
      ff = data['originalDetectIntentRequest']['payload']['data']['message']['text']
      url = "https://nepalcorona.info/api/v1/faqs"
      response = requests.get(url)
      todos = json.loads(response.text)
      rand = random.randrange(0, 45, 1)
      opt3 = ["Live Nepali Data","Latest Nepali News","Symptoms","Preventions","Self Isolation","Play Corona Quiz"]
      faqs = todos['data']
      faq = faqs[rand]
      if(ff=="English FAQ" or ff =="More Quizzles" or ff =="भाषा परिवर्तन"):
        randq= faq['question']
        randa = faq['answer']
        opt1 = "More Quizzles"
        opt2 = "Switch Language"
      else:
        randq = faq['question_np']
        randa = faq['answer_np']
        opt1 = "अरु देखाउनुहोस >>"
        opt2 = "भाषा परिवर्तन"

      response2 = "Q. "+randq+"\n A. "+randa+"\n"
      response = [{
        "text": {
          "text": [
            randq
          ]
        },
        "platform": "FACEBOOK"
      },{
          "text":{"text":["Dummy text"]}
        },

      {
        "quickReplies": {
          "title": randa,
          "quickReplies": [
            opt1,
            opt2,
            random.choice(opt3)
          ]
        },
        "platform": "FACEBOOK"
      },
        {
          "text":{"text":["Dummy text"]}
        }
        
        ]
      reply = { "fulfillmentMessages": response }

    elif(intent=="bloodpal-need-blood-main-int - yes"):
      print (intent)
      print (data)
      # response = "Test this feature"

      blood_group = data['queryResult']['parameters']['blood-group']
      blood_amount = data['queryResult']['parameters']['blood-pint']
      location = data['queryResult']['parameters']['blood-location']
      case = data['queryResult']['parameters']['blood-case']
      date = data['queryResult']['parameters']['blood-date']
      phone = data['queryResult']['parameters']['blood-number']
      ilist = [blood_group,blood_amount,location,case,date,phone]
      sheets_row_writer(ilist)
      response = "Successfully requested "+blood_group+" blood "+str(blood_amount)+" pints. We will contact you in the provided number "+phone+" Thank you ."
      reply = { "fulfillmentText": response }


    else:
      response = death_global()
      reply = { "fulfillmentText": response }   
      

    return jsonify(reply)
   

if __name__ == '__main__':
    
    app.run()

      

      
      
      
