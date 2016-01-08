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

g_all_servers = [
    {'id': 'ORACLE-X5-1', 'domain': 'netqe-vm-243.cn.oracle.com'},
    {'id': 'ORACLE-T5-1', 'domain': 'netqe-vm-237.cn.oracle.com'},
    {'id': 'SUZHOU-VM', 'domain': '192.168.1.71'},
    ]
g_servers_map = {
    'ORACLE-X5-1': 'netqe-vm-243.cn.oracle.com',
    'ORACLE-T5-1': 'netqe-vm-237.cn.oracle.com',
    'SUZHOU-VM': '192.168.1.71'
}
'''online server'''
g_servers = []
TIMEOUT = 5
g_users =  [
	{'name': 'admin', 'id': '1', 'role': 'admin'},
	{'name': 'Qingzhou', 'id': '2', 'role': 'server admin'},
	{'name': 'Alex', 'id': '3', 'role': 'server admin'},
	{'name': 'yuanyue', 'id': '4', 'role': 'instance admin'},
	{'name': 'Peirong', 'id': '5', 'role': 'instance admin'},
	{'name': 'Sonny', 'id': '6', 'role': 'instance admin'},
	{'name': 'Chenchen', 'id': '7', 'role': 'instance admin'}
	]
'''
helpers
'''
def _get_time():
    return strftime("%Y-%m-%d %H:%M:%S", gmtime())

def _format_log(msg):
    username = session['username']
    return '%s | %s | %s' %(_get_time(), username, msg)

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
        data = json.load(urllib2.urlopen(url, timeout = TIMEOUT))
    # except urllib2.URLError, e:
    except:
        # app.logger.info(_format_log("Timeout: " + url))
        print "Timeout: " + url
        return None
    return data

def _check_server_up(hostname):
    import socket;
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(TIMEOUT)
    result = sock.connect_ex((hostname, 22))
    if result == 0:
        return True
    return False

def _check_servers(log=True):
    global g_servers
    g_servers = []
    for i, _ in enumerate(g_all_servers):
        if _check_server_up(g_all_servers[i]['domain']):
            g_servers.append(g_all_servers[i])
            g_all_servers[i]['status'] = 1
            if log:
                app.logger.info(_format_log(g_all_servers[i]['domain'] + " is up!"))
            else:
                print g_all_servers[i]['domain'] + " is up!"
            # print str(g_all_servers[i]) + " is up!"
        else:
            g_all_servers[i]['status'] = 0
            if log:
                app.logger.info(_format_log(g_all_servers[i]['domain'] + " is down!"))
            else:
                print g_all_servers[i]['domain'] + " is down!"
'''
DB
'''

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
	serversNum=len(g_all_servers)
	usersNum=len(g_users)
	logsNum=len(logs)
	return render_template('dashboard.html',logs=logs,serversNum=len(g_all_servers),usersNum=usersNum,logsNum=logsNum)

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
    messages = []
    if request.method == 'POST':
        app.logger.info(_format_log(json.dumps(request.form)))
        name = request.form['name']
        compute_id = request.form['compute_id']

        if 'poweron' in request.form:
            result = _load_remote_json(compute_id, "boot?name=" + name)
            messages.append("PowerOn Zone - " + name +"!")

        if 'poweroff' in request.form:
            result = _load_remote_json(compute_id, "stop?name=" + name)
            messages.append("PowerOff Zone - " + name +"!")

        if 'powercycle' in request.form:
            result = _load_remote_json(compute_id, "reboot?name=" + name)
            messages.append("Reboot Zone - " + name +"!")

        if 'suspend' in request.form:
            result = _load_remote_json(compute_id, "stop?name=" + name)
            messages.append("Suspend Zone - " + name +"!")

        if 'resume' in request.form:
            result = _load_remote_json(compute_id, "boot?name=" + name)
            messages.append("Resume Zone - " + name +"!")

        if 'configure' in request.form:
            return redirect("/servers/" + compute_id + "/instance?name=" + name)


        print result


    # if request.method == 'GET':
        # instances = {'server': [
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
        #     ]}
        # print instances
    instances = {}
    for serv in g_servers:
        print serv
        ins = _load_remote_json(serv['domain'], "list")
        if ins:
            # for i,_ in enumerate(ins)
            # instances.extend(ins)
            instances[serv['domain']] = ins

    if len(instances) == 0:
        instances = {'netqe-vm-243.cn.oracle.com': [
            {'name': 'zone1', 'status': 'installed', 'ip': '127.0.0.1', 'brand': 'solaris'}],
            'netqe-vm-237.cn.oracle.com': [
            {'name': 'zone2', 'status': 'incomplete', 'ip': '127.0.0.2', 'brand': 'solaris'},
            {'name': 'zone3', 'status': 'running', 'ip': '127.0.0.3', 'brand': 'solaris'}]}
    print instances
    return render_template('instances.html', instances=instances, servers=g_servers, messages=messages)

        # return render_template('instance.html', test="xxx", entry="xxx")

@app.route('/users')
def users():
	if not session.get('logged_in'):
		return redirect(url_for('login'))
	return render_template('users.html', users=g_users)

@app.route('/servers/<server_name>/create/')
def create_instance(server_name):
    if not session.get('logged_in'):
        abort(401)
    instance_name = request.args.get('name', '')
    messages = []
    msg = "Create Zone - %s on %s" % (instance_name, server_name)
    app.logger.info(_format_log(msg))
    messages.append(msg)

    result = _load_remote_json(g_servers_map[server_name], "boot?name=" + instance_name)
    print result
    entry = {
    'status' : 'installed'
    }
    return render_template('instance.html', instance_name=instance_name, messages=messages, entry= entry)

@app.route('/servers/<server_name>/instance/')
def configure_instance(server_name):
    if not session.get('logged_in'):
        abort(401)
    instance_name = request.args.get('name', '')
    messages = []
    msg = "Get Configure of Zone - %s on %s" % (instance_name, server_name)
    app.logger.info(_format_log(msg))
    messages.append(msg)
    entry = {
    'status' : 'running'
    }
    return render_template('instance.html', instance_name=instance_name, messages=messages, entry=entry)

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
    _check_servers()
    return render_template('servers.html', servers=g_all_servers)

@app.route('/cpuUsage')
def cpuUsage():
	if len(g_servers) == 0:
		d = {'kernel':'0.8%','user':'0.4%'}
		return json.dumps(d)
	usage = _load_remote_json(g_servers[0]['domain'], "hostinfo")
	return json.dumps(usage)

if __name__ == "__main__":
    handler = RotatingFileHandler('foo.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    _check_servers(log=False)
    app.run('0.0.0.0')
