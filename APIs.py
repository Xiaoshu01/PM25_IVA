# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 08:14:33 2019

@author: 73921

计算变量间的相关性
预测未来的PM2.5

"""
import pandas as pd
import json

def Load_data():
    data = pd.read_csv("total_clean_data.csv")
    
    return data

def savetocsv(data_df,file_name):
    """
    存成csv文件，有需要可以调用
    data_df:dataframe数据
    file_name:csv文件名
    """
    data_df.to_csv()
    
def savetojson(file_name,jfile_name):
    """
    存成json格式文件（既可以得到json文件也可以直接获得json数据）
    file_name:待转换文件名
    jfile_name:json文件名
    """
    fo = open(file_name, 'r')

    ls=[]
    for line in fo:
        line=line.replace("\n","")  #将换行换成空
        ls.append(line.split(","))  #以，为分隔符
    fo.close()  #关闭文件流
    fw=open(jfile_name,"w")  #打开json文件
    for i in range(1,len(ls)):  
        ls[i]=dict(zip(ls[0],ls[i]))  
    json.dump(ls[1:],fw,sort_keys=True,indent=4)

    fw.close()
    
    ###返回json数据
    with open(jfile_name, 'r') as f:
        jdata = json.loads(f.read())
    
    return jdata
    
    

def corr_var(city):
    """
    Calculate the correlation between variables and save as json
    city: the city which you want to calculate(Beijing,Shanghai,Chengdu,Guangzhou,Shenyang)
    """
    data = Load_data()
    data_city = data[data['city'] == city]
    data_city = data_city.drop(['Unnamed: 0','season','cbwd','city','date'], axis = 1)
    corr_city = data_city.corr()
    
    file_name = "corr_"+city+".csv"
    savetocsv(corr_city, file_name)
    
    ###存成csv文件
    corr_city.to_csv(file_name)

    ###存成json文件
    jfile_name = "corr_"+city+".json"
    jdata_city = savetojson(file_name,jfile_name)
    
    return corr_city

def main():
    corr_Beijing = corr_var("Beijing")
    corr_Shanghai = corr_var("Shanghai")
    corr_Chengdu = corr_var("Chengdu")
    corr_Guangzhou = corr_var("Guangzhou")
    corr_Shenyang = corr_var("Shengyang")
    
if __name__ == '__main__':
    main()

    