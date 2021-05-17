#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import db
import azure_auth

dbcnx = azure_auth.dbcnx()

def MFRC522_Init(self):
    GPIO.output(self.NRSTPD, 1)
    self.Write_MFRC522(self.RFCfgReg, (0x07<<4))

def readnfc():
    reader = SimpleMFRC522()
    id, data = reader.read()
    return id


while True:
    print("Waiting...")
    serial = readnfc()
    print(serial)
    conn = dbcnx.get_db()
    tag = db.get_usertag(conn,serial)
    res = db.insert_checkin(conn,tag)
    if res > 0:
        #Success...
    elif res == -1:
        #User is already checked in; check out
        db.insert_checkout(conn, tag)
    sleep(5)

    

    
