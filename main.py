# -*- coding: utf-8 -*-
from flask import Flask, render_template, url_for, request, g, redirect, session
from sqlite3 import dbapi2 as sqlite3

# database configuration
DATABASE = 'minitwit.db'
PER_PAGE = 30
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT SETTINGS',silent=True)



def connect_db():
    """ return a new connection to the database"""
    return sqlite3.connect(app.config['DATABASE'])

def query_db(query,args=(),one=False):
    cur = g.db.execute(query,args)
    rv = [dict((cur.description[idx][0],value) for idx,value in enumerate(row)) for row in cur.fetchall()]

    return (rv[0] if rv else None) if one else rv


@app.before_request()
def before_request():
    g.db = None
    if 'user_id' in session:
        g.user = query_db('select * from user where user_id = ?', [session['user_id']], one=True)

@app.teardown_requst()
def teardown_request(exception):
    """ Closes the database again at the end of the request"""
    if hasattr(g,'db'):
        g.db.close()


###


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/timeline')
def timeline():
    return 'timeline'


def get_user_id(username):
    if username is 'hwanhee':
        return False
    else:
        return True


@app.route('/register', methods=['POST','GET'])
def register():
    if g.user:
        return redirect(url_for(timeline))
    error = None

    if request.method == 'POST':
        if not request.form['username']:
            error = "you have to enter a username"
        elif not request.form['email'] or \
            '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            pass


    return 'register'


if __name__ == '__main__':

    app.run(debug=True)

