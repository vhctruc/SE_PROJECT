#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re, sys, unicodedata
import csv
import gzip
import collections
import numpy as np
import urllib
import pyodbc
import pandas as pd
import sqlalchemy as sa
import numpy as np
import math
import xml.etree.ElementTree as ET
import pandas as pd
from unidecode import unidecode

connection_string = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'SERVER=118.69.201.34;'
    'Database=FLC_SHOP_SALES_DATAWAREHOUSE;'
    'UID=ecom_user;'
    'PWD=Ec0m@12345;'
    'Trusted_Connection=no;'
)

connection_uri = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(str(connection_string))}"
engine = sa.create_engine(connection_uri, fast_executemany=True)


# In[2]:


df = pd.read_excel(r'D:\TEST123.xlsx')
df


# In[11]:


# df.rename(columns={ df.columns[0]: 'NAME'}, inplace = True)
# remove = []
# regex = re.compile("[,\.!?:*();%]")
# for i in range(len(Apply)):
#     result_remove = unidecode(unidecode(regex.sub('',Apply[i]).strip().lower()))
#     remove.append(result_remove)
# df['REMOVE'] = pd.DataFrame(remove)
# df.to_excel(r'E:\Remove_Final.xlsx')


# In[3]:


def flatten_2_level_array(arr):
    flattened = []
    for sub_arr in arr:
        for item in sub_arr:
            flattened.append(item)
    return flattened
def findall(f, s):
    l = []
    i = -1
    while True:
        i = s.find(f, i+1)
        if i == -1:
            return l
        l.append(s.find(f, i))
# def processString6(txt):
#     dictionary = {' và': ',' , 'hoặc': ',', 'có thể': ','}
#     pattern = re.compile('|'.join(sorted(dictionary.keys(), key=len, reverse=True)))
#     result = pattern.sub(lambda x: dictionary[x.group()], txt)
#     return result


# In[4]:


a = '@' + df['tac_dung_phu_clean']
a


# In[5]:


cp = df['slug']
cp


# In[6]:


ComPound = []
RS_raw = []
RS_remove = []
C_SPACE = []

for i in range(len(a)):
    Compound = cp[i]
    string = a[i]
    indexes = [i for i, c in enumerate(string) if c == ',' or c == '.' or c == ';' or c == '@' or c == ':']
    print(indexes)
    if len(indexes) > 1:
        k = 0
        regex = re.compile("[,\.!?:*();%]")
        for i in range(len(indexes)-1):
            b = k + indexes[i+1]
            result_raw = regex.sub('',string[indexes[i]:b]).strip().lower()
            result_remove = unidecode(unidecode(regex.sub('',string[indexes[i]:b]).strip().lower()))
            if result_raw != '':
                ComPound.append(Compound)
                C_SPACE.append(result_raw.count(' '))
                RS_remove.append(result_remove)
                RS_raw.append(result_raw)
                print(Compound)
                print(result_remove)
                print(result_raw)
                print(result_raw.strip().count(' '))
print(len(RS_remove))
print(len(RS_raw))
print(len(C_SPACE))


# In[7]:


df = pd.DataFrame(RS_remove)
df['COMPOUND'] = pd.DataFrame(ComPound)
df['RAW'] = pd.DataFrame(RS_raw)
df['C_SPACE'] = pd.DataFrame(C_SPACE)


# In[8]:


df.rename(columns={ df.columns[0]: 'REMOVE'}, inplace = True)


# In[9]:


df


# In[11]:


df.to_excel(r'D:\Compound_Result_Re_2.xlsx')

