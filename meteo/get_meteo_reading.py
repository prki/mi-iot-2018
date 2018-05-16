from mcp3208 import MCP3208
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import csv

GPIO.setmode(GPIO.BCM)

adc = MCP3208()

gas_channel = 2
light_channel = 6
dht_pin_bcm = 17

def get_percentage_value(min_val, max_val, value):
    value -= min_val
    max_val -= min_val

    percentage = (value * 100) / max_val
    return percentage

def get_temp_humidity(bcm_pin):
    humidity = None
    temperature = None

    while humidity is None or temperature is None:
        humidity = None
        temperature = None
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, bcm_pin)

    return temperature, humidity

def get_gas_percentage(channel):
    gas_min_volt = 0
    gas_max_volt = 4096

    gas_val = adc.read(channel)

    return get_percentage_value(gas_min_volt, gas_max_volt, gas_val)

def get_light_percentage(channel):
    light_avg_val = 2000
    light_dark_val = 0
    light_bright_val = 4096

    val = adc.read(channel)

    if val > light_bright_val:
        val = light_bright_val
    elif val < light_dark_val:
        val = light_dark_val

    return get_percentage_value(light_dark_val, light_bright_val, val)

temp, hum = get_temp_humidity(dht_pin_bcm)
gas = get_gas_percentage(gas_channel)
light = get_light_percentage(light_channel)

with open('meteo_data.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    cur_time = int(time.time())
    writer.writerow([cur_time, temp, hum, gas, light])

