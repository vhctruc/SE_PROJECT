#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import gzip
import collections
import pandas


# In[6]:


columns_ = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g'
]
meddra_all_label_se = pandas.read_table(r'D:\Medra\meddra_all_label_se.tsv', sep='\t', names=columns_)
meddra_all_label_se


# In[7]:


meddra_all_label_se['b'].nunique()


# In[7]:


drug_name = pandas.read_table(r'D:\Medra\drug_names.tsv', sep='\t')
drug_name


# In[ ]:


drug_name.to_csv(r'D:\Medra\side-effects.csv')


# In[2]:


def stitch_flat_to_pubchem(cid):
    assert cid.startswith('CID')
    return int(cid[3:]) - 1e8

def stitch_stereo_to_pubchem(cid):
    assert cid.startswith('CID')
    return int(cid[3:])


# In[2]:


# Read DrugBank terms
url = 'https://raw.githubusercontent.com/dhimmel/SIDER4/master/data/side-effects.tsv'
drugbank_df = pandas.read_table(url)

# Pubchem to DrugBank mapping
# url = 'https://raw.githubusercontent.com/dhimmel/drugbank/3e87872db5fca5ac427ce27464ab945c0ceb4ec6/data/mapping/pubchem.tsv'
# drugbank_map_df = pandas.read_table(url)


# In[3]:


drugbank_df


# In[4]:


drugbank_df.to_csv(r'D:\Side_Effect.csv')


# In[ ]:





# In[5]:


drugbank_map_df


# In[18]:


columns_ = [
    'drug_id',
    'drug_name'
]
drug_name = pandas.read_table(r'D:\Medra\drug_names.tsv', sep='\t', names=columns_)
drug_name


# In[14]:


columns = [
    'stitch_id_flat',
    'stitch_id_sterio',
    'umls_cui_from_label',
    'placebo',
    'frequency',
    'lower',
    'upper',
    'meddra_type',
    'umls_cui_from_meddra',
    'side_effect_name',
]
freq_df = pandas.read_table(r'D:\Medra\meddra_freq.tsv', sep='\t', names=columns)
freq_df


# In[13]:


freq_df.to_csv(r'D:\Medra\TEST.csv')


# In[11]:


columns = [
    'stitch_id_flat',
    'stitch_id_sterio',
    'umls_cui_from_label',
    'meddra_type',
    'umls_cui_from_meddra',
    'side_effect_name',
]
se_df = pandas.read_table(r'D:\Medra\meddra_all_se.tsv', sep='\t', names=columns)
# se_df['pubchem_id'] = se_df.stitch_id_sterio.map(stitch_stereo_to_pubchem)
# se_df = drugbank_map_df.merge(se_df)
se_df


# In[12]:


se_df.query("stitch_id_flat == 'CID100047725'")


# In[12]:


se_df = se_df[['drugbank_id', 'umls_cui_from_meddra', 'side_effect_name']]
se_df = se_df.dropna()
se_df = se_df.drop_duplicates(['drugbank_id', 'umls_cui_from_meddra'])
se_df = drugbank_df.merge(se_df)
se_df = se_df.sort_values(['drugbank_name', 'side_effect_name'])
len(se_df)


# In[14]:


se_terms_df = se_df[['umls_cui_from_meddra', 'side_effect_name']].drop_duplicates()
assert se_terms_df.side_effect_name.duplicated().sum() == 0
se_terms_df = se_terms_df.sort_values('side_effect_name')
se_terms_df.to_csv(r'D:\Medra\side-effect-terms.tsv', sep='\t', index=False)


# In[16]:


se_df.drugbank_id.nunique()


# In[17]:


se_df.umls_cui_from_meddra.nunique()


# In[19]:


# Save side effects
se_df.to_csv(r'D:\Medra\side-effects.tsv', sep='\t', index=False)


# In[32]:


check_ = pandas.read_table(r'D:\Medra\side-effects.tsv', sep='\t', header= None)
check_


# In[34]:


check_.rename(columns={ 
    check_.columns[0]: 'drugbank_id', 
    check_.columns[1]: 'drugbank_name', 
    check_.columns[2]: 'umls_cui_from_meddra',
    check_.columns[3]: 'side_effect_name'}, inplace = True)


# In[36]:


check_.to_csv(r'D:\Medra\side-effects.csv')


# In[37]:


columns = [
    'stitch_id_flat',
    'umls_cui_from_label',
    'method',
    'concept_name',
    'meddra_type',
    'umls_cui_from_meddra',
    'meddra_name',
]
indication_df = pandas.read_table(r'D:\Medra\meddra_all_indications.tsv', names=columns)
indication_df['pubchem_id'] = indication_df.stitch_id_flat.map(stitch_flat_to_pubchem)


# In[38]:


indication_df = drugbank_df.merge(drugbank_map_df.merge(indication_df))
indication_df = indication_df.query("meddra_type == 'PT'")
indication_df.head(2)


# In[39]:


# Multiple Sclerosis indications
indication_df.query("umls_cui_from_meddra == 'C0026769'").drugbank_name.tolist()


# In[46]:


df = pandas.DataFrame(indication_df)


# In[49]:


df


# In[50]:


indication_df


# In[51]:


indication_df.to_csv(r'D:\Medra\indications.tsv', sep='\t', index=False)


# In[52]:


check_1 = pandas.read_table(r'D:\Medra\indications.tsv', sep='\t', header= None)
check_1


# In[53]:


check_1.rename(columns={ 
    check_1.columns[0]: 'drugbank_id', 
    check_1.columns[1]: 'drugbank_name', 
    check_1.columns[2]: 'pubchem_id',
    check_1.columns[3]: 'stitch_id_flat',
    check_1.columns[4]: 'umls_cui_from_label',
    check_1.columns[5]: 'method',
    check_1.columns[6]: 'concept_name',
    check_1.columns[7]: 'meddra_type',
    check_1.columns[8]: 'umls_cui_from_meddra',
    check_1.columns[9]: 'meddra_name'}, inplace = True)


# In[54]:


check_1.to_csv(r'D:\Medra\indication_df.csv')

