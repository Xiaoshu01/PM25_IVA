# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 10:33:32 2019

@author: 73921

save data as json form
"""

import csv
import json

file_name = "total_clean_data.csv"

fo = open(file_name, 'r')

ls=[]
for line in fo:
    line=line.replace("\n","")  #将换行换成空
    ls.append(line.split(","))  #以，为分隔符
fo.close()  #关闭文件流
fw=open("clean_data.json","w")  #打开json文件
for i in range(1,len(ls)):  
    ls[i]=dict(zip(ls[0],ls[i]))  
json.dump(ls[1:],fw,sort_keys=True,indent=4)

fw.close()
