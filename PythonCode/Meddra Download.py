#!/usr/bin/env python
# coding: utf-8

# In[1]:


# %load dic_reading.py
import pickle
import numpy as np
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import glob
from tqdm import tqdm
import itertools

from datetime import date, datetime

# se_dic = pickle.load(open('../Data/curated/AE_dic.pk', 'rb'))
# drug_dic = pickle.load(open('../Data/curated/drug_mapping.pk', 'rb'))

# # In this MeDRA_dic, key is string of PT_name, value is a list:
# # [PT, PT_name, HLT,HLT_name,HLGT,HLGT_name,SOC,SOC_name,SOC_abbr]
# meddra_pd_all = pickle.load(open('../Data/curated/AE_mapping.pk', 'rb'))


# In[2]:


# initial setup
def date_normalize(formate, dat): 
    stand_date = date(2000, 1, 1)
    if formate=='102':  # the date is formed as yyyymmdd
        current_date = date(int(dat[:4]), int(dat[4:6]), int(dat[6:8])) 
    elif formate=='610':  # formed as yyyymm
        current_date = date(int(dat[:4]), int(dat[4:6]), 1)
    elif formate=='602':  #formed as yyyy
        current_date = date(int(dat[:4]), 1, 1)
    delta = current_date - stand_date
    return delta.days

def days_to_date(days):
    stand_date = date(2000, 1, 1)

    if int(days)<0:
        days = 1
    
    dt = datetime.fromordinal(int(days))
    return dt.strftime('%Y-%m-%d')


# In[6]:


# initial setup
def date_normalize(formate, dat): 
    stand_date = date(2000, 1, 1)
    if formate=='102':  # the date is formed as yyyymmdd
        current_date = date(int(dat[:4]), int(dat[4:6]), int(dat[6:8])) 
    elif formate=='610':  # formed as yyyymm  
        current_date = date(int(dat[:4]), int(dat[4:6]), 1)
    elif formate=='602':  #formed as yyyy      
        current_date = date(int(dat[:4]), 1, 1)
    delta = current_date - stand_date
    return delta.days

n_reports = []
miss_count = {}
# To save time, parse 2018-2018  in the first round, then 2018-2021
for yr in range(2013, 2023):

    if yr == 2020:
        qtr_list = [1, 2, 3]
#         qtr_list = [3]
    else:
        qtr_list=[1,2,3,4]
    for qtr in qtr_list:
        qtr_name = str(yr)+'q'+ str(qtr)
        print('I am parsing:',qtr_name)
        
#         """Read data from lab storage""" 
#         /n/data1/hms/dbmi/zitnik/lab/datasets/2020-08-FAERS/
        lab_storage = 'D:/Medra/faers_xml_2022Q4/TEST'

#         files = lab_storage + qtr_name + '/**/**'
        xml_files = glob.glob(lab_storage +"/*.xml", recursive=True)
        unique_files = list(set(xml_files))  # only keep the unique values, remove duplicated files.
        xml_files = unique_files
        xml_files.sort()
        print('find {} files'.format(len(xml_files)))
        print(xml_files)


# In[7]:


root = None
for xml_file in xml_files:
    print(xml_file)
    data = ET.parse(xml_file).getroot()
    if root is None:
        root = data
    else:
        root.extend(data)
        print('finished merge',xml_file)
nmb_reports = len(root)
print(nmb_reports)

count = 0
patient_ID = 0
dic = {}

miss_admin = miss_patient = miss_reaction = miss_drug =0


# In[8]:


for report in tqdm(root.findall('safetyreport')):
    """Administrative Information"""
#             report.find('').text
    try:  # Mandatory Information: report_id
        try:
            version = report.find('safetyreportversion').text
        except:
            version = '1'
            
        report_id = report.find('safetyreportid').text
        
        try:
            case_id = report.find('companynumb').text
        except:
            case_id = '0'  # unknown case id
            
        try:
            country = report.find('primarysource')[0].text
        except:
            country = 'unknown'          

            
        if country =='COUNTRY NOT SPECIFIED':
            country = 'unknown'
            
            
        try:
            qualify = report.find('primarysource')[1].text
        except:
            qualify = '6'  # the qualify is unknown
            
