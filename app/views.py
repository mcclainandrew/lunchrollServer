from app import app
from flask import render_template
from services import client, user, group, admin

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
###################


#Register client endpoints
app.register_blueprint(client)

#Register user endpoints
app.register_blueprint(user)

#Register group endpoints
app.register_blueprint(group)

#Register admin endpoints
app.register_blueprint(admin)

