from app import app
from Flask import g;
import sqlite3
import random
from passlib.hash import md5_crypt


def createUser(username, password, email):
	db = get_db()
	encryptedPass = md5_crypt.encrypt(password)
	db.execute("INSERT into Users (username, password, email) VALUES (?, ?, ?)", [username, encryptedPass, email])
	db.commit()
	cur = db.execute("SELECT userId, username, password, email FROM Users WHERE username = (?)", [email])
	db.commit()
	entries = [dict(userID=row[0], username=row[1], password=row[2], email=row[3]) for row in cur.fetchall()]
	return jsonify(data=entries)

def updateUser(userId, username, password, email):
	db = get_db()
	encryptPass = md5_crypt.encrypt(password)
	db.execute("UPDATE Users SET username=(?), password=(?), email=(?) WHERE userId = (?)", [username, encryptedPass, email, userId])
	db.commit()
	cur = db.execute("SELECT userId, username, password, email FROM Users WHERE username = (?)")
	db.commit()
	entries = [dict(userID=row[0], username=row[1], password=row[2], email=row[3]) for row in cur.fetchall()]
	return jsonify(data=entries)

	
def get_db():
	if not hasattr(g, 'db'):
		g.db = connect_db()
		g.db.row_factory = sqlite3.Row
	return g.db
    
def connect_db():
	return sqlite3.connect('/var/www/lunchroll/app/database/lunchroll.db')
