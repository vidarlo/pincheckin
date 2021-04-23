#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import db

def MFRC522_Init(self):
    GPIO.output(self.NRSTPD, 1)
    self.Write_MFRC522(self.RFCfgReg, (0x07<<4))

def readnfc():
    reader = SimpleMFRC522()
    id, data = reader.read()
    return id

conn = db.create_connection('database.db')

while True:
    print("Waiting...")
    id = readnfc()
    print(id)
    print(db.get_usertag(conn,id))
    sleep(2)

    

    
