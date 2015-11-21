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
        "SELECT asian, american, italian, mexican,indian, greek FROM genrePreferences WHERE genrePreferenceId = ?",
        [genrePreferenceId])
    entries = [dict(asian=row[0], american=row[1], italian=row[2], mexican=row[3], indian=row[4], greek=row[5]) for row
               in cur.fetchall()]
    return jsonify(data=entries)


"""
@user.route('/user/updatePreferences', methods = ['POST'])
def updatePreferences():
	db = get_db()
	data_dict = request.get_json()
	userId = data_dict['userId'] + ""
	asian = data_dict['asian'] + ""
	american = data_dict['american'] + ""
	italian = data_dict['italian'] + ""
	mexican = data_dict['mexican'] + ""
	indian = data_dict['indian'] + ""
	greek = data_dict['greek'] + ""
	preferenceId = data_dict['preferenceId'] + ""
	if preferenceId == '0':
		c = db.cursor()
		c.execute("INSERT INTO GenrePreferences (asian, american, italian, mexican, indian, greek) VALUES (?, ?, ?, ?, ?, ?)", [asian, american, italian, mexican, indian, greek])
		db.commit()
		genrePreferenceId = c.lastrowid
		c.execute("INSERT INTO Preferences (userId, genrePreferenceId) VALUES (?, ?)", [userId, genrePreferenceId])
		db.commit()
		preferenceId = c.lastrowid
		entries = dict(preferenceId = preferenceId)
		return jsonify(data = entries)
	else:
		#need to fix this
		#user can't update settings yet
		db.execute("SELECT GenrePrefernceId FROM Preferences WHERE userId = ?", [userId])
		db.commit()
		db.execute("UPDATE GenrePreferences SET (asian=?, american=?, italian=?, mexican=?, indian=?, greek=?) WHERE genrePreferenceId = ?", [asian,american,italian,mexican,indian,greek,groupPreferencesId])
		db.commit()
		return None
"""


##################
# Group Services #
##################
@group.route('/group/getData', methods=['POST'])
def get_group_data_service():
    data_dict = request.get_json()
    groupId = data_dict['groupId']
    entries = get_group(groupId)
    return jsonify(data=entries)


@group.route('/group/updateGroup', methods=['POST'])
def update_group_service():
    data_dict = request.get_json()
    groupId = data_dict['groupId']
    userId = data_dict['userId']
    name = data_dict['name']
    users = data_dict['users']

    if groupId == '0':
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


@admin.route('/admin/getUsers', methods=['POST'])
def get_all_users_service():
    entries = get_all_users()
    return jsonify(data=entries)


@admin.route('/admin/getGroups', methods=['POST'])
def get_all_groups_service():
    entries = get_all_groups()
    return jsonify(data=entries)


@user.route('/user/login', methods=['POST'])
def login():
    db = get_db()
    data_dict = request.get_json()
    email = data_dict['email'] + ""
    password = data_dict['password'] + ""
    encryptedPass = md5_crypt.encrypt(password)

    cur = db.execute("SELECT * FROM Users WHERE email = ? AND password = ?", [email, password])
    db.commit()
    entries = [dict(userId=row[0], username=row[1]) for row in cur.fetchall()]
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


# End Database Calls
