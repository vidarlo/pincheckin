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

def update_userstatus(serial):
    conn = dbcnx.get_db()
    tag = db.get_usertag(conn,serial)
    if not tag == -1:
        if db.ischeckedin(conn, tag):
            db.insert_checkout(conn, tag)
            return("Checked out")
        else:
            db.insert_checkin(conn, tag)
            return("Checked in")
    else:
        return("No such token serial")
        

def led_checkin():
    #Do something

def led_checkout():
    #Do something
            
        

if __name__ == "__main__":
    serial = readnfc()
    print(serial)
    
    
    
