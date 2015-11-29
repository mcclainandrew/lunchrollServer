from app import app
import repository
from flask import Blueprint, request
from repository import search, user_suggest, group_suggest



#Start Client Calls
client = Blueprint('client', __name__)

@client.route('/client/nearbyAny', methods=['POST'])
@client.route('/client/nearbySpecific', methods=['POST'])
@client.route('/client/search', methods=['POST'])
def search_specific_service():
    data_dict = request.get_json()
    latitude = data_dict['latitude']
    longitude = data_dict['longitude']
    location = latitude + ',' + longitude
    genre = None
    if 'genre' in data_dict:
        genre = data_dict['genre']
    return search(location, genre)


@client.route('/client/suggest', methods=['POST'])
def search_suggested_service():
    data_dict = request.get_json()
    latitude = data_dict['latitude']
    longitude = data_dict['longitude']
    location = latitude + ',' + longitude
    if 'userId' in data_dict:
        operationReport = user_suggest(data_dict['userId'])
    elif 'groupId' in data_dict:
        operationReport = group_suggest(data_dict['groupId'])
    else:
        return dict(success=False, Error="no user or group ID in json")

    if operationReport['success'] is not True:
        return operationReport

    return search(location, operationReport['genre'])

#End Client Calls
