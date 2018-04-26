from flask import Flask, g, render_template
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

"""
Function generating the graph to be displayed on the website.

Currently draws a simple plot taken from matplotlib tutorial
https://matplotlib.org/gallery/lines_bars_and_markers/simple_plot.html
"""
def generateGraph():
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
            title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig('static/graph.png')


@app.route('/')
def main_page():
    generateGraph()

    return render_template('main_page.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
