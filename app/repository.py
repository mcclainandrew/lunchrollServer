from app import app
from flask import g;
import sqlite3
import random


###################
# User Repository #
###################
def create_user(username, password, email):
    existing_user = query_db("SELECT * FROM Users WHERE username = (?)", [username], one=True)
    if existing_user is not None:
        errorReport = dict(success=False, error="username already exists")
        return errorReport

    existing_email = query_db("SELECT * FROM Users WHERE email = (?)", [email], one=True)
    if existing_email is not None:
        errorReport = dict(success=False, error="email already exists")
        return errorReport

    query_db("INSERT into Users (username, password, email) VALUES (?, ?, ?)", [username, password, email],
             one=True)
    cur = query_db("SELECT userId FROM Users WHERE username = (?)", [username], one=True)
    if cur is None:
        errorReport = dict(success=False, error="user was not successfully saved")
        return errorReport

    successReport = dict(success=True, userId=cur['userId'])
    return successReport;


def update_user(userId, username, password, email):
    user = query_db("SELECT * FROM Users WHERE userId = (?)", [userId], one=True)
    if user is None:
        errorReport = dict(success=False, error="username does not exist")
        return errorReport

    existing_email = query_db("SELECT * FROM Users WHERE email = (?)", [email], one=True)
    if existing_email is not None:
        errorReport = dict(success=False, error="email already exists")
        return errorReport

    query_db("UPDATE Users SET password=(?), email=(?) WHERE userId=(?)", [password, email, userId])
    successReport = dict(success=True, userId=userId)
    return successReport;


def get_user(userId):
    cur = query_db("SELECT username, email FROM Users WHERE userId = (?)", [userId], one=True)
    if cur is None:
        operationReport = dict(success=False, error="could not find userId in the table")
    else:
        operationReport = dict(success=True, username=cur['username'], email=cur['email'])
    return operationReport


def update_preferences(**data_dict):
    userId = data_dict['userId']
    check_user_existence(userId)
    asian = data_dict['asian']
    american = data_dict['american']
    italian = data_dict['italian']
    mexican = data_dict['mexican']
    indian = data_dict['indian']
    greek = data_dict['greek']
    cur = query_db("SELECT * FROM Preferences WHERE UserId = (?)", [userId])

    if cur is None:
        genrePreferenceId = query_db(
            "INSERT INTO GenrePreferences (asian, american, italian, mexican, indian, greek)"
            "VALUES (?, ?, ?, ?, ?, ?)",
            [asian, american, italian, mexican, indian, greek], insert=True)
        if genrePreferenceId == 0 or genrePreferenceId is None:
            operationReport = dict(success=False, Error="unable to insert values into genrePreference table")
            return operationReport

        preferenceId = query_db("INSERT INTO Preferences (userId, genrePreferenceId) VALUES (?, ?)",
                                [data_dict['userId'], genrePreferenceId], insert=True)
        if preferenceId == 0 or preferenceId is None:
            operationReport = dict(success=False, Error="unable to insert values into preference table")
            return operationReport

        operationReport = dict(success=True)
    else:
        genrePreferenceId = cur['genrePreferenceId']
        cur = query_db("SELECT * FROM GenrePreferences WHERE genrePreferenceId = (?)", [genrePreferenceId])
        if cur is None:
            operationReport = dict(success=False,
                                   Error="incorrect genrePreferenceId set in preference table, blame it on Andrew")
            return operationReport

        query_db(
            "UPDATE GenrePreferences SET asian=(?), american=(?), italian=(?), mexican=(?), indian=(?), greek=(?)"
            "WHERE genrePreferenceId = (?)",
            [asian, american, italian, mexican, indian, greek, genrePreferenceId])

        operationReport = dict(success=True)
    return operationReport


def get_preferences(userId):
    check_user_existence(userId)
    cur = query_db("SELECT * FROM Preferences WHERE UserId = (?)", userId)
    if cur is None:
        operationReport = dict(success=False, Error="unable to find preference entry for user")
        return operationReport
    else:
        genrePreferenceId = cur['genrePreferenceId']
        cur = query_db("SELECT * FROM GenrePreferences WHERE genrePreferenceId=(?)", [genrePreferenceId])
        if cur is None:
            operationReport = dict(success=False,
                                   Error="incorrect genrePreferenceId set in preference table, blame it on Andrew")
        else:
            operationReport = dict(success=True, asian=cur['asian'], american=cur['american'], italian=cur['italian'],
                                   mexican=cur['mexican'], indian=cur['indian'], greek=cur['greek'])
    return operationReport


def add_friend(userId, friend_userId):
    check_user_existence(userId + "," + friend_userId)
    cur = query_db("SELECT * FROM Friends WHERE UserId = (?) AND FriendId = (?)", [userId, friend_userId])
    if cur is not None:
        operationReport = dict(success=False, Error="user already has this friend")
    else:
        query_db("INSERT INTO Friends (userId, friendId) VALUES (?, ?)", [userId, friend_userId])
        operationReport = dict(success=True)

    return operationReport


