# -*- coding: utf-8 -*-
"""
Description      : Transfer the PM to AQI(Air Quality Index) value
Author           : Yan Xiaoshu
Last update date : 04/14/2019
"""
import pandas as pd
import numpy as np
import time
import os


def pm_to_aqi():
    """Transfer the pm value to aqi
    :return:a csv file include city, date, PM2.5, AQI columns.
    """
    df = pd.read_csv("./static/data/total_clean_data.csv")
    # 将时间转换为%Y%m%d格式
    df.date = df.date.apply(lambda x: time.strftime("%Y%m%d", time.strptime(x, "%Y-%m-%d-%H")))
    print(df.date.head(5))
    df.set_index('date', drop=True)

    data1 = pd.DataFrame(df['PM2.5'].groupby([df['city'], df['date']]).mean())
    data1['AQI'] = ((500 - 400) / (500 - 350)) * (data1[['PM2.5']].values) + 400
    # data1_date = data1[['PM2.5']].index
    # data1_pm = data1[['PM2.5']].values
    return data1.to_csv('{}.csv'.format("pm2aqi"), encoding="utf8")


def corr():
    """pc of the six elements: 'PM2.5', 'DEWP', 'HUMI', 'PRES', 'TEMP', 'Iws'.
    :return:a csv file include city, date, AQI, and other six columns.
    """
    df = pd.read_csv("./static/data/total_clean_data.csv")
    # 将时间转换为%Y%m%d格式
    df.date = df.date.apply(lambda x: time.strftime("%Y%m%d", time.strptime(x, "%Y-%m-%d-%H")))
    print(df.date.head(5))
    df.set_index('date', drop=True)
    num_agg = {'PM2.5': ['mean'], 'DEWP': ['mean'], 'HUMI': ['mean'], 'PRES': ['mean'], 'TEMP': ['mean'],
               'Iws': ['mean']}
    data1 = pd.DataFrame(df.groupby([df['city'], df['date']]).agg(num_agg))
    data1['AQI'] = ((500 - 400) / (500 - 350)) * (data1[['PM2.5']].values) + 400
    return data1.to_csv('{}.csv'.format("corr"), encoding="utf8")


if __name__ == '__main__':
    pm_to_aqi()
    corr()
