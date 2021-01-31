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

@api.route("/checkin/")
async def receive_incoming(req, resp):
    data = await req.media()
    id = db.insert_checkin(conn,tag=data['tag'])
    resp.media = {"id":id}

@api.route("/checkout/")
async def receive_incoming(req, resp):
    data = await req.media()
    id = db.insert_checkout(conn,tag=data['tag'])
    resp.media = {"id":id}

print(listen_ip)
api.run(address=listen_ip,port=listen_port)
