from app import app
from repository import *
from flask import Blueprint, request, session, abort, jsonify, g
import json
import random

user = Blueprint('user', __name__)
group = Blueprint('group', __name__)
admin = Blueprint('admin', __name__)

app.debug = True


#################
# User Services #
#################
@user.route('/user/updateUser', methods=['POST'])
def modify_user_service():
    data_dict = request.get_json()
    userId = data_dict['userId']
    username = data_dict['username']
    password = data_dict['password']
    email = data_dict['email']

    if userId == '0':
        entries = create_user(username, password, email)
    else:
        entries = update_user(userId, username, password, email)

    return jsonify(data=entries)


@user.route('/user/getUser', methods=['POST'])
def get_user_data_service():
    data_dict = request.get_json()
    userId = data_dict['userId']

    entries = get_user(userId)
    return jsonify(data=entries)


@user.route('/user/getGroups', methods=['POST'])
def get_user_groups_service():
    data_dict = request.get_json()
    userId = data_dict['userId']
    entries = get_groups(userId)
    return jsonify(data=entries)


@user.route('/user/getPreferences', methods=['POST'])
def get_preferences_service():
    db = get_db()
    data_dict = request.get_json()
    userId = data_dict['userId']
    cur = db.execute("SELECT genrePreferenceId FROM Preferences WHERE userId = ?", [userId])
    db.commit()
    (rv,) = cur.fetchone()
    genrePreferenceId = rv
    cur = db.execute(
        "SELECT asian, american, italian, mexican, indian, greek FROM genrePreferences WHERE genrePreferenceId = ?",
        [genrePreferenceId])
    entries = [dict(asian=row[0], american=row[1], italian=row[2], mexican=row[3], indian=row[4], greek=row[5]) for row
               in cur.fetchall()]
    return jsonify(data=entries)


@user.route('/user/updatePreferences', methods=['POST'])
def update_preferences_service():
    data_dict = request.get_json()
    userId = data_dict['userId']
    asian = data_dict['asian']
    american = data_dict['american']
    italian = data_dict['italian']
    mexican = data_dict['mexican']
    indian = data_dict['indian']
    greek = data_dict['greek']

    entries = update_preferences(**data_dict)

    return jsonify(data=entries)

@user.route('/user/getPreferences', methods=['POST'])
def get_preferences_service():
    data_dict = request.get_json()
    userId = data_dict['userId']
    entries = get_preferences(userId)
    return jsonify(data=entries)

@user.route('/user/login', methods=['POST'])
def login_service():
    data_dict = request.get_json()
    password = data_dict['password']
    entries = login(**data_dict)
    return jsonify(data=entries)

'''d
def suggest(userId):
	db = get_db()
	totalGenre = 6
	genres = ["mexican", "american", "italian", "asian", "indian", "greek"]
	genreTok = []
	cur = db.execute("SELECT genrePreferenceId FROM Preferences WHERE userId = ?",[userId])
	db.commit()
	(rv,) = cur.fetchone()
	cur = db.execute("SELECT mexican, american, italian, asian, indian, greek FROM GenrePreferences WHERE genrePreferenceId = ? ", rv)
	for i in range(0,totalGenre)
		(rv,) = cur.fetchone()
		genreTok[i] = rv
	totalTokens = sum(int(i) for i in genreTok)
	ran = randomrange(0, totalTokens)
	count = 0
	for i in range(0, totalGenre)
		count += genreTok[i]
		if count <= ran:
			return genres[i]
'''


##################
# Group Services #
##################
@group.route('/group/getGroup', methods=['POST'])
def get_group_data_service():
    data_dict = request.get_json()
    groupId = data_dict['groupId']
    entries = get_group(groupId)
    return jsonify(data=entries)


@group.route('/group/updateGroup', methods=['POST'])
def update_group_service():
    data_dict = request.get_json()
    groupId = data_dict['groupId']
    name = data_dict['name']
    users = data_dict['users']

    if groupId == '0':
        userId = data_dict['userId']
        entries = create_group(userId, name, users)
    else:
        entries = update_group(groupId, name, users)

    return jsonify(data=entries)


@group.route('/group/deleteGroup', methods=['POST'])
def delete_group_service():
    data_dict = request.get_json()
    groupId = data_dict['groupId']
    password = data_dict['password']
    report = delete_group(groupId, password)
    return jsonify(data=report)


########################
# Debug Admin Services #
########################
@admin.route('/admin/getUsers', methods=['POST'])
def get_all_users_service():
    entries = get_all_users()
    return jsonify(data=entries)


@admin.route('/admin/getGroups', methods=['POST'])
def get_all_groups_service():
    entries = get_all_groups()
    return jsonify(data=entries)

# End Database Calls
