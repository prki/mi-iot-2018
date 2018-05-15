from flask import Flask, g, render_template
import csv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime

app = Flask(__name__)
CSVFILENAME = '../../../dev/meteo/meteo_data.csv'

"""
Reads the data out of the CSV file. CSV file is formatted as
timestamp, temperature, humidity, gas.
"""
def readData():
    with open(CSVFILENAME, 'r') as csvfile:
        reader = csv.reader(csvfile)
        timestamps = []
        temps = []
        humids = []
        gases = []
        lights = []
        for row in reader:
            timestamps.append(float(row[0]))
            temps.append(float(row[1]))
            humids.append(float(row[2]))
            gases.append(float(row[3]))
            lights.append(float(row[4]))

    return timestamps, temps, humids, gases, lights


def generateTempGraph(dates, temps):
    plt.xlabel('Dates')
    plt.ylabel('Temperature [C]')
    plt.title('Temperature over time')
    plt.plot(dates, temps)
    plt.gcf().autofmt_xdate()
    plt.savefig('static/graph_temperature.png')


def generateHumidGraph(dates, humids):
    plt.xlabel('Dates')
    plt.ylabel('Humidity [%]')
    plt.title('Air humidity over time')
    plt.plot(dates, humids)
    plt.gcf().autofmt_xdate()
    plt.savefig('static/graph_humidity.png')


def generateGasesGraph(dates, gases):
    plt.xlabel('Dates')
    plt.ylabel('CO in the air [%]')
    plt.title('CO in the air over time')
    plt.plot(dates, gases)
    plt.gcf().autofmt_xdate()
    plt.savefig('static/graph_gases.png')


def generateLightsGraph(dates, lights):
    plt.xlabel('Dates')
    plt.ylabel('Light intensity [%]')
    plt.title('Light intensity over time')
    plt.plot(dates, lights)
    plt.gcf().autofmt_xdate()
    plt.savefig('static/graph_lights.png')


def generateGraphs(dates, temps, humids, gases, lights):
    plt.clf() # Clear figure. Important in case a figure was loaded once already.
    generateTempGraph(dates, temps)
    plt.clf()
    generateHumidGraph(dates, humids)
    plt.clf()
    generateGasesGraph(dates, gases)
    plt.clf()
    generateLightsGraph(dates, lights)

@app.route('/')
def main_page():
    times, temps, humids, gases, lights = readData()
    dates = [datetime.datetime.fromtimestamp(ts) for ts in times]
    generateGraphs(dates, temps, humids, gases, lights)

    maxTemp = max(temps)
    minTemp = min(temps)

    maxHumidity = max(humids)
    minHumidity = min(humids)

    maxGas = max(gases)
    minGas = min(gases)

    maxLight = max(lights)
    minLight = min(lights)

    return render_template('main_page.html', maxTemp=maxTemp, minTemp=minTemp, maxHumidity=maxHumidity, minHumidity=minHumidity, maxGas=maxGas, minGas=minGas, maxLight=maxLight, minLight=minLight)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7770)
