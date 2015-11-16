from app import app
from flask import g;
import sqlite3
import random
from passlib.hash import md5_crypt


def createUser(username, password, email):
	encryptedPass = md5_crypt.encrypt(password)
	user = query_db("SELECT * FROM Users WHERE username = (?)", [username], one=True)
	if user is not None:
		return -1
	
	query_db("INSERT into Users (username, password, email) VALUES (?, ?, ?)", [username, encryptedPass, email], one=True)
	cur = query_db("SELECT * FROM Users WHERE username = (?)", [username])
	if cur is None:
		return -2;
	
	return cur['userId'];

def updateUser(userId, username, password, email):
	db = get_db()
	encryptPass = md5_crypt.encrypt(password)
	db.execute("UPDATE Users SET username=(?), password=(?), email=(?) WHERE userId = (?)", [username, encryptedPass, email, userId])
	db.commit()
	cur = db.execute("SELECT userId, username, password, email FROM Users WHERE username = (?)")
	db.commit()
	entries = [dict(userID=row[0], username=row[1], password=row[2], email=row[3]) for row in cur.fetchall()]
	return entries

	
def get_db():
	db = getattr(g, 'db', None)
	if db is None:
		db = g.db = connect_db()
		db.row_factory = sqlite3.Row
	return db
    
def connect_db():
	return sqlite3.connect('/var/www/lunchroll/app/database/lunchroll.db')

def make_dicts(cursor, row):
	return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))

def query_db(query, args=(), one=False):
	cur = get_db().execute(query, args)
	rv = cur.fetchall()
	cur.commit()
	cur.close()
	return (rv[0] if rv else None) if one else rv