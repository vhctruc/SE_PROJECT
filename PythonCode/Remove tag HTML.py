#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re
import pandas as pd
import io
from math import sin, cos, sqrt, atan2, radians
from math import radians, cos, sin, asin, sqrt
import matplotlib.pyplot as plt
from csv import reader
import sys
from bs4 import BeautifulSoup


# In[2]:


df = pd.read_excel(r'D:\compound_SE.xlsx')
df


# In[3]:


df.rename(columns={ df.columns[0]: 'NAME', df.columns[2]: 'VALUE'}, inplace = True)
sub_dict = {
    '&agrave;' : 'à','&aacute;' : 'á','&acirc;' : 'â','&atilde;' : 'ã','&auml;' : 'ä','&aring;' : 'å','&aelig;' : 'æ',
    '&szlig;' : 'ß','&ccedil;' : 'ç','&egrave;' : 'è','&eacute;' : 'é','&ecirc;' : 'ê','&euml;' : 'ë','&#131;' : 'ƒ',
    '&igrave;' : 'ì','&iacute;' : 'í','&icirc;' : 'î','&iuml;' : 'ï','&ntilde;' : 'ñ','&ograve;' : 'ò','&oacute;' : 'ó',
    '&ocirc;' : 'ô','&otilde;' : 'õ','&ouml;' : 'ö','&oslash;' : 'ø','&#140;' : 'œ','&#156;' : 'œ','&#138;' : 'š','&#154;' : 'š',
    '&ugrave;' : 'ù','&uacute;' : 'ú','&ucirc;' : 'û','&uuml;' : 'ü','&#181;' : 'µ','&#215;' : '×','&yacute;' : 'ý','&#159;' : 'ÿ',
    '&yuml;' : 'ÿ','&#176;' : '°','&#134;' : '†','&#135;' : '‡','&lt;' : '<','&gt;' : '>','&#177;' : '±','&#171;' : '«','&#187;' : '»',
    '&#191;' : '¿','&#161;' : '¡','&#183;' : '·','&#149;' : '•','&#153;' : '™','&copy;' : '©','&reg;' : '®','&#167;' : '§;','&#182;' : '¶',
    '&ge;':'>=', '&nbsp' : ' '
}

df['VALUE']=df['VALUE'].replace(sub_dict,regex=True)
df


# In[4]:


a = df['VALUE']


# In[6]:


CustomValue = []
for i in range(len(a)):
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    html = a[i]
    cleantext = re.sub(CLEANR, '', html)
    CustomValue.append(cleantext)
    df = pd.read_csv(io.StringIO(cleantext), sep=";", header = None)
    print(df)
print(CustomValue)


# In[7]:


a = pd.DataFrame(CustomValue)


# In[8]:


a


# In[9]:


a.to_excel(r'D:\TEST123.xlsx',sheet_name = 'TEST')

