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

import responder
import config
import db
import os

listen_ip = config.listen_ip()
listen_port = config.listen_port()

api = responder.API()
conn=db.create_connection(config.DBFile())

@api.route("/ping")
def ping(req, resp):
    resp.text = "pong"

@api.route("/checkin")
async def receive_incoming(req, resp):
    data = await req.media()
    id = db.insert_checkin(conn,tag=data['tag'])
    resp.media = {"id":id}

@api.route("/checkout")
async def receive_incoming(req, resp):
    data = await req.media()
    id = db.insert_checkout(conn,tag=data['tag'])
    resp.media = {"id":id}

@api.route("/")
def landing_html(req, resp):
    resp.html = api.template('index.html')

@api.route("/register")
def register(req,resp):
    resp.html = api.template('newuser.html')    

@api.route("/list")
async def list(req, resp):
    data = await req.media()
    start = None
    count = None
    try:
        start = int(data['start'])
    except:
        start = 0
    try:
        count = int(data['count'])
    except:
        count = 25;
    
    response = db.get_entries(conn,start = start, count=count)
    resp.media = response

@api.route("/list/csv")
async def list(req, resp):
    data = await req.media()
    start = None
    count = None
    try:
        start = int(data['start'])
    except:
        start = 0
    try:
        count = int(data['count'])
    except:
        count = 25;
    resp.headers['Content-Type'] = 'text/csv'
    response = db.get_entries(conn,start = start, count=count)
    csv = 'Tag, Checkin, Checkout\n'
    for row in response:
        csv += row[0]+", "+str(row[1])+", "+str(row[2])+'\n'
    resp.text = csv
    
api.run(address=listen_ip,port=listen_port)
