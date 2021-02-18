#    BFK Pinball Player Checkin system
#    Copyright (C) 2021 Vidar Løkken <vl@bitsex.net>

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import config
import db
import os
import time
import json
import datetime
from flask import Flask
from flask import request
from flask import render_template
from flask import render_template_string
from flask import Response

listen_ip = config.listen_ip()
listen_port = config.listen_port()

api = Flask(__name__)

def render_js(fname, **kwargs):
    with open(fname) as fin:
        script = fin.read()
        rendered_script = render_template_string(script, **kwargs)
        return rendered_script

@api.route("/ping")
def ping():
    return render_template('message.html', message="pong")

@api.route("/checkin", methods=['POST'])




def checkin():
    if request.form.get('Checkin'):
        try:
            conn=db.create_connection(config.DBFile())
            id = db.insert_checkin(conn,tag=request.form['tag'])
            if id > 0:
                print("ready to make javascript, if")
                js = render_js('static/scripts.js', a=10000)
                return render_template('message.html',
                                       message="Velkommen hjem, " + request.form['tag'], js = js)
            else:
                print("ready to make javascript, else")
                js = render_js('static/scripts.js', a=30000)
                return render_template('message.html',
                                       message='Are you already checked in?', js = js,
                                       fault=True)
        except:
            print("ready to make javascript, except")
            js = render_js('static/scripts.js', a=30000)
            return render_template('message.html',
                                   fault=True,
                                   message='Are you already logged in?', js = js)

    elif request.form.get('Checkout'):
        try:
            conn=db.create_connection(config.DBFile())
            id = db.insert_checkout(conn,tag=request.form['tag'])
            name = db.get_name(conn,request.form['tag'])
            if id > 0:
                return render_template('message.html',
                                       message="Takk for besøket, " + request.form['tag'])
            else:
                return render_template('message.html',
                                       message='Are you already checked out?',
                                       fault=True)
        except:
            return render_template('message.html',
                                   fault=True,
                                   message="Are you already logged out?")
    else:
        return render_template('message.html',
                               fault=True,
                               message="Invalid parameter?")



@api.route("/")
def index():
    return render_template('index.html')

@api.route("/register")
def register():
    return render_template('newuser.html')

@api.route("/register/add",methods=['POST'])
def adduser():
    try:
        conn=db.create_connection(config.DBFile())
        if request.form['name'] and request.form['tag'] and request.form['email'] and request.form['phone']:
            retval = db.new_user(conn,
                                 request.form['tag'],
                                 request.form['email'],
                                 request.form['phone'],
                                 request.form['name'])
            if retval == -1:
                return render_template('message.html', message="Are you sure you're not already registered?")
            elif retval == -2:
                return render_template('message.html', message="Something went wrong, try again later")
            else:
                return render_template('message.html',
                                       message="Welcome, " + request.form['tag'])
        else:
            return render_template('message.html', message="Missing some items...")
    except:
        return render_template('message.html',
                               message="Something wrong happened!<br />Already registered?")


@api.template_filter('formattime')
def formattime_filter(s,format="%H:%M"):
    if isinstance(s, int):
        return datetime.datetime.fromtimestamp(s).strftime(format)
    else:
        return "Still here!"

@api.template_filter('formattime_onlydate')
def formattime_onlydate_filter(s,format="%d. %b"):
    if isinstance(s, int):
        return datetime.datetime.fromtimestamp(s).strftime(format)
    else:
        return "Still here!"

    
@api.route("/list")
def list():
    print("trying to make list")
    conn=db.create_connection(config.DBFile())
    print("connection made")
    visits = db.get_entries(conn,start = 0, count=10)
    print("found the last 10 entries")
    conn.close()
    print("closed connection")
    return render_template('list.html', visits = visits)
    print("made viewing")
    

@api.route("/list/csv")
def csv():
    start = None
    count = None
    try:
        start = int(request.form['start'])
    except:
        start = 0
    try:
        count = int(request.form['count'])
    except:
        count = 25;
    conn=db.create_connection(config.DBFile())
    response = db.get_entries(conn,start = start, count=count)
    conn.close()
    csv = 'Tag, Checkin, Checkout\n'
    for row in response:
        csv += row[0]+", "+str(time.ctime(row[1]))+", "+str(time.ctime(row[2]))+'\n'
    response = Response(csv)
    response.headers['Content-Type'] = 'text/csv'
    return response