def remove_friend(userId, friend_userId):
    cur = query_db("SELECT * FROM Friends WHERE UserId = (?) AND FriendId = (?)", [userId, friend_userId])
    if cur is None:
        operationReport = dict(success=False, Error="user does not have 2nd user as friend")
    else:
        query_db("DELETE FROM Friends WHERE userId=(?) AND friendId=(?)", [userId, friend_userId])
        operationReport = dict(success=True)
    return operationReport


def get_user_friends(userId):
    cur = query_db("SELECT friendId FROM Friends WHERE UserId=(?)", [userId], one=False)
    operationReport = [dict(friendId=row[1]) for row in cur]
    return operationReport


def login(**data_dict):
    password = data_dict['password']
    if 'username' in data_dict:
        username = data_dict['username']
        cur = query_db("SELECT * FROM Users WHERE username=(?)", [username])
    elif 'email' in data_dict:
        email = data_dict['email']
        cur = query_db("SELECT * FROM Users WHERE email=(?)", [email])
    else:
        operationReport = dict(success=False, Error="no username or password")
        return operationReport

    if cur is None:
        operationReport = dict(success=False, Error="unable to find user")
        return operationReport

    if password != cur['password']:
        operationReport = dict(success=False, Error="incorrect password")
        return operationReport

    return dict(success=True, userId=cur['userId'])


####################
# Group Repository #
####################
def create_group(userId, name, users):
    result = check_user_existence(users)
    if result['success'] != True:
        return result

    cur = query_db("SELECT groupId FROM Groups WHERE name=(?) and userId=(?)", [name, userId], one=True)
    if cur is not None:
        operationReport = dict(success=False, error="group already exists for user")
        return operationReport
    query_db("INSERT INTO Groups (userId, name, users) VALUES (?, ?, ?)", [userId, name, users], one=True)
    cur = query_db("SELECT groupId FROM Groups WHERE name=(?) and userId=(?)", [name, userId], one=True)
    operationReport = dict(success=True, groupId=cur['groupId'])
    return operationReport


def update_group(groupId, name, users):
    result = check_user_existence(users)
    if result['success'] != True:
        return result
    cur = query_db("SELECT * FROM Groups WHERE groupId=(?)", [groupId], one=True)
    if cur is None:
        operationReport = dict(success=False, error="could not find group")
    else:
        query_db("UPDATE Groups SET name=(?),users=(?) WHERE groupId=(?)",
                 [name, users, groupId], one=True)
        operationReport = dict(success=True)
    return operationReport


def get_group(groupId):
    cur = query_db("SELECT * FROM Groups WHERE groupId = (?)", [groupId], one=True)
    if cur is None:
        operationReport = dict(success=False, error="could not find group")
    else:
        operationReport = dict(success=True, groupId=cur['groupId'], userId=cur['userId'], name=cur['name'],
                               users=cur['users'])
    return operationReport


def get_groups(userId):
    cur = query_db("SELECT groupId, name, users FROM Groups WHERE userId = ?", [userId], one=False)
    if cur is None:
        operationReport = dict(success=False, error="could not find any groups")
    else:
        operationReport = [dict(success=True, groupId=row[0], name=row[1], users=row[2]) for row in cur]
    return operationReport


def delete_group(groupId, password):
    cur = query_db("SElECT userId FROM Groups WHERE groupId=(?)", [groupId], one=True)
    userId = cur['userId']
    cur = query_db("SELECT password FROM Users WHERE userId=(?)", [userId], one=True)
    if cur is None:
        return dict(success=False, error="could not find user associated with group")
    if cur['password'] != password:
        operationReport = dict(success=False, error="incorrect password", attempted=password, actual=cur['password'])
        return operationReport
    query_db("DELETE FROM Groups WHERE groupId=(?)", [groupId], one=True)
    operationReport = dict(success=True)
    return operationReport


##############################
# Admin Repository Functions #
##############################

def get_all_users():
    cur = query_db("SELECT * FROM Users", one=False)
    entries = [dict(userId=row[0], username=row[1], password=row[2], email=row[3]) for row in cur]
    return entries


def get_all_groups():
    cur = query_db("SELECT * FROM Groups", one=False)
    entries = [dict(groupId=row[0], userId=row[1], name=row[2], users=row[3]) for row in cur]
    return entries


############################
# Aux Repository Functions #
############################
def check_user_existence(users):
    user_list = users.split(',')
    for user in user_list:
        cur = query_db("SELECT * FROM Users WHERE userId = (?)", [user])
        if cur is None:
            return dict(success=False, Error="could not find user", userId=user)
    return dict(success=True)


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_db()
        db.row_factory = sqlite3.Row
    return db


def connect_db():
    return sqlite3.connect('/var/www/lunchroll/app/database/lunchroll.db')


def query_db(query, args=(), one=True, insert=False):
    db = get_db()
    cur = db.execute(query, args)
    db.commit()
    if insert is True:
        rv = cur.lastrowid
        one = False
    else:
        rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
