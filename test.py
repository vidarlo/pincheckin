import db
import config
db_file = config.DBFile()

conn = db.create_connection(db_file)
#new_user = db.new_user(conn,'HAG','foo@example.com','+12345678901')
checkin = db.insert_checkin(conn, 'HAG')
checkout = db.insert_checkout(conn,'HAG')
#print(new_user)
print(checkin)
print(checkout)
