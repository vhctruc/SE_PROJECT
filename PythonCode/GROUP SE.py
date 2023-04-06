#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import Counter
import requests
import io
from PIL import Image
import requests
from io import BytesIO
from tika import parser
import pandas as pd
import numpy as np
import urllib
import pyodbc
import sqlalchemy as sa
import math
import fitz
import re, sys, unicodedata
import csv
import gzip
import collections
import xml.etree.ElementTree as ET
from unidecode import unidecode
import os
from PyPDF2 import PdfFileMerger
import urllib.request
import pytesseract as tess
from PIL import Image
stripJunk = str.maketrans("","","- ")


# In[2]:


df = pd.read_excel(r'D:\SE\TEST.xlsx',dtype=object)
df = df.replace({ '–' : ' ', '-' : ' '}, regex=True)
data = df['Group_SideEffect_Name']
data


# In[3]:


def getRatio(a,b):
    a = a.lower().translate(stripJunk)
    b = b.lower().translate(stripJunk)
    total  = len(a)+len(b)
    counts = (Counter(a)-Counter(b))+(Counter(b)-Counter(a))
    return 100 - 100 * sum(counts.values()) / total
def dedup(value):
    words = set(value.split(' '))
    return ' '.join(words)


# In[16]:


treshold     = 75
minGroupSize = 1

from itertools import combinations

paired = { c:{c} for c in data }
for a,b in combinations(data,2):
    if getRatio(a,b) < treshold: continue
    paired[a].add(b)
    paired[b].add(a)

groups    = list()
ungrouped = set(data)
while ungrouped:
    bestGroup = {}
    for city in ungrouped:
        g = paired[city] & ungrouped
        for c in g.copy():
            g &= paired[c] 
        if len(g) > len(bestGroup):
            bestGroup = g
    if len(bestGroup) < minGroupSize : break  # to terminate grouping early change minGroupSize to 3
    ungrouped -= bestGroup
    groups.append(bestGroup)


# In[17]:


result = pd.DataFrame(groups)


# In[20]:


result


# In[21]:


result = pd.DataFrame(groups)
result.fillna("ức chế tủy xương nặngaa",inplace=True)
result = result.replace('   ','  ')


# In[22]:


result = result.replace('  ',' ')
# result['concatenated'] = result.apply(lambda x: ','.join(x.astype(str)), axis=1)
result


# In[32]:


# DEDUP_ = []
# for i in range(len(result)):
#     DEDUP = dedup(result['concatenated'][i]).strip().replace('  ',' ')
#     DEDUP_.append(DEDUP)


# In[35]:


# result['dedup'] = pd.DataFrame(DEDUP_)


# In[23]:


result['min_group'] = result.min(axis=1)
result = result.replace('ức chế tủy xương nặngaa','')
result


# In[24]:


result.to_excel(r'D:\SE\SE_GROUP.xlsx')


# In[ ]:





# In[ ]:




