import responder
import config
import db

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
    
api.run(address=listen_ip,port=listen_port)
