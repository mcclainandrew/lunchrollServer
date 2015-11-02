from app import app
from flask import request
from flask import Response
import json
import requests
from flask import render_template
placesApiKey = "AIzaSyD7Dxn7cpZ2q70mDr3Ia5stmPrcydNgh0w"
nearbySearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
textSearch = "https://maps.googleapis.com/maps/api/place/textsearch/json"
headers = {'Content-Type':'application/json'}
app.debug = 1

@app.route('/')
@app.route('/index')
@app.route('/help')
@app.route('/help/<name>')
def help(name=None):
    return render_template("apihelp.html", name=name) 

@app.route('/help/client/nearbyAny')
@app.route('/help/client/nearbyAny/<name>')
def helpNearbyAny(name=None):
    return render_template("nearbyAny.html", name=name)

@app.route('/help/client/nearbySpecific')
@app.route('/help/client/nearbySpecific/<name>')
def helpNearbySpecific(name=None):
    return render_template("nearbySpecific.html", name=name)

@app.route('/help/client/nearbySuggested')
@app.route('/help/client/nearbySuggested/<name>')
def helpNearbySuggested(name=None):
    return render_template("nearbySuggested.html", name=name)

@app.route('/client/nearbySpecific', methods=['POST'])
def searchSpecific():
    data_dict = request.get_json()
    latitude = data_dict['latitude']
    longitude = data_dict['longitude']
    location = latitude + ',' + longitude
    genre = data_dict['genre']
    genre = genre + '+food'
    payload = {'location': location, 'radius': 5000, 'types': "food|restaurant", 'query': genre, 'key': placesApiKey}
    r = requests.post(textSearch, params=payload, headers=headers);
    return Response(r.text, content_type='application/json')
    
@app.route('/client/nearbySuggested', methods=['POST'])
       
@app.route('/client/nearbyAny', methods=['POST'])
def searchNearby():
    data_dict = request.get_json()

    latitude = data_dict['latitude']
    longitude = data_dict['longitude']
    location = latitude + "," + longitude 
    payload = {'location': location, 'radius': 5000, 'types': 'food', 'key': placesApiKey}

    r = requests.post(nearbySearch, params=payload, headers=headers)
    return Response(r.text, content_type="application/json")

