#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

def readnfc():
    reader = SimpleMFRC522()
    id, data = reader.read()
    return id


while True:
    print("Waiting...")
    id = readnfc()
    print(id)
    sleep(2)

    
