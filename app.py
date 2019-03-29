from flask import Flask, render_template, url_for, jsonify
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

app = Flask(__name__)


@app.route("/data")
def data():
    return "hello world"


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    print(os.listdir("./static/data"))
    app.run(debug=True)
