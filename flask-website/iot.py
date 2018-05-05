from flask import Flask, g, render_template
import csv
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as md
import numpy as np
import datetime

app = Flask(__name__)

"""
Reads the data out of the CSV file. CSV file is formatted as
timestamp, temperature, humidity, gas.
"""
def readData():
    with open('data.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        timestamps = []
        temps = []
        humids = []
        gases = []
        for row in reader:
            timestamps.append(int(row[0]))
            temps.append(int(row[1]))
            humids.append(int(row[2]))
            gases.append(int(row[3]))

    return timestamps, temps, humids, gases


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


def generateGraphs(dates, temps, humids, gases):
    generateTempGraph(dates, temps)
    plt.clf() # Clear figure
    generateHumidGraph(dates, humids)
    plt.clf()
    generateGasesGraph(dates, gases)

@app.route('/')
def main_page():
    times, temps, humids, gases = readData()
    dates = [datetime.datetime.fromtimestamp(ts) for ts in times]
    generateGraphs(dates, temps, humids, gases)

    maxTemp = max(temps)
    minTemp = min(temps)

    maxHumidity = max(humids)
    minHumidity = min(humids)

    maxGas = max(gases)
    minGas = min(gases)

    return render_template('main_page.html', maxTemp=maxTemp, minTemp=minTemp, maxHumidity=maxHumidity, minHumidity=minHumidity, maxGas=maxGas, minGas=minGas)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
