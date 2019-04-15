# -*- coding: utf-8 -*-
"""
Copyright : (c) 04/14/2019 by Yan Xiaoshu.
------------------------------------------------------------------------------------------------------------------------
base information :
File Name       : app.py
Description     : The Visualization of PM2.5 of the Five Chiniese Cities
@Co-Author      : Yan Xiaoshu, Liu Wei, Ren Qianru.
Version         : via-pm25-01

Change Activity :
Date    : 2019/4/14
Author  : Yan Xiaoshu
Content : Create the handle function
------------------------------------------------------------------------------------------------------------------------
"""

from flask import Flask, render_template, url_for, jsonify, request
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/city", methods=['GET', 'POST'])
def city():
    """return the PM  and other meteorological value according to the city name.
    :param city_name: include five cities : Beijing、Chengdu、Guangzhou、Shanghai、Shenyang, the city name can
                      use a mixture of uppercase and lowercase.
    :return: a list of average quarterly PM and other meteorological value.
    """
    city_name = request.values.get("city_name")
    df = pd.read_csv("pm2aqi.csv")
    data1 = df[df.city == city_name][['date', 'PM2.5']]

    return jsonify(data1.values.tolist())


@app.route("/corr", methods=['GET', 'POST'])
def corr():
    """return the pc matrix of the 8 meteorological values according to the time range and city name.
    :param start: the start time
    :param end: the end time
    :return: a 8*8 matrix of meteorological value.
    """
    city_name = request.values.get("city_name")
    start = request.values.get("start")
    end = request.values.get("end")
    print(city_name)
    print(start)
    print(end)

    df = pd.read_csv("corr.csv")
    df['date'] = pd.to_datetime(df['date'], format="%Y%m%d")  # 将数据类型转换为日期类型
    df = df.set_index('date', drop=True)  # 将时间作为索引
    df = df[start:end]
    data1 = df[df.city == city_name][['PM2.5', 'DEWP', 'HUMI', 'PRES', 'TEMP', 'Iws']]
    data1 = np.fabs(np.array(data1.corr()).round(2))
    print(type(data1))
    data = []
    for i in range(0, len(data1)):
        for j in range(0, len(data1)):
            data.append([i, j, data1[i, j]])

    return jsonify(data)


@app.route("/default_corr", methods=['GET', 'POST'])
def default_corr():
    """return the pc matrix of the 8 meteorological values according to the whole time and city name.
    :param start: the start time
    :param end: the end time
    :return: a 8*8 matrix of meteorological value.
    """
    city_name = request.values.get("city_name")
    df = pd.read_csv("corr.csv")
    data1 = df[df.city == city_name][['PM2.5', 'DEWP', 'HUMI', 'PRES', 'TEMP', 'Iws']]
    data1 = np.fabs(np.array(data1.corr()).round(2))
    data = []
    for i in range(0, len(data1)):
        for j in range(0, len(data1)):
            data.append([i, j, data1[i, j]])

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)  # run in the debug mod.
