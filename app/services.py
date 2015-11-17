from app import app
from repository import *
from flask import Blueprint, request, session, abort, jsonify, g
import json
import random


user = Blueprint('user', __name__)
group = Blueprint('group', __name__)
admin = Blueprint('admin', __name__)

app.debug = True

#Start Database Calls

@user.route('/user/updateUser', methods = ['POST'])
def new_user():
	data_dict = request.get_json()
	userId = data_dict['userId']
	username = data_dict['username']
	password = data_dict['password']
	email = data_dict['email']
	
	if userId == '0':
		entries = createUser(username, password, email)
	else:
		entries = updateUser(userId, username, password, email)
	
	return jsonify(data=entries)

@user.route('/user/getUser', methods = ['POST'])
def getUserData():
	data_dict = request.get_json()
	userId = data_dict['userId']
	
	entries = getUser(userId)
	return jsonify(data=entries)   

@group.route('/group/updateGroup', methods = ['POST'])
def updateGroup():    
	db = get_db()
	data_dict = request.get_json()
	groupId = data_dict['groupId']
	userId = data_dict['userId']
	name = data_dict['name']
	users = data_dict['users']

	if groupId == '0':
		db.execute("INSERT INTO Groups (userId, name, users) VALUES (?, ?, ?)", [userId, name, users])
		db.commit()
	cur = db.execute("SELECT groupId, userId, name, users FROM Groups WHERE name = (?)", [name])
	db.commit()
	entries = [dict(groupId=row[0], userId=row[1], name=row[2], users=row[3]) for row in cur.fetchall()]
	return jsonify(data=entries)

@user.route('/user/getGroups', methods = ['POST'])
def getGroups():
	db = get_db()
	data_dict = request.get_json()
	userId = data_dict['userId']
	cur = db.execute("SELECT groupId, name FROM Groups WHERE userId = ?", [userId])
	db.commit()
	entries = [dict(groupId=row[0], name=row[1]) for row in cur.fetchall()]
	return jsonify(data = entries)

@group.route('/group/getData', methods = ['POST'])
def getGroupData():
	db = get_db()
	data_dict = request.get_json()
	groupId = data_dict['groupId']
	cur = db.execute("SELECT userId, name, users FROM Groups WHERE groupId = (?)", [groupId])
	db.commit()
	entries = [dict(groupId=groupId, userId=row[0], name=row[1], users=row[2]) for row in cur.fetchall()]
	return jsonify(data=entries)

@user.route('/user/getPreferences', methods = ['POST'])
def getPreferences():
	db = get_db()
	data_dict = request.get_json()
	userId = data_dict['userId']
	cur = db.execute("SELECT genrePreferenceId FROM Preferences WHERE userId = ?", [userId])
	db.commit()
	(rv,) = cur.fetchone()
	genrePreferenceId = rv
	cur = db.execute("SELECT asian, american, italian, mexican,indian, greek FROM genrePreferences WHERE genrePreferenceId = ?", [genrePreferenceId])
	entries = [dict(asian=row[0], american=row[1], italian=row[2], mexican=row[3], indian=row[4], greek=row[5]) for row in cur.fetchall()]
	return jsonify(data=entries)
	

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
#todo

@admin.route('/admin/getUsers', methods = ['POST'])
def getUsers():
	db = get_db()
	cur = db.execute("SELECT * FROM Users")
	db.commit()
	entries = [dict(userId=row[0],username=row[1],password=row[2],email=row[3]) for row in cur.fetchall()]
	return jsonify(data=entries)

@user.route('/user/login', methods = ['POST'])
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


#End Database Calls
