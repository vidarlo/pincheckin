#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import db
import azure_auth


class leds:
    def __init__(self):
        self.in_led = 3
        self.out_led = 5
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in_led, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.out_led, GPIO.OUT, initial=GPIO.LOW)

    def in_light(self):
        GPIO.output(self.in_led, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(self.in_led, GPIO.LOW)
        sleep(0.25)
        GPIO.output(self.in_led, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(self.in_led, GPIO.LOW)

    def out_light(self):
        GPIO.output(self.out_led, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(self.out_led, GPIO.LOW)
        sleep(0.25)
        GPIO.output(self.out_led, GPIO.HIGH)
        sleep(0.25)
        GPIO.output(self.out_led, GPIO.LOW)

    def error_light(self):
        GPIO.output(self.out_led, GPIO.HIGH)
        GPIO.output(self.in_led, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(self.in_led, GPIO.LOW)
        GPIO.output(self.out_led, GPIO.LOW)

    def rd_flash(self):
        GPIO.output(self.in_led, GPIO.HIGH)
        sleep(0.1)
        GPIO.output(self.in_led, GPIO.LOW)
        
msg = leds()
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
        if db.is_checkedin(conn, tag):
            db.insert_checkout(conn, tag)
            msg.out_light()
            return("Checked out")
        else:
            db.insert_checkin(conn, tag)
            msg.in_light()
            return("Checked in")
    else:
        msg.error_light()
        db.register_token(conn, serial)
        return("No such token serial")
    conn.close()

if __name__ == "__main__":
    while True:
        serial = readnfc()
        msg.rd_flash()
        print(serial)
        print(update_userstatus(serial))
    
    
