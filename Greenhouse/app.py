import datetime
from itertools import count
import statistics
from flask import Flask
from flask import render_template
from fhict_cb_01.CustomPymata4 import CustomPymata4


app = Flask(__name__)

def current_time():
    dt = datetime.datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")


sensors = {
'id':'319',
'current_timestamp': current_time(),
'current_temperature': 0,
'current_humidity': 'current_humidity',
'current_brightness': 'current_brightness',
'average_temperature': 'average_temperature',
'average_humidity': 'average_humidity',
'average_brightness': 'average_brightness',
'max_temperature': 'max_temperature',
'min_temperature': 'min_temperature',
'max_humidity': 'max_humidity',
'min_humidity': 'min_humidity',
'max_brightness': 'max_brightness',
'min_brightness': 'min_brightness'
}


statistic= [sensors]


average_humdity = 0
average_temperature = 0
average_brightness = 0


humidity_list = []
temperature_list = []
brightness_list = []


def on_sensor_data_received_from_arduino(data):
    global humidity_list, temperature_list, average_humdity, average_temperature
    

    if (data[3] == 0):
        humidity = data[4]
        sensors['current_timestamp'] = current_time()
        sensors['current_humidity'] = humidity
        humidity_list.append(humidity)

        temperature = data[5]
        sensors['current_temperature'] = temperature
        temperature_list.append(temperature)
        
        
        average_humdity = round(sum(humidity_list) / len(humidity_list),2)
        
        sensors['average_humidity'] = average_humdity
        
        average_temperature = round( sum(temperature_list) / len(temperature_list),2)
        sensors['average_temperature'] = average_temperature

        max_temperature = round(max(temperature_list))
        sensors['max_temperature']=max_temperature

        min_temperature = round(min(temperature_list))
        sensors['min_temperature']=min_temperature

        min_humidity = round(min(humidity_list))
        sensors['min_humidity']=min_humidity

        max_humidity = round(max(humidity_list))
        sensors['max_humidity']=max_humidity



def on_ldr_data_received_from_arduino(data):
    global brightness_list, average_brightness
    sensors['current_timestamp'] = current_time()
    brightness = data[2]
    sensors['current_brightness'] = brightness
    brightness_list.append(brightness)
       
    average_brightness = round( sum(brightness_list) / len(brightness_list),2)
    sensors['average_brightness'] = average_brightness

    min_brightness = round(min(brightness_list))
    sensors['min_brightness']= min_brightness

    max_brightness = round(max(brightness_list))
    sensors['max_brightness']= max_brightness
       

DHTPIN  = 12
LDRPIN = 2


def setup():
    global board
    board = CustomPymata4(com_port = "COM3")
    board.displayOn()
    board.set_pin_mode_dht(DHTPIN, sensor_type=11, differential=.5, callback=on_sensor_data_received_from_arduino)
    board.set_pin_mode_analog_input(LDRPIN, callback = on_ldr_data_received_from_arduino, differential = 10)

setup()

@app.route('/')
def index():
    return render_template('index.html', statistics=statistic)


