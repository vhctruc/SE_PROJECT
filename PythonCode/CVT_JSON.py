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
from flatten_json import flatten
import json


# In[2]:


df = pd.read_excel(r'D:\compound_SE.xlsx')
sub_dict = {
    '&Agrave;' : 'À','&Otilde;' : 'Õ','&Ecirc;' : 'Ê','&ucirc;' : 'û','&Ocirc;' : 'Ô',
'&Aacute;' : 'Á','&Ouml;' : 'Ö','&Euml;' : 'Ë','&uuml;' : 'ü','&#149;' : '•',
'&Acirc;' : 'Â','&ograve;' : 'ò','&egrave;' : 'è','&#181;' : 'µ','&#153;' : '™',
'&Atilde;' : 'Ã','&oacute;' : 'ó','&eacute;' : 'é','&#215;' : '×','&copy;' : '©',
'&Auml;' : 'Ä','&ocirc;' : 'ô','&ecirc;' : 'ê','&Yacute;' : 'Ý','&reg;' : '®',
'&Aring;' : 'Å','&otilde;' : 'õ','&euml;' : 'ë','&#159;' : 'Ÿ','&#167;' : '§',
'&agrave;' : 'à','&ouml;' : 'ö','&#131;' : 'ƒ','&yacute;' : 'ý','&#182;' : '¶',
'&aacute;' : 'á','&Oslash;' : 'Ø','&Igrave;' : 'Ì','&yuml;' : 'ÿ',
'&acirc;' : 'â','&oslash;' : 'ø','&Iacute;' : 'Í','&#176;' : '°',
'&atilde;' : 'ã','&#140;' : 'Œ','&Icirc;' : 'Î','&#134;' : '†',
'&auml;' : 'ä','&#156;' : 'œ','&Iuml;' : 'Ï','&#135;' : '‡',
'&aring;' : 'å','&#138;' : 'Š','&igrave;' : 'ì','&lt;' : '<',
'&AElig;' : 'Æ','&#154;' : 'š','&iacute;' : 'í','&gt;' : '>',
'&aelig;' : 'æ','&Ugrave;' : 'Ù','&icirc;' : 'î','&#177;' : '±',
'&szlig;' : 'ß','&Uacute;' : 'Ú','&iuml;' : 'ï','&#171;' : '«',
'&Ccedil;' : 'Ç','&Ucirc;' : 'Û','&Ntilde;' : 'Ñ','&#187;' : '»',
'&ccedil;' : 'ç','&Uuml;' : 'Ü','&ntilde;' : 'ñ','&#191;' : '¿',
'&Egrave;' : 'È','&ugrave;' : 'ù','&Ograve;' : 'Ò','&#161;' : '¡',
'&Eacute;' : 'É','&uacute;' : 'ú','&Oacute;' : 'Ó','&#183;' : '·',
'&amp;' : '&','&lt;' : '<','&gt;' : '>','&nbsp;' : ' ','&le;' : '≤','&ge;' : '≥'
}

df['VALUE'] = df['VALUE'].replace(sub_dict,regex=True)
json_data = df['VALUE']
df


# In[3]:


df_all = pd.DataFrame()
for i in range(len(json_data)):
    try:
        json_object = json.loads(json_data[i])
        json_formatted_str = json.dumps(json_object, indent=2)
        df = pd.json_normalize(json.loads(json_formatted_str))
        df_all = pd.concat([df, df_all])
    except:
        continue
df_all


# In[4]:


filter_result = df_all[['slug', 'tac_dung_phu']].reset_index()
tac_dung_phu_clean = []
for i in range (len(filter_result['tac_dung_phu'])):
    final_result = re.sub("\n|\r|\t", "@",filter_result['tac_dung_phu'][i])
    tac_dung_phu_clean.append(final_result)
filter_result['tac_dung_phu_clean'] = pd.DataFrame(tac_dung_phu_clean)
filter_result


# In[13]:


a = '@' + filter_result['tac_dung_phu_clean']
a


# In[6]:


filter_result.to_excel(r'D:\TEST123.xlsx',sheet_name = 'TEST')

