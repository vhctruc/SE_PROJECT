#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


url = 'https://cdn.nhathuoclongchau.com.vn/unsafe/fit-in/1200x1200/filters:quality(100):fill(white)/nhathuoclongchau.com.vn/images/product/2022/12/00014354-nolvadex-d-1516-63aa_large.jpg'
response = requests.get(url)


# In[3]:


path = Image.open(BytesIO(response.content))
path


# In[4]:


text= tess.image_to_string(path, lang='vie')
print(text)

