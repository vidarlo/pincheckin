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

listen_ip = config.listen_ip()
listen_port = config.listen_port()

api = Flask(__name__)

@api.route("/ping")
def ping():
    return render_template('message.html', message="pong")

@api.route("/checkin", methods=['POST'])
def checkin():
    try:
        conn=db.create_connection(config.DBFile())
        id = db.insert_checkin(conn,tag=request.form['tag'])
        name = db.get_name(conn,request.form['tag'])
        return render_template('checkin.html', tag=request.form['tag'], name=name)
    except:
        return render_template('checkin.html', fault=True)

@api.route("/checkout")
def checkout():
    try:
        conn=db.create_connection(config.DBFile())
        id = db.insert_checkout(conn,tag=request.form['tag'])
        name = db.get_name(conn,request.form['tag'])
        return render_template('checkin.html', tag=request.form['tag'], name=name)
    except:
        return render_template('checkin.html', fault=true)

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
def formattime_filter(s,format="%H:%M %d. %b"):
        return datetime.datetime.fromtimestamp(s).strftime(format)
    
@api.route("/list")
def list():
    conn=db.create_connection(config.DBFile())
    visits = db.get_entries(conn,start = 0, count=10)
    return render_template('list.html', visits = visits)
    

#@api.route("/list/csv")
#async def list(req, resp):
#    data = await req.media()
#    start = None
#    count = None
#    try:
#        start = int(data['start'])
#    except:
#        start = 0
#    try:
#        count = int(data['count'])
#    except:
#        count = 25;
#    resp.headers['Content-Type'] = 'text/csv'
#    response = db.get_entries(conn,start = start, count=count)
#    csv = 'Tag, Checkin, Checkout\n'
#    for row in response:
#        csv += row[0]+", "+str(time.ctime(row[1]))+", "+str(time.ctime(row[2]))+'\n'
#    resp.text = csv
    
#api.run(address=listen_ip,port=listen_port)
