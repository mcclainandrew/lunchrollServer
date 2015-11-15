from app import app
from flask import request, Response, session, abort, jsonify, render_template, g
import json
import requests
import sqlite3
import random
from passlib.hash import md5_crypt

placesApiKey = "AIzaSyD7Dxn7cpZ2q70mDr3Ia5stmPrcydNgh0w"
nearbySearch = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
textSearch = "https://maps.googleapis.com/maps/api/place/textsearch/json"
headers = {'Content-Type':'application/json'}
app.debug = True

#Start Api Help Page

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

#End Api Help Page

#Start Client Calls

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

#End Client Calls

#Start Database Calls

@app.route('/user/updateUser', methods = ['POST'])
def new_user():
    db = get_db()
    data_dict = request.get_json()
    userID = data_dict['userID'] + ""
    username = data_dict['username'] + ""
    password = data_dict['password'] + ""
    email = data_dict['email'] + ""
    
    if userID == '0':
	encryptedPass = md5_crypt.encrypt(password)
        db.execute("insert into Users (username, password, email) values (?, ?, ?)", [username, password, email])
        db.commit()
    cur = db.execute("SELECT userID, username, password, email FROM Users WHERE email = (?)", [email])
    db.commit()
    entries = [dict(userID=row[0], username=row[1], password=row[2], email=row[3]) for row in cur.fetchall()]

    return jsonify(data=entries[-1])

@app.route('/group/updateGroup', methods = ['POST'])
def updateGroup():    
    db = get_db()
    data_dict = request.get_json()
    groupID = data_dict['groupID'] + ""
    userID = data_dict['userID'] + ""
    name = data_dict['name'] + ""
    users = data_dict['users'] + ""

    if groupID == '0':
        db.execute("INSERT INTO Groups (userID, name, users) VALUES (?, ?, ?)", [userID, name, users])
        db.commit()
    cur = db.execute("SELECT groupID, userID, name, users FROM Groups WHERE name = (?)", [name])
    db.commit()
    entries = [dict(groupID=row[0], userID=row[1], name=row[2], users=row[3]) for row in cur.fetchall()]
    return jsonify(data=entries)

@app.route('/user/getData', methods = ['POST'])
def getUserData():
    db = get_db()
    data_dict = request.get_json()
    userID = data_dict['userID']
    cur = db.execute("SELECT username, password, email FROM Users WHERE userID = (?)", [userID])
    db.commit()
    entries = [dict(userID=userID, username=row[0], password=row[1], email=row[2]) for row in cur.fetchall()]
    return jsonify(data=entries)   

@app.route('/user/getGroups', methods = ['POST'])
def getGroups():
    db = get_db()
    data_dict = request.get_json()
    userID = data_dict['userID']
    cur = db.execute("SELECT groupID, name FROM Groups WHERE userID = ?", [userID])
    db.commit()
    entries = [dict(groupID=row[0], name=row[1]) for row in cur.fetchall()]
    return jsonify(data = entries)

@app.route('/group/getData', methods = ['POST'])
def getGroupData():
    db = get_db()
    data_dict = request.get_json()
    groupID = data_dict['groupID']
    cur = db.execute("SELECT userID, name, users FROM Groups WHERE groupID = (?)", [groupID])
    db.commit()
    entries = [dict(groupID=groupID, userID=row[0], name=row[1], users=row[2]) for row in cur.fetchall()]
    return jsonify(data=entries)

@app.route('/user/getPreferences', methods = ['POST'])
def getPreferences():
    db = get_db()
    data_dict = request.get_json()
    userID = data_dict['userID']
    cur = db.execute("SELECT genrePreferenceID FROM Preferences WHERE userID = ?", [userID])
    db.commit()
    (rv,) = cur.fetchone()
    genrePreferenceID = rv
    cur = db.execute("SELECT asian, american, italian, mexican,indian, greek FROM genrePreferences WHERE genrePreferenceID = ?", [genrePreferenceID])
    entries = [dict(asian=row[0], american=row[1], italian=row[2], mexican=row[3], indian=row[4], greek=row[5]) for row in cur.fetchall()]
    return jsonify(data=entries)
    

@app.route('/user/updatePreferences', methods = ['POST'])
def updatePreferences():
    db = get_db()
    data_dict = request.get_json()
    userID = data_dict['userID'] + ""
    asian = data_dict['asian'] + ""
    american = data_dict['american'] + ""
    italian = data_dict['italian'] + ""
    mexican = data_dict['mexican'] + ""
    indian = data_dict['indian'] + ""
    greek = data_dict['greek'] + ""
    preferenceID = data_dict['preferenceID'] + ""
    if preferenceID == '0':
        c = db.cursor()
        c.execute("INSERT INTO GenrePreferences (asian, american, italian, mexican, indian, greek) VALUES (?, ?, ?, ?, ?, ?)", [asian, american, italian, mexican, indian, greek])
        db.commit()
        genrePreferenceID = c.lastrowid
        c.execute("INSERT INTO Preferences (userID, genrePreferenceID) VALUES (?, ?)", [userID, genrePreferenceID])
        db.commit()
        preferenceID = c.lastrowid
        entries = dict(preferenceID = preferenceID)
        return jsonify(data = entries)
    else:
        #need to fix this
        #user can't update settings yet
        db.execute("SELECT GenrePrefernceID FROM Preferences WHERE userID = ?", [userID])
        db.commit()
        db.execute("UPDATE GenrePreferences SET (asian=?, american=?, italian=?, mexican=?, indian=?, greek=?) WHERE genrePreferenceID = ?", [asian,american,italian,mexican,indian,greek,groupPreferencesID])
        db.commit()
        return None
#todo

@app.route('/admin/getUsers', methods = ['POST'])
def getUsers():
    db = get_db()
    cur = db.execute("SELECT * FROM Users")
    db.commit()
    entries = [dict(userID=row[0],username=row[1],password=row[2],email=row[3]) for row in cur.fetchall()]
    return jsonify(data=entries)

@app.route('/user/login', methods = ['POST'])
def login():
    db = get_db()
    data_dict = request.get_json()
    email = data_dict['email'] + ""
    password = data_dict['password'] + ""
    encryptedPass = md5_crypt.encrypt(password)

    cur = db.execute("SELECT * FROM Users WHERE email = ? AND password = ?", [email, password])
    db.commit()
    entries = [dict(userID=row[0], username=row[1]) for row in cur.fetchall()]
    return jsonify(data=entries)         
'''d
def suggest(userID):
    db = get_db()
    totalGenre = 6
    genres = ["mexican", "american", "italian", "asian", "indian", "greek"]
    genreTok = []
    cur = db.execute("SELECT genrePreferenceID FROM Preferences WHERE userID = ?",[userID])
    db.commit()
    (rv,) = cur.fetchone()
    cur = db.execute("SELECT mexican, american, italian, asian, indian, greek FROM GenrePreferences WHERE genrePreferenceID = ? ", rv)
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
@app.teardown_appcontext
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def get_db():
    if not hasattr(g, 'db'):
        g.db = connect_db()
        g.db.row_factory = sqlite3.Row
    return g.db
    
def connect_db():
    return sqlite3.connect('/var/www/lunchroll/app/database/lunchroll.db')

#End Database Calls

