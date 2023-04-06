#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

tess.pytesseract.tesseract_cmd= r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# In[2]:


url = "https://cdn.drugbank.vn/1555746490156_Nha%CC%83n%2094-1-205-217.pdf"
request = requests.get(url)
filestream = io.BytesIO(request.content)


# In[3]:


with fitz.open(stream=filestream, filetype="pdf") as doc:
    text = ""
    for page in doc:
        print(page)
        text = text + page.get_text()
df = pd.DataFrame(text.rstrip().split('\n'))
df.rename(columns={df.columns[0]: 'CRAWL'}, inplace = True)
filter_df = df.loc[df['CRAWL'].str.len() > 1]
filter_df = filter_df.reset_index()
filter_df = filter_df.drop(filter_df.columns[0], axis=1)
regex = re.compile("[,\.!?:*();%]")
REMOVE = []
for i in range(len(filter_df)):
    remove = unidecode(unidecode(regex.sub('',filter_df['CRAWL'][i]).strip().lower())).replace(' ','')
    REMOVE.append(remove)
filter_df['REMOVE'] = pd.DataFrame(REMOVE)
filter_df_RS = filter_df.loc[filter_df['REMOVE'] != 'dtqgvn2']
filter_df_RS


# In[20]:


filter_df_RS.to_excel('D:\SE\TEST_PDF.xlsx')

