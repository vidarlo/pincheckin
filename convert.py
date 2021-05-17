import azure_auth
import sqlite3

sqlite = sqlite3.connect('database.db')
dbcnx = azure_auth.dbcnx()
msql = dbcnx.get_db()

sc = sqlite.cursor()
mc = msql.cursor()
sql = '''INSERT INTO users(tag, email, phone, name) VALUES(%s,%s,%s,%s)'''
sc.execute("SELECT tag,email,phone,name FROM users ORDER BY id")
for row in sc:
    print(row)
    mc.execute(sql, row)

sql = '''INSERT INTO checkins(uid, checkin, checkout) VALUES(%s,%s,%s)'''
sc.execute("SELECT user, checkin, checkout FROM checkins ORDER BY id")
for row in sc:
    print(row)
    mc.execute(sql,row)

sql = '''INSERT INTO guest_checkins(time_stamp, name, email, phone) VALUES (%s,%s,%s,%s)'''
sc.execute("SELECT time_stamp, name, email, phone FROM guest_checkins")
for row in sc:
    print(row)
    mc.execute(sql, row)
msql.commit()
