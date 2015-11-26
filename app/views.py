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

@app.route('/help/client/suggest')
@app.route('/help/client/suggest/<name>')
def helpClientSuggest(name=None):
    return render_template("client/suggest.html", name=name)

@app.route('/help/client/search')
@app.route('/help/client/search/<name>')
def helpClientSearch(name=None):
    return render_template("client/search.html", name=name)

@app.route('/help/user/updateUser')
@app.route('/help/user/updateUser/<name>')
def helpUserUpdateUser(name=None):
    return render_template("user/updateUser.html", name=name)

@app.route('/help/user/getUser')
@app.route('/help/user/getUser/<name>')
def helpUserGetUser(name=None):
    return render_template("user/getUser.html", name=name)

@app.route('/help/user/getGroups')
@app.route('/help/user/getGroups/<name>')
def helpUserGetGroups(name=None):
    return render_template("user/getGroups.html", name=name)

@app.route('/help/user/getPreferences')
@app.route('/help/user/getPreferences/<name>')
def helpUserGetPreferences(name=None):
    return render_template("user/getPreferences.html", name=name)

@app.route('/help/user/updatePreferences')
@app.route('/help/user/updatePreferences/<name>')
def helpUserUpdatePreferences(name=None):
    return render_template("user/updatePreferences.html", name=name)

@app.route('/help/user/getFriends')
@app.route('/help/user/getFriends/<name>')
def helpUserGetFriends(name=None):
    return render_template("user/getFriends.html", name=name)

@app.route('/help/user/addFriend')
@app.route('/help/user/addFriend/<name>')
def helpUserAddFriend(name=None):
    return render_template("user/addFriend.html", name=name)

@app.route('/help/user/removeFriend')
@app.route('/help/user/removeFriend/<name>')
def helpUserRemoveFriend(name=None):
    return render_template("user/removeFriend.html", name=name)

@app.route('/help/group/getGroup')
@app.route('/help/group/getGroup/<name>')
def helpGroupGetGroup(name=None):
    return render_template("group/getGroup.html", name=name)

@app.route('/help/group/updateGroup')
@app.route('/help/group/updateGroup/<name>')
def helpGroupUpdateGroup(name=None):
    return render_template("group/updateGroup.html", name=name)

@app.route('/help/group/deleteGroup')
@app.route('/help/group/deleteGroup/<name>')
def helpGroupDeleteGroup(name=None):
    return render_template("group/deleteGroup.html", name=name)

#End Api Help Page
###################

@app.teardown_appcontext
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

