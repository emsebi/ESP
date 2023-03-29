import machine
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from time import sleep
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) #I2C for ESP32
#i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000) #I2C for ESP8266
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
i = 1
while True:
 lcd.putstr("heloo" + str(i))
 lcd.clear()
 i = i+1;
 print ( " heloo" , i )