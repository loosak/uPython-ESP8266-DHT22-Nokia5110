"""
* Nokia 5110
* Connections:
* WeMos D1 Mini   Nokia 5110    Description
* (ESP8266)       PCD8544 LCD
*
* D2 (GPIO4)      0 RST         Output from ESP to reset display
* D1 (GPIO5)      1 CE          Output from ESP to chip select/enable display
* D6 (GPIO12)     2 DC          Output from display data/command to ESP
* D7 (GPIO13)     3 Din         Output from ESP SPI MOSI to display data input
* D5 (GPIO14)     4 Clk         Output from ESP SPI clock
* 3V3             5 Vcc         3.3V from ESP to display
* D0 (GPIO16)     6 BL          3.3V to turn backlight on, or PWM
* G               7 Gnd         Ground
"""

from machine import Pin, SPI
from time import sleep, ticks_ms
import upcd8544

spi = SPI(1, baudrate=80000000, polarity=0, phase=0)
RST = Pin(4)
CE = Pin(5)
DC = Pin(12)
BL = Pin(16)
lcd = upcd8544.PCD8544(spi, RST, CE, DC, BL)

#lcd.light_on()
#lcd.light_off()

# Use a framebuffer to store the 4032 pixels (84x48):

import framebuf
width = 84
height = 48
pages = height // 8
buffer = bytearray(pages * width)
framebuf = framebuf.FrameBuffer1(buffer, width, height)

# Print Hello, World! using the 8x8 font:

framebuf.text("Hello,", 0, 0, 1)
framebuf.text("World!", 0, 9, 1)
lcd.data(buffer)
sleep(5)

def elTime(sec):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)

import dht
DHTPIN = Pin(2)
dht = dht.DHT22(DHTPIN)

# Update display
while(True):
	dht.measure()
	seconds = ticks_ms()/1000
	framebuf.fill(0)
	framebuf.text(elTime(seconds), 0, 0, 1)
	framebuf.text("%7d" % (ticks_ms() // 1000), 0, 11, 1)
	#framebuf.text("Temp", 0, 11, 1)
	framebuf.text("%.1f C" % dht.temperature(), 0, 20, 1)
	framebuf.text("Humidity", 0, 31, 1)
	framebuf.text("%.1f %%" % dht.humidity(), 0, 40, 1)
	lcd.data(buffer)
	sleep(1)
