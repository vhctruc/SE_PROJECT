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


# In[2]:


df = pd.read_excel(r'E:\Compound.xlsx')


# In[3]:


df


# In[4]:


def dic_(value):
    x = value.replace(" ", "")
    dictionary = "A aB bC cD dE εeF fG gH hI iJ jK kL lM mN nO oP pQ qR rS sT tU uV vW wXä xY^ yZ~<> –z ±*%.α-−()0123456789,[]/\''{}:;,+-ωδψγ→β"
    y = dictionary.replace(" ", "")
    k = 0
    txt = ''
    z=0
    for i in range(len(x)):
        if txt.find(y[z]) == 0:
            k = k + 1
        for z in range(len(y)):
            txt = x[i]
            char = y[z]
            if txt.find(y[z]) == 0:
#                 print(x[i],i,txt.find(y[z]))
                break
#     print(k)
#     print(len(x))
    if (k+1) < len(x):
#         print("No")
        return 'No'
    else:
#         print("Yes")
        return 'Yes'


# In[34]:


# message = "Arg34Lys26-(N-ε-(γ-Glu(N-α-hexadecanoyl)))-GLP-1[7-37]"
# print(message,(dic_(message)))


# In[5]:


NAME = []
FLAG = []
for i in range(len(df['Name'])):
    message = df['Name'][i]
    NAME.append(message)
    FLAG.append(dic_(message))


# In[6]:


df['FLAG'] = pd.DataFrame(FLAG)


# In[7]:


df


# In[8]:


df.to_excel(r'E:\Compound_Re.xlsx')

