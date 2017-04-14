# upython for ESP8266 DHT22 + Nokia 5110 LCD

WeMos D1 mini +  + Nokia 5110 (PCD8544)

![DHT Nokia]()

## Parts

* [WeMos D1 Mini] () $4.00 USD
* [WeMos DHT Pro Shield] (https://www.wemos.cc/product/dht-pro-shield.html)
* [Nokia 5110 LCD module] () $2.10 USD

## Pinouts

[WeMos D1 Mini](https://hobbytronics.com.pk/wp-content/uploads/wemos-pinout.jpg)

## Install MicroPython on your ESP8266 device

Install [esptool](https://github.com/themadinventor/esptool/) with pip

```
$ pip install esptool
```

### Download latest MicroPython firmware

Open [http://micropython.org/download/#esp8266](http://micropython.org/download/#esp8266)

Download the latest firmware

### Flash firmware with esptool

```
$ esptool.py -p /dev/tty.wchusbserial1420 erase_flash
esptool.py v1.1
Connecting...
Erasing flash (this may take a while)...
```

Upload the new MicroPython firmware.

```
$ esptool.py -p /dev/tty.wchusbserial1420 write_flash -fm dio -fs 32m 0 esp8266-20160827-v1.8.3-61-g531217a.bin
```

More info in the [MicroPython docs](http://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#deploying-the-firmware) on flashing the firmware.

### Verify firmware

```
$ screen /dev/ttyUSB0  115200
```

To exit screen run: `Control+A` then `Control+\`.



### Setup and test Nokia 5110 display

Connections:

WeMos D1 Mini (ESP8266) | Nokia 5110 PCD8544 LCD | Description
----------------------- | ---------------------- | ----------------------------------------------
D2 (GPIO4)              | 0 RST                  | Output from ESP to reset display
D1 (GPIO5)              | 1 CE                   | Output from ESP to chip select/enable display
D6 (GPIO12)             | 2 DC                   | Output from display data/command to ESP
D7 (GPIO13)             | 3 Din                  | Output from ESP SPI MOSI to display data input
D5 (GPIO14)             | 4 Clk                  | Output from ESP SPI clock
3V3                     | 5 Vcc                  | 3.3V from ESP to display
D0 (GPIO16)             | 6 BL                   | 3.3V to turn backlight on, or PWM
G                       | 7 Gnd                  | Ground

Test the display:

```
>>> from machine import Pin, SPI
>>> import time
>>> import upcd8544

>>> spi = SPI(1, baudrate=80000000, polarity=0, phase=0)
>>> RST = Pin(4)
>>> CE = Pin(5)
>>> DC = Pin(12)
>>> BL = Pin(16)
>>> lcd = upcd8544.PCD8544(spi, RST, CE, DC, BL)
```

For my Nokia 5110 display, the `lcd.light_on()` and `lcd.light_off()` methods are reversed.

Switch off the backlight:

```
>>> lcd.light_on()
```

Switch on the backlight:

```
>>> lcd.light_off()
```

Use a framebuffer to store the 4032 pixels (84x48):

```
>>> import framebuf
>>> width = 84
>>> height = 48
>>> pages = height // 8
>>> buffer = bytearray(pages * width)
>>> framebuf = framebuf.FrameBuffer1(buffer, width, height)
```

Light every pixel:

```
>>> framebuf.fill(1)
>>> lcd.data(buffer)
```

Clear screen:

```
>>> framebuf.fill(0)
>>> lcd.data(buffer)
```

Print `Hello, World!` using the 8x8 font:

```
>>> framebuf.text("Hello,", 0, 0, 1)
>>> framebuf.text("World!", 0, 9, 1)
>>> lcd.data(buffer)
```


## Setup and test DHT22

![DHT22](http://www.electroschematics.com/11293/am2302-dht22-datasheet/)

Connections:

WeMos D1 Mini (ESP8266) | DHT12   | Description
----------------------- | ------- | ------------
3V3                     | 1 VDD   | 3.3V
D4 (GPIO2)              | 2 DATA  | Serial data
G                       | 4 GND   | Ground


Test the DHT22 sensor:

```
import dht
DHTPIN = Pin(2)
dht = dht.DHT22(DHTPIN)

dht.measure()
dht.temperature()
dht.humidity()
```



## Links

* [WeMos D1 Mini](http://www.wemos.cc/Products/d1_mini.html)
* [micropython.org](http://micropython.org)
* [Hardware SPI docs](http://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html#hardware-spi-bus)

## Credits

* Markus Birth's [wipy Nokia 5110 library](https://github.com/mbirth/wipy-upcd8544)
*
