from flask import Flask
import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.worldometers.info/coronavirus/")
soup = BeautifulSoup(page.content, 'html.parser')

# Initialize application
app = Flask(__name__)


@app.route("/")
def hello():
    return "Flask setup"

 @app.route("/death/global")
 def death_global():
 	result = soup.find_all("div", {"class":"maincounter-number"})
    cases_list = []
    for res in result:
        cases_list.append(res.text)
    return "There are"+cases_list[0]+" Total cases out of which"+cases_list[1]+" have died and"+cases_list[2]+" have recovered ."

if __name__ == '__main__':
    app.run()
