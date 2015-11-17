from app import app
from flask import g;
import sqlite3
import random
from passlib.hash import md5_crypt


def createUser(username, password, email):
	encryptedPass = md5_crypt.encrypt(password)
	existing_user = query_db("SELECT * FROM Users WHERE username = (?)", [username], one=True)
	if existing_user is not None:
		errorReport = dict(Success=False, Error="username already exists")
		return errorReport
		
	existing_email = query_db("SELECT * FROM Users WHERE email = (?)", [email], one=True)
	if existing_email is not None:
		errorReport = dict(Success=False, Error="email already exists")
		return errorReport
	
	query_db("INSERT into Users (username, password, email) VALUES (?, ?, ?)", [username, encryptedPass, email], one=True)
	cur = query_db("SELECT userId FROM Users WHERE username = (?)", [username], one=True)
	if cur is None:
		errorReport = dict(Success=False, Error="user was not successfully saved")
		return errorReport
	
	successReport = dict(Success=True, userId=cur['userId'])
	return successReport;

def updateUser(userId, username, password, email):
	encryptedPass = md5_crypt.encrypt(password)
	user = query_db("SELECT * FROM Users WHERE userId = (?)", [userId], one=True)
	if user is None:
		return "Error: user does not exist"
	
	existing_email = query_db("SELECT * FROM Users WHERE email = (?)", [email], one=True)
	if existing_email is not None:
		return "Error: email already exists"	
		
	cur = query_db("UPDATE Users SET password=(?), email=(?) WHERE userId=(?)", [encryptedPass, email, userId])
	
	return userId;
	
def getUser(userId):
	cur = get_db("SELECT username, password, email FROM Users WHERE userId = (?)", [userId], one=True)
	return 
def get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = g.db = connect_db()
		db.row_factory = sqlite3.Row
	return db
    
def connect_db():
	return sqlite3.connect('/var/www/lunchroll/app/database/lunchroll.db')

def query_db(query, args=(), one=False):
	db = get_db()
	cur = db.execute(query, args)
	db.commit()
	rv = cur.fetchall()
	cur.close()
	return (rv[0] if rv else None) if one else rv
