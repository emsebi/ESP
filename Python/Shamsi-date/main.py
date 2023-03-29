import wifimgr   
from time import sleep     
import network, urequests, utime, machine
import gc
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import shamsi

#date
urldt = "http://worldtimeapi.org/api/timezone/Asia/tehran" # see http://worldtimeapi.org/timezones
web_query_delay = 60000 # interval time of web JSON query
retry_delay = 5000 # interval time of retry after a failed Web query

try:
  import usocket as socket
except:
  import socket
led = machine.Pin(2, machine.Pin.OUT)
wlan = wifimgr.get_connection()       
if wlan is None:
    print("Could not initialize the network connection.")
    while True:
        pass  
print("ESP OK0")
led_state = "OFF"

def web_page():
    html = """<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css"
     integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
    <style>
        html {
            font-family: Arial;
            display: inline-block;
            margin: 0px auto;
            text-align: center;
        }

        .button {
            background-color: #ce1b0e;
            border: none;
            color: white;
            padding: 16px 40px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
        }

        .button1 {
            background-color: #000000;
        }
    </style>
</head>

<body>
    <h2>ESP MicroPython Web Server</h2>
    <p>LED state: <strong>""" + led_state + """</strong></p>
    <p>
        <i class="fas fa-lightbulb fa-3x" style="color:#c81919;"></i>
        <a href=\"?led_2_on\"><button class="button">LED ON</button></a>
    </p>
    <p>
        <i class="far fa-lightbulb fa-3x" style="color:#000000;"></i>
        <a href=\"?led_2_off\"><button class="button button1">LED OFF</button></a>
    </p>
</body>

</html>"""
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

    
        
while True:
    try:
        if gc.mem_free() < 102000:
            gc.collect()
        conn, addr = s.accept()
        conn.settimeout(3.0)
        print('Received HTTP GET connection request from %s' % str(addr))
        request = conn.recv(1024)
        conn.settimeout(None)
        request = str(request)
        print('GET Rquest Content = %s' % request)
        
        led_on = request.find('/?led_2_on')
        led_off = request.find('/?led_2_off')
        if led_on == 6:
            print('LED ON -> GPIO2')
            led_state = "ON"
            led.on()
        if led_off == 6:
            print('LED OFF -> GPIO2')
            led_state = "OFF"
            led.off()
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
        
        # HTTP GET data
        responsedt = urequests.get(urldt)
        if responsedt.status_code == 200: # query success
        
            print("JSON response:\n", responsedt.text)
            
            # parse JSON
            parsed = responsedt.json()
            datetime_str = str(parsed["datetime"])
            year = int(datetime_str[0:4])
            month = int(datetime_str[5:7])
            day = int(datetime_str[8:10])
            hour = int(datetime_str[11:13])
            minute = int(datetime_str[14:16])
            second = int(datetime_str[17:19])
            subsecond = int(round(int(datetime_str[20:26]) / 10000))
                        
# LCD 16x2 Print Code
        I2C_ADDR = 0x27
        totalRows = 2
        totalColumns = 16
        i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000) #I2C for ESP32
        #i2c = I2C(scl=Pin(5), sda=Pin(4), freq=10000) #I2C for ESP8266
        lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)
        lcd.putstr(str(year)+"/"+str(month)+"/"+str(day))
        #lcd.clear()
        lcd.move_to(0,1)
        # Date To Shamsi
        shamsidt = shamsi.gregorian_to_jalali(year, month, day)
        lcd.putstr(str(shamsidt))
        sleep(5)
        lcd.clear()
        lcd.putstr(str(hour)+":"+str(minute)+":"+str(subsecond))
        sleep(5)
        lcd.clear()
        lcd.putstr(str(addr))
        sleep (3)
    
        
        
                 
    except OSError as e:
        conn.close()
        print (str(addr))
        print('Connection closed')