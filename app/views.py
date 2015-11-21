from app import app
from flask import render_template, g
from services import user, group, admin
from clientServices import client


#Register client endpoints
app.register_blueprint(client)

#Register user endpoints
app.register_blueprint(user)

#Register group endpoints
app.register_blueprint(group)

#Register admin endpoints
app.register_blueprint(admin)


####################
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
    return render_template("client/nearbyAny.html", name=name)

@app.route('/help/client/nearbySpecific')
@app.route('/help/client/nearbySpecific/<name>')
def helpNearbySpecific(name=None):
    return render_template("client/nearbySpecific.html", name=name)

@app.route('/help/client/nearbySuggested')
@app.route('/help/client/nearbySuggested/<name>')
def helpNearbySuggested(name=None):
    return render_template("client/nearbySuggested.html", name=name)
	
@app.route('/help/user/updateUser')
@app.route('/help/user/updateUser/<name>')
def helpUpdateUser(name=None):
    return render_template("user/updateUser.html", name=name)

@app.route('/help/user/getUser')
@app.route('/help/user/getUser/<name>')
def helpGetUser(name=None):
    return render_template("user/getUser.html", name=name)

@app.route('/help/user/getGroups')
@app.route('/help/user/getGroups/<name>')
def helpGetUserGroups(name=None):
    return render_template("user/getGroups.html", name=name)

#End Api Help Page
###################

@app.teardown_appcontext
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

