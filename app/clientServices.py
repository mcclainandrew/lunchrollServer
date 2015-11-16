from app import app
import repository
from flask import Blueprint, Response, jsonify
import requests

#Start Client Calls
client = Blueprint('client', __name__)

@client.route('/client/nearbySpecific', methods=['POST'])
def searchSpecific():
    data_dict = request.get_json()
    latitude = data_dict['latitude']
    longitude = data_dict['longitude']
    location = latitude + ',' + longitude
    genre = data_dict['genre']
    genre = genre + '+food'
    payload = {'location': location, 'radius': 5000, 'types': "food|restaurant", 'query': genre, 'key': placesApiKey}
    r = requests.post(textSearch, params=payload, headers=headers)
    return Response(r.text, content_type='application/json')

@client.route('/client/nearbySuggested', methods=['POST'])


@client.route('/client/nearbyAny', methods=['POST'])
def searchNearby():
    data_dict = request.get_json()

    latitude = data_dict['latitude']
    longitude = data_dict['longitude']
    location = latitude + "," + longitude
    payload = {'location': location, 'radius': 5000, 'types': 'food', 'key': placesApiKey}
    r = requests.post(nearbySearch, params=payload, headers=headers)
    return Response(r.text, content_type="application/json")

#End Client Calls