#                 qualify = report.find('primarysource')[1].text
            
        if qualify not in {'1', '2', '3', '4', '5', '6','7'}:
            qualify = '0'
                              
            
        try:
            serious = report.find('serious').text
        except:
            serious = '-1'
        
        try:
            s_1 = report.find('seriousnessdeath').text
        except:
            s_1 = '0'
        try:
            s_2 = report.find('seriousnesslifethreatening').text
        except:
            s_2 = '0'
        try:
            s_3 = report.find('seriousnesshospitalization').text
        except:
            s_3 = '0'
        try:
            s_4 = report.find('seriousnessdisabling').text
        except:
            s_4 = '0'
        try:
            s_5 = report.find('seriousnesscongenitalanomali').text
        except:
            s_5 = '0'
        try:
            s_6 = report.find('seriousnessother').text
        except:
            s_6 = '0'
        serious_subtype = [s_1, s_2, s_3, s_4, s_5, s_6]
    except:
        miss_admin +=1
        continue

    try:  # Optional information
        # receivedate: Date when the report was the FIRST received
        receivedateformat, receivedate = report.find('receivedateformat').text, report.find('receivedate').text
        receivedate = date_normalize(receivedateformat, receivedate)
    except:
        receivedate = '0'
    
    try:
        # receiptdate: Date of most RECENT report received
        receiptdateformat, receiptdate = report.find('receiptdateformat').text, report.find('receiptdate').text
        receiptdate = date_normalize(receiptdateformat, receiptdate)
    except:
         receiptdate =  '0'

    for patient in report.findall('patient'):
        """Demographic Information"""                
        try:
            age = patient.find('patientonsetage').text
        except:
            age = -1 # unknown age
        try:
            ageunit = patient.find('patientonsetageunit').text
        except:
            ageunit = '801' 
        # normalize age
        try:
            age = int(age)  
            if age!= -1:
                if ageunit == '800':  # Decade 
                    age = '-1'
                elif ageunit == '801':  # Year
                    age = age
                elif ageunit == '802':  # Month
                    age = int(age/12)
                elif ageunit == '803':  # Week
                    age = int(age/52)
                elif ageunit == '804':  # Day
                    age = int(age/365)
                elif ageunit == '805':  # Hour
                    age = int(age/(24*365))
    #                     else:
    #                         age = '-1'  # unknown age
        except:
            age = -1
            
              
        try:
            gender = patient.find('patientsex').text
        except:
            gender = '0'
        try:
            weight = patient.find('patientweight').text
        except:
            weight = '0'
        ## Nothing is mandatory
