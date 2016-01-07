# -*- coding: utf-8 -*-
import os, time
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
import logging
from logging.handlers import RotatingFileHandler
from time import gmtime, strftime
import json
import urllib2

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
    return '%s | %s | %s' %(_get_time(), session['username'], msg)

def _parser_log():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    log_file = 'foo.log'
    content = ""
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            content = reversed(f.readlines())

    for line in content:
        logs.append(line.split('|'))
    return logs

def _load_remote_json(domain, route):
    url = "http://" + domain + ":5000/" + route
    print url
    try:
        data = json.load(urllib2.urlopen(url, timeout = 2))
    except urllib2.URLError, e:
        app.logger.info(_format_log("Timeout: " + url))
        return None
    return data

def _check_server_up(hostname):
    import socket;
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    result = sock.connect_ex((hostname, 22))
    if result == 0:
        return True
    return False

g_all_servers = [
    {'id': 'SanFrancisco-1', 'domain': 'netqe-vm-243.cn.oracle.com'},
    {'id': 'BeiJing-1', 'domain': 'netqe-vm-237.cn.oracle.com'},
    {'id': 'SuZhou-vm', 'domain': '192.168.1.71'},
    ]
'''online server'''
g_servers = []

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
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	logs = _parser_log()
	return render_template('dashboard.html',logs=logs)

@app.route('/logs')
def show_log():
	logs = _parser_log()
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
        # instances = [
        #     {'name': 'host1', 'status': '1', 'ip': '127.0.0.1'},
        #     {'name': 'host2', 'status': '2', 'ip': '127.0.0.2'},
        #     {'name': 'host3', 'status': '3', 'ip': '127.0.0.3'},
        #     {'name': 'host4', 'status': '1', 'ip': '127.0.0.4'},
        #     {'name': 'host5', 'status': '2', 'ip': '127.0.0.5'},
        #     {'name': 'host6', 'status': '3', 'ip': '127.0.0.6'},
        #     {'name': 'host7', 'status': '1', 'ip': '127.0.0.7'},
        #     {'name': 'host8', 'status': '2', 'ip': '127.0.0.8'},
        #     {'name': 'host9', 'status': '3', 'ip': '127.0.0.9'},
        #     {'name': 'host10', 'status': '1', 'ip': '127.0.0.10'},
        #     ]
        # print instances
        instances = []
        for serv in g_servers:
            print serv
            ins = _load_remote_json(serv['domain'], "list")
            if ins:
                instances.append()
        print instances
        if len(instances) == 0:
            instances = [
                {'name': 'host1', 'status': '1', 'ip': '127.0.0.1'},
                {'name': 'host2', 'status': '2', 'ip': '127.0.0.2'},
                {'name': 'host3', 'status': '3', 'ip': '127.0.0.3'},
                ]
        return render_template('instances.html', instances=instances, servers=g_servers)

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

@app.route('/users')
def users():
	if not session.get('logged_in'):
		abort(401)
	users = [
            {'name': 'admin', 'id': '1', 'role': 'admin'},
			{'name': 'Qingzhou', 'id': '2', 'role': 'server admin'},
			{'name': 'Alex', 'id': '3', 'role': 'server admin'},
			{'name': 'yuanyue', 'id': '4', 'role': 'instance admin'},
			{'name': 'Peirong', 'id': '5', 'role': 'instance admin'},
			{'name': 'Sonny', 'id': '6', 'role': 'instance admin'},
			{'name': 'Chenchen', 'id': '7', 'role': 'instance admin'}
            ];
	return render_template('users.html', users=users)

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
            return redirect(url_for('dashboard'))
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
    return render_template('servers.html', servers=g_servers)

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    for server in g_all_servers:
        print server
        if _check_server_up(server['domain']):
            g_servers.append(server)
            print str(server) + " is up!"
    app.run('0.0.0.0')
