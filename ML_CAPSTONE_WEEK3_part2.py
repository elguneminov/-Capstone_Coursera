#!/usr/bin/env python
# coding: utf-8

# **Importing the useful libraries**

# In[1]:


import pandas as pd # library for data analsysis
import numpy as np # library to handle data in a vectorized manner

link = "http://cocl.us/Geospatial_data"
df1 = pd.read_csv(link)

df1.head()


# In[2]:


df1.shape


# In[3]:


df1.columns = ['Postcode','Latitude','Longitude']

cols = df1.columns.tolist()
cols


# In[4]:


link = "https://raw.githubusercontent.com/Shekhar-rv/Coursera_Capstone/master/df_can.csv"
df = pd.read_csv(link,index_col=0)
df.head()


# **Merging the two dataframes**

# In[5]:


df_new = pd.merge(df, df1, on='Postcode')
df_new.head()


# In[6]:


df_new.to_csv(r'df_final.csv')

