from flask import Flask, jsonify, request
import requests, json, random
from bs4 import BeautifulSoup
import gspread
import pandas as pd
import dataservices as dss
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

def sheets_row_writer_donor(data_list_donor):
  print("donor sheets method invoked")
  credentials = ServiceAccountCredentials.from_json_keyfile_name('mechnepal-test-54c4387178d9.json', scope)
  client = gspread.authorize(credentials)
  sh = client.open('corona-help-resource-management')
  worksheet = sh.get_worksheet(2)
  # worksheet = client.open('corona-help-resource-management').BloodPal
  worksheet.append_row(data_list_donor) 
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
    intent = data['queryResult']['intent']['displayName']
    print (intent)
    
    def nepal_data_int():
      url = "https://nepalcorona.info/api/v1/data/nepal"
      response = requests.get(url)
      todos = json.loads(response.text)
      data = todos['tested_total']
      

      # response2 = "In Nepal Total Tested : "+str(todos['tested_total'])+ " among them "+str(todos["tested_negative"])+" tested negative and only "+str(todos["tested_positive"])+" tested positive  "+str(todos["in_isolation"])+" are in isolation and "+str(todos["deaths"])+" deaths. "
      response2 = "In Nepal \n Tested Total: "+str(todos['tested_total'])+" \n Tested Positive :"+str(todos["tested_positive"])+" \n Recovered: "+str(todos["recovered"])+"\n"+"RDT Tested: "+str(todos["tested_rdt"])+"\n In ISolation: "+str(todos["in_isolation"])+"\n Quarantined: "+str(todos["quarantined"])+"\n"
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
      return reply

      
    def news_nepal_int():
      url = "https://nepalcorona.info/api/v1/news"
      response = requests.get(url)
      news = json.loads(response.text)
      data = news['data']
      data1 = data[0]
      data2 = data[1]
      data3 = data[2]
      
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
        },

      ]

      reply = { "fulfillmentMessages": response2 }
      return reply
    
    def i_need_help_yes():
      name = data['queryResult']['parameters']['name-people']
      place = data['queryResult']['parameters']['name-place']
      item_required = data['queryResult']['parameters']['help-ent']
      phone = data['queryResult']['parameters']['phone-number']
      ilist = [item_required[0],name[0],phone[0],place[0]]
      sheets_row_writer(ilist)
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
      return reply

    def faq_ques_ans():
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

      return reply
    
    def blood_pal_yes():
      print (intent)
      print (data)
      blood_group = data['queryResult']['parameters']['blood-group']
      blood_amount = data['queryResult']['parameters']['blood-pint']
      location = data['queryResult']['parameters']['blood-location']
      case = data['queryResult']['parameters']['blood-case']
      date = data['queryResult']['parameters']['blood-date']
      phone = data['queryResult']['parameters']['blood-number']
      ilist = [blood_group,blood_amount,location,case,date,phone]
      sheets_row_writer(ilist)
      response3 = "For critical case, please contact \n Kathmandu 9880998523 \n Bhaktapur 9880998525 \n Kavre 9869294490 \n Purwanchal 9862176689 \n Chitwan 9801070746 \n Butwal 9807522664 \n Dang 9801920169 \n Stay connected with BloodPal!"
      response = "The following request has been sent. We will contact you shortly. "+blood_group+" blood ("+str(blood_amount)+" ) required for "+case+" at "+location+" On "+date+" - "+phone+" Thank you ."
      response2 = [{
        "text": {
          "text": [
            response
          ]
        },
        "platform": "FACEBOOK"
      },{
          "text":{"text":["Dummy text"]}
        },
        {
        "text": {
          "text": [
            response3
          ]
        },
        "platform": "FACEBOOK"
      },{
          "text":{"text":["Dummy text"]}
        }
        
        ]
      reply = { "fulfillmentMessages": response2 }
      return reply
    
    def blood_pal_donor_yes():
      print (intent)
      print (data)
      permananet_address = data['queryResult']['parameters']['permananet-address']
      height = data['queryResult']['parameters']['height']
      gender = data['queryResult']['parameters']['gender']
      age = data['queryResult']['parameters']['age']
      blood = data['queryResult']['parameters']['blood']
      current_address = data['queryResult']['parameters']['current-address']
      email = data['queryResult']['parameters']['email']
      name = data['queryResult']['parameters']['name']
      last_donation= data['queryResult']['parameters']['last-donation']
      weight = data['queryResult']['parameters']['weight']
      number = data['queryResult']['parameters']['number']
      ilist = [name,number,email,current_address,permananet_address,age,height,weight,gender,blood,last_donation]
      sheets_row_writer_donor(ilist)
      response3 = "For critical case, please contact \n Kathmandu 9880998523 \n Bhaktapur 9880998525 \n Kavre 9869294490 \n Purwanchal 9862176689 \n Chitwan 9801070746 \n Butwal 9807522664 \n Dang 9801920169 \n Stay connected with BloodPal!"
      response = "Thank you "+name+" for registration as a blood donor We will contact you at the time of urgency in your area."
      response2 = [{
        "text": {
          "text": [
            response
          ]
        },
        "platform": "FACEBOOK"
      },{
          "text":{"text":["Dummy text"]}
        },
        {
        "text": {
          "text": [
            response3
          ]
        },
        "platform": "FACEBOOK"
      },{
          "text":{"text":["Dummy text"]}
        }
        
        ]
      reply = { "fulfillmentMessages": response2 }
      return reply

    def world_data_live():
      response = death_global()
      reply = { "fulfillmentText": response }
      return reply
    
    def district_data_live():
      text = dss.district_all_summary()
      # district = data['queryResult']['parameters']['district']
      # district_data= pd.read_csv('https://raw.githubusercontent.com/mepesh/python-dashboard-covid19/master/test_data_cases_states.csv')
      # district_data["district"] = district_data["district"].str.lower()
      # dr = district_data.loc[district_data['district'] == district.lower()]
      # if(len(dr)==0):
      #   opt2="Search Another District"
      #   response2=("No data Found for "+district+"")
      # else:
      #   opt2="Nepal Data Live"
      #   drl= dr.values.tolist()
      #   response2 = ("In "+drl[0][0]+" district there are "+str(drl[0][3])+" CASES "+str(drl[0][4])+" in ISOLATION "+str(drl[0][5])+" DEATHS and "+str(drl[0][6])+" RECOVERED .")
      
      response = [
      {
        "quickReplies": {
          "title": text,
          "quickReplies": [
            "Provience Data",
             "Nepali Stats"
          ]
        },
        "platform": "FACEBOOK"
      },
      {
        "text":{"text":["Dummy text"]}
      }   
      ]

      reply = { "fulfillmentMessages": response }
      return reply
          
    def province_data_live():
      text = dss.provience_all_summary()
      print(text)
      response = [
      {
        "text": {
        "text": [
          text
        ]
      },
        "platform": "FACEBOOK"
      },
      {
        "text":{"text":["Dummy text"]}
      }   
      ]

      reply = { "fulfillmentMessages": response }
      return reply

    def nepal_data_new_main_int():
      url = "https://nepalcorona.info/api/v1/data/nepal"
      response = requests.get(url)
      todos = json.loads(response.text)
      covid_df = dss.create_covid_df()
      
      response2 = "In Nepal \n Tested Total: "+str(todos['tested_total'])+" \n Tested Positive :"+str(todos["tested_positive"])+" \n Recovered: "+str(todos["recovered"])+"\n"+"RDT Tested: "+str(todos["tested_rdt"])+"\n In ISolation: "+str(todos["in_isolation"])+"\n Quarantined: "+str(todos["quarantined"])+"\n"
      response_summary = dss.affected_summary()

      response = [
      {
      "text": {
        "text": [
          response2
        ]
      },
      "platform": "FACEBOOK"
      },
      {
      "text": {
        "text": [
          ""
        ]
      }
      },
      {
      "card":{
      "title": "Covid-19 Nepal | Stats",
      "subtitle":response_summary,
      # "subtitle": "Find details by Province, Municipals and Districts for Nepal",
      "imageUri": "https://miro.medium.com/max/1400/1*35jjrjxz8iI5f2r8hMi8PQ.png",
      "buttons":[
      {
      "text":"Provience Wise Data",
      "postback":"province data int"
      },
      {
      "text":"District Wise Data",
      "postback":"district data int"
      },
      {
      "text":"Mun/Vdc  Data",
      "postback":"district data int"
      }
      ]
      },
      "platform":"FACEBOOK"
      },
      {
        "text":{"text":["Dummy text"]}
      },
      ]


      reply = { "fulfillmentMessages": response }
      return reply

    def default():
      return "Incorrect Data"

    switcher = {
    "nepal data int": nepal_data_int,
    "news-nepal-int": news_nepal_int,
    "i need help main int - yes": i_need_help_yes,
    "faq-que-ans-int": faq_ques_ans,
    "bloodpal-need-blood-main-int - yes": blood_pal_yes,
    "data world int": world_data_live,
    "district data int": district_data_live,
    "province data int": province_data_live,
    "bloodpal-become-donor-main-int":blood_pal_donor_yes,
    "nepal-data-new-main-int": nepal_data_new_main_int
    }
    
    def switch(intentname):
      return switcher.get(intentname, default)()

    reply = switch(intent)
    return jsonify(reply)
    

if __name__ == '__main__':
    
    app.run()
