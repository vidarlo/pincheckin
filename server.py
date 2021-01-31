import responder
import config
import db

listen_ip = config.listen_ip()
listen_port = config.listen_port()

api = responder.API()

@api.route("/ping")
def ping(req, resp):
    resp.text = "pong"

@api.route("/checkin/")
def checkin(req, resp):
    print(req)
    checkinid = db.insert_checkin(tag)
    resp.media = {"id":checkinid}

print(listen_ip)
api.run(address=listen_ip,port=listen_port)