#                 if age == -1 and gender== '0':  # Mandatory: if age & gender both missing, ignore this report.
#                     miss_patient +=1
#                     continue

        reaction_list = []
        for side_ in patient.findall('reaction'):
            try:  # outcome: 1-6, 6 levels in total
                try: 
                    PT_code = side_[0].text
                except:
                    PT_code = '0'
                try:
                    outcome = side_[2].text
                except:
                    outcome = '6'
                try:
                    PT = side_[1].text
                except:
                    PT = 'none'
                reaction = [PT_code, PT, outcome]
            except:
                continue
            reaction_list.append(reaction) 
        if reaction_list.__len__() == 0:  # Mandatory condition: at least has one reaction
            miss_reaction += 1
            continue

        drug_list = []
        for drug_ in patient.findall('drug'):
            try:
                try:
                    char =  drug_.find('drugcharacterization').text  # drugcharacterization: 1(suspect)/2(concomitant)/3(interacting)
                except:
                    char = '0'
                try:
                    product =  drug_.find('medicinalproduct').text  # drug brand
                except:
                    product = 'none'
                """Dosage are generally fixed according to the indication"""
                try: 
                    dorse, unit=  drug_.find('drugstructuredosagenumb').text, drug_.find('drugstructuredosageunit').text
                    drugseparatedosagenumb, drugintervaldosageunitnumb, drugintervaldosagedefinition = \
                        drug_.find('drugseparatedosagenumb').text, drug_.find('drugintervaldosageunitnumb').text, \
                        drug_.find('drugintervaldosagedefinition').text
                    form = drug_.find('drugdosageform').text  # tablet or capsule or sth 
                except:
                    dorse, unit, drugseparatedosagenumb,drugintervaldosageunitnumb, drugintervaldosagedefinition, form =\
                    '0', '0', '0','0','0', '0'
                try:
                    route = drug_.find('drugadministrationroute').text
                    if route == '048':
                        route = '1'  # oral 
                    elif route == '061':
                        route = '2'  # Topical
                except:
                    route = '0'  # no information of route
                
                try:
                    indication = drug_.find('drugindication').text  # indication (disease): super important
                except:
                    indication = 'none'

                try:
                    start_format, start_date = drug_.find('drugstartdateformat').text, drug_.find('drugstartdate').text
                    start_date = date_normalize(start_format, start_date)
                except:
                    start_date = '0'
                try:
                    end_format, end_date = drug_.find('drugenddateformat').text, drug_.find('drugenddate').text
                    end_date = date_normalize(end_format, end_date)
                except:
                    try:
                        end_date = receiptdate
                    except:
                        end_date = '0'
                    
                try:
                    action = drug_.find('actiondrug').text
                except:
                    action = '5'
                try:
                    additional = drug_.find('drugadditional').text
                except:
                    additional = '3'
                try:
                    readm = drug_.find('drugrecurreadministration').text
                except:
                    readm = '3'
                try:
                    substance = drug_.find('activesubstance')[0].text
                except:
                    substance = 'none'
            except:  # Mandatory condition: if none of the above information is provided, ignore this report
                continue
            drug = [char, product, dorse, unit, drugseparatedosagenumb, drugintervaldosageunitnumb,
                    drugintervaldosagedefinition, form, route, indication, start_date, end_date, action,
                    readm, additional, substance]
            drug_list.append(drug)
        if drug_list.__len__() ==0:
            miss_drug += 1
            continue

        """for patient_ID"""
        dic[count] = [version, report_id, case_id, country, qualify, serious, 
                      s_1, s_2, s_3, s_4, s_5, s_6, 
                      receivedate, receiptdate,  
                      age, gender, weight, reaction_list, drug_list]
        count += 1

pickle.dump(dic, open('D:/Medra/faers_xml_2022Q4/XML/'+ qtr_name+'.pk', 'wb'))

n_reports.append(len(dic))
print(qtr_name+' file saved. with', len(dic), 'reports')
miss_count[qtr_name] = [nmb_reports, miss_admin, miss_patient, miss_reaction, miss_drug]

print ('All data saved')


# In[9]:


# check the number of reports in 2019 Q4
sep_2020 =pickle.load(open('D:/Medra/faers_xml_2022Q4/XML/2022q4.pk', 'rb'))
len(sep_2020)


# In[10]:


reports_pd = pd.DataFrame(sep_2020.values(), 
                          columns=['version','report_id','case_id','country','qualify','serious',
                                   's1','s2','s3','s4','s5','s6','receivedate','receiptdate',
                                   'age','gender','weight','SE','drugs'])


# In[11]:


df = reports_pd.head(1000)


# In[13]:


df.to_csv(r'D:/Medra/faers_xml_2022Q4/XML/TEST.csv')


# In[17]:


df1 = df['drugs']


# In[19]:


df2 = pd.DataFrame([df1])


# In[21]:


df2


# In[20]:


df2.columns =['col1','col2','col3']
df2

