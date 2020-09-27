from flask import Flask, render_template
import json
import requests
import COVID19Py
from datetime import timedelta, date
import datetime

app = Flask(__name__)

@app.route('/graph')
def graph():
  current_time = datetime.datetime.now()
  def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

  start_date = date(current_time.year, current_time.month, (current_time.day)-10)
  end_date = date(current_time.year, current_time.month, current_time.day)
  cases = []
  deaths = []
  recovered = []
  dates = []
  for single_date in daterange(start_date, end_date):
    graph = (single_date.strftime("%Y-%m-%d"))
    json = requests.get(f'https://covidapi.info/api/v1/global/{single_date}')
    api = json.json()
    print(api)
    print(graph)
    print(single_date)
    recovered.append(api['result']['recovered'])
    deaths.append(api['result']['deaths'])
    cases.append(api['result']['confirmed'])
    dates.append(single_date)
  return render_template('graph.html', recovered=recovered, deaths=deaths, cases=cases, dates=single_date)

@app.route('/')
def main():
  json = requests.get('https://api.covid19api.com/summary')
  json = json.json()
  return render_template('index.html', json=json)

@app.route('/states')
def states():
  states = {
    "AL": "Alabama",
    "AK": "Alaska",
    "AS": "American Samoa",
    "AZ": "Arizona",
    "AR": "Arkansas",
    "CA": "California",
    "CO": "Colorado",
    "CT": "Connecticut",
    "DE": "Delaware",
    "DC": "District Of Columbia",
    "FM": "Federated States Of Micronesia",
    "FL": "Florida",
    "GA": "Georgia",
    "GU": "Guam",
    "HI": "Hawaii",
    "ID": "Idaho",
    "IL": "Illinois",
    "IN": "Indiana",
    "IA": "Iowa",
    "KS": "Kansas",
    "KY": "Kentucky",
    "LA": "Louisiana",
    "ME": "Maine",
    "MH": "Marshall Islands",
    "MD": "Maryland",
    "MA": "Massachusetts",
    "MI": "Michigan",
    "MN": "Minnesota",
    "MS": "Mississippi",
    "MO": "Missouri",
    "MT": "Montana",
    "NE": "Nebraska",
    "NV": "Nevada",
    "NH": "New Hampshire",
    "NJ": "New Jersey",
    "NM": "New Mexico",
    "NY": "New York",
    "NC": "North Carolina",
    "ND": "North Dakota",
    "MP": "Northern Mariana Islands",
    "OH": "Ohio",
    "OK": "Oklahoma",
    "OR": "Oregon",
    "PW": "Palau",
    "PA": "Pennsylvania",
    "PR": "Puerto Rico",
    "RI": "Rhode Island",
    "SC": "South Carolina",
    "SD": "South Dakota",
    "TN": "Tennessee",
    "TX": "Texas",
    "UT": "Utah",
    "VT": "Vermont",
    "VI": "Virgin Islands",
    "VA": "Virginia",
    "WA": "Washington",
    "WV": "West Virginia",
    "WI": "Wisconsin",
    "WY": "Wyoming"
  }
  json = requests.get('https://covidtracking.com/api/v1/states/current.json')
  json = json.json()
  return render_template('states.html', json=json, states=states)
  
app.run(host='0.0.0.0', port=8080)