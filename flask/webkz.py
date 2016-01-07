# -*- coding: utf-8 -*-
import os, time
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import logging
from logging.handlers import RotatingFileHandler
from time import gmtime, strftime
import json

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

'''
helpers
'''
def _get_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def _format_log(msg):
    return '%s | %s | Operation: %s' %(_get_time(), session['username'], msg)

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

@app.route('/logs')
def record_log():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    log_file = 'foo.log'
    content = ""
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            content = f.readlines()

    for line in content:
        logs.append(line.split('|'))
    return render_template('logs.html', logs=logs)

@app.route('/instances', methods=['GET', 'POST'])
def instances():
    # db = get_db()
    # cur = db.execute('select title, text from entries order by id desc')
    # instances = cur.fetchall()
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'GET':
        '''
        fake data here, pls replace it.
        '''
        instances = [
            {'name': 'host1', 'status': '1', 'ip': '127.0.0.1'},
            {'name': 'host2', 'status': '2', 'ip': '127.0.0.2'},
            {'name': 'host3', 'status': '3', 'ip': '127.0.0.3'},
            {'name': 'host4', 'status': '1', 'ip': '127.0.0.4'},
            {'name': 'host5', 'status': '2', 'ip': '127.0.0.5'},
            {'name': 'host6', 'status': '3', 'ip': '127.0.0.6'},
            {'name': 'host7', 'status': '1', 'ip': '127.0.0.7'},
            {'name': 'host8', 'status': '2', 'ip': '127.0.0.8'},
            {'name': 'host9', 'status': '3', 'ip': '127.0.0.9'},
            {'name': 'host10', 'status': '1', 'ip': '127.0.0.10'},
            ]
        # print instances
        servers = [
            {'id': 'server1', 'name': '192.168.1.3'},
            {'id': 'server2', 'name': '127.0.0.1'}
            ]
        return render_template('instances.html', instances=instances, servers=servers)

    if request.method == 'POST':
        print request.form
        name = request.form['name']
        if 'poweron' in request.form:
            pass

        if 'poweroff' in request.form:
            pass

        if 'powercycle' in request.form:
            pass

        if 'suspend' in request.form:
            pass

        if 'resume' in request.form:
            pass

        app.logger.info(_format_log(json.dumps(request.form)))

        return render_template('instances.html', test="xxx")

@app.route('/servers/<server_name>/create/')
def create_instance(server_name):
    if not session.get('logged_in'):
        abort(401)
    # db = get_db()
    # db.execute('insert into entries (title, text) values (?, ?)',
    #            [request.form['title'], request.form['text']])
    # db.commit()
    instance_name = request.args.get('name', '')
    app.logger.info(_format_log(json.dumps("Create Zone - %s on %s" % (instance_name, server_name))))
    return render_template('instance.html', instance_name=instance_name, entry="xxxx")

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
            session['username'] = request.form['username']
            app.logger.info(_format_log("login"))
            return redirect(url_for('instances'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    app.logger.info(_format_log("logout"))
    session.pop('logged_in', None)
    session.pop('username', None)
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
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run()
