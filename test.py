import db
import config
db_file = config.DBFile()

conn = db.create_connection(db_file)
#new_user = db.new_user(conn,'VLO','vl@bitsex.net','+4796628780')
checkin = db.insert_checkin(conn, 'VLO')
checkout = db.insert_checkout(conn,'VLO')
#print(new_user)
print(checkin)
print(checkout)
