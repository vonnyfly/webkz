# -*- coding: utf-8 -*-
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'webkz.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('WEBKZ_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return redirect(url_for('instances'))

@app.route('/instances')
def instances():
    # db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    # instances = cur.fetchall()
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''
    fake data here, pls replace it.
    '''
    instances = [
        {'name': 'host1', 'status': 'running', 'ip': '127.0.0.1'},
        {'name': 'host2', 'status': 'running', 'ip': '127.0.0.2'},
        {'name': 'host3', 'status': 'running', 'ip': '127.0.0.3'},
        {'name': 'host4', 'status': 'running', 'ip': '127.0.0.4'},
        {'name': 'host5', 'status': 'running', 'ip': '127.0.0.5'},
        {'name': 'host6', 'status': 'running', 'ip': '127.0.0.6'},
        {'name': 'host7', 'status': 'running', 'ip': '127.0.0.7'},
        {'name': 'host8', 'status': 'running', 'ip': '127.0.0.8'},
        {'name': 'host9', 'status': 'running', 'ip': '127.0.0.9'},
        {'name': 'host10', 'status': 'running', 'ip': '127.0.0.10'},
        ]
    print instances
    return render_template('instances.html', instances=instances)

@app.route('/instances/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    # db = get_db()
    # db.execute('insert into entries (title, text) values (?, ?)',
    #            [request.form['title'], request.form['text']])
    # db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('instances'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('instances'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))

@app.route('/servers')
def servers():
    # db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    # instances = cur.fetchall()
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    '''
    fake data here, pls replace it.
    '''
    servers = [
        {'name': 'host1', 'status': 'running', 'ip': '127.0.0.1'},
        {'name': 'host2', 'status': 'running', 'ip': '127.0.0.2'},
        {'name': 'host3', 'status': 'running', 'ip': '127.0.0.3'},
        {'name': 'host4', 'status': 'running', 'ip': '127.0.0.4'},
        {'name': 'host5', 'status': 'running', 'ip': '127.0.0.5'},
        {'name': 'host6', 'status': 'running', 'ip': '127.0.0.6'},
        {'name': 'host7', 'status': 'running', 'ip': '127.0.0.7'},
        {'name': 'host8', 'status': 'running', 'ip': '127.0.0.8'},
        {'name': 'host9', 'status': 'running', 'ip': '127.0.0.9'},
        {'name': 'host10', 'status': 'running', 'ip': '127.0.0.10'},
        ]
    return render_template('servers.html', servers=servers)

if __name__ == "__main__":
    app.run()
