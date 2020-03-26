from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

# page = requests.get("https://www.worldometers.info/coronavirus/")
# soup = BeautifulSoup(page.content, 'html.parser')

# Initialize application
app = Flask(__name__)


@app.route("/")
def hello():
		return "Flask setup"

# @app.route("/death/global")
def death_global():
	page = requests.get("https://www.worldometers.info/coronavirus/")
	soup = BeautifulSoup(page.content, 'html.parser')
	result = soup.find_all("div", {"class":"maincounter-number"})
	cases_list = []
	for res in result:
		cases_list.append(res.text)

	return "There are"+cases_list[0]+" Total cases out of which"+cases_list[1]+" have died and"+cases_list[2]+" have recovered ."

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
		# print (data)
		query_text = data['queryResult']['queryText']
		country_code = data['queryResult']['parameters']['geo-country-code']['alpha-2']
		print (country_code)

		if(query_text=="Data World"):
			response = death_global()

		# if (country =="world"):
		# 	response = death_global()
		else:
			response = death_country(country)
		
		reply = { "fulfillmentText": response }    
		return jsonify(reply)

if __name__ == '__main__':
		app.run()
