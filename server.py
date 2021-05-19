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
import datetime
from flask import Flask
from flask import request
from flask import render_template
from flask import render_template_string
from flask import Response
from waitress import serve
import gettext
from flask_babel import Babel
import azure_auth

localedir = './translations/'
translate = gettext.translation('messages', localedir, fallback=True,languages=['nb'])
_ = translate.gettext
translate.install()

api = Flask(__name__)
babel = Babel(api, default_locale='nb_NO')
api.config['BABEL_DEFAULT_LOCALE'] = 'nb_NO'

dbcnx = azure_auth.dbcnx()
                  
def render_js(fname, **kwargs):
    with open(fname) as fin:
        script = fin.read()
        rendered_script = render_template_string(script, **kwargs)
        return rendered_script

@api.route("/ping")
def ping():
    return render_template('message.html', message=_("pong"))

@api.route("/checkin", methods=['POST'])


def checkin():
    if request.form.get('Checkin'):
        try:
            conn=dbcnx.get_db()
            id = db.insert_checkin(conn,tag=request.form['tag'])
            if id > 0:
                js = render_js('static/scripts.js', a=3000)
                return render_template('message.html',
                                       message=_('Welcome back, ') + request.form['tag'], returnscript = js)
            elif id == -2:
                return render_template('message.html',
                                       message=_('Are you sure you\'re registered?'),
                                       fault=True)
            else:
                js = render_js('static/scripts.js', a=30000)
                return render_template('message.html',
                                       message=_('Are you already checked in?'), returnscript = js,
                                       fault=True)
        except:
            js = render_js('static/scripts.js', a=30000)
            return render_template('message.html',
                                   fault=True,
                                   message=_('Something went wrong. Are you registered?'), returnscript = js)

    elif request.form.get('Checkout'):
        try:
            conn=dbcnx.get_db()
            id = db.insert_checkout(conn,tag=request.form['tag'])
            name = db.get_name(conn,request.form['tag'])
            if id > 0:
                js = render_js('static/scripts.js', a=3000)
                return render_template('message.html', message=_('See you soon, ') + request.form['tag'], returnscript = js)
            else:
                js = render_js('static/scripts.js', a=30000)
                return render_template('message.html',
                                       message=_('Are you already checked out?'),
                                       fault=True, returnscript = js)
        except:
            js = render_js('static/scripts.js', a=30000)
            return render_template('message.html',
                                   fault=True,
                                   message=_('Something went wrong!'), returnscript = js)
    elif request.form.get('Token'):
        conn = dbcnx.get_db()
        id = db.prepare_register_token(conn, tag=request.form['tag'])
        if id > 0:
            js = render_js('static/scripts.js', a=30000)
            return render_template('message.html', message=_('Place your token on the reader. After one short blink, remove token. When both lights blink, you are registed, and can check in by placing your token on the reader again'), returnscript = js)
        else:
         js = render_js('static/scripts.js', a=15000)
         return render_template('message.html',
                                fault=True,
                                message=_('Something went wrong!'), returnscript = js)   
                                   
    else:
        js = render_js('static/scripts.js', a=30000)
        return render_template('message.html',
                               fault=True,
                               message=_('Invalid parameter?'), returnscript = js)



@api.route("/")
def index():
    return render_template('index.html')

@api.route("/register")
def register():
    return render_template('newuser.html')

@api.route("/guest")
def guest():
    return render_template('guestuser.html')

@api.route("/register/add",methods=['POST'])
def adduser():
    try:
        conn=dbcnx.get_db()
        if request.form['name'] and request.form['tag'] and request.form['email'] and request.form['phone']:
            retval = db.new_user(conn,
                                 request.form['tag'],
                                 request.form['email'],
                                 request.form['phone'],
                                 request.form['name'])
            if retval == -1:
                return render_template('message.html', message=_('Are you sure you\'re not already registered?'))
            elif retval == -2:
                return render_template('message.html', message=_('Something went wrong, try again later'))
            else:
                return render_template('message.html',
                                       message=_('Welcome, ') + request.form['tag'])
        else:
            return render_template('message.html', message=_('Missing some items...'))
    except:
        return render_template('message.html',
                               message=_('Something wrong happened!<br />Already registered?'))

@api.route("/guest/add",methods=['POST'])
def add_guest():
    try:
        conn=dbcnx.get_db()
        if request.form['name'] and request.form['email'] and request.form['phone']:
            retval = db.insert_guest_checkin(conn,
                                 request.form['email'],
                                 request.form['phone'],
                                 request.form['name'])
            js = render_js('static/scripts.js', a=60000)
            return render_template('message.html',
                                       message=_('Welcome, ') + request.form['name'], guest=True, returnscript = js)
        else:
            return render_template('message.html', message=_('Missing some items...'))
    except:
        return render_template('message.html',
                               message=_('Something wrong happened!'))



@api.template_filter('formattime')
def formattime_filter(s,format="%H:%M"):
    if isinstance(s, int):
        return datetime.datetime.fromtimestamp(s).strftime(format)
    else:
        return _('Still here!')

@api.template_filter('formattime_onlydate')
def formattime_onlydate_filter(s,format="%d. %b"):
    if isinstance(s, int):
        return datetime.datetime.fromtimestamp(s).strftime(format)
    else:
        return _('Still here!')

def formattime_full(s,format="%d. %b   %H:%M"):
    if isinstance(s, int):
        return datetime.datetime.fromtimestamp(s).strftime(format)
    else:
        return _('Something is fucked')

    
@api.route("/list")
def list():
    conn=dbcnx.get_db()
    visits = db.get_entries(conn,start = 0, count=15)
    return render_template('list.html', visits = visits)

@api.route("/list/checkout")
def list_checkedin():
    conn=dbcnx.get_db()
    visits = db.get_entries(conn,start = 0, count=200, checkedin=True)
    return render_template('list.html', visits = visits, checkedin=True)
    

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
    conn=get_db()
    response = db.get_entries(conn,start = start, count=count)
    csv = 'Tag, Checkin, Checkout\n'
    for row in response:
        csv += row[0]+", "+str(time.ctime(row[1]))+", "+str(time.ctime(row[2]))+'\n'
    response = Response(csv)
    response.headers['Content-Type'] = 'text/csv'
    return response

if __name__ == '__main__':
    serve(api, port=config.listen_port(), host=config.listen_ip())

