#!/usr/bin/env python
# coding: utf-8

# # Segmenting and Clustering Neighborhoods in Toronto

# # Installing and importing the useful libraries

# In[56]:


get_ipython().system('pip install folium')


# In[4]:


get_ipython().system('pip install geopy')


# In[5]:


import numpy as np # library to handle data in a vectorized manner

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json # library to handle JSON files

#!conda install -c conda-forge geopy --yes # uncomment this line if you haven't completed the Foursquare API lab
from geopy.geocoders import Nominatim # convert an address into latitude and longitude values

import requests # library to handle requests
from pandas.io.json import json_normalize # tranform JSON file into a pandas dataframe

# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors

# import k-means from clustering stage
from sklearn.cluster import KMeans

#!conda install -c conda-forge folium=0.5.0 --yes # uncomment this line if you haven't completed the Foursquare API lab
import folium # map rendering library

print('Libraries imported.')


# # Scrapping the datasets from the web

# In[24]:


import requests
import lxml.html as lh
import pandas as pd


# In[25]:


#Scrape the table cells

url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
#Create a handle, page, to handle the contents of the website
page = requests.get(url)
#Store the contents of the website under doc
doc = lh.fromstring(page.content)
#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')


# In[26]:


#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]


# In[27]:



# Parse the first row as our header
tr_elements = doc.xpath('//tr')

#Create empty list
col=[]
i=0

#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))


# # Creating the dataframe 

# In[34]:


#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 10, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


# In[57]:


#The size of the dataframe


# In[58]:


[len(C) for (title,C) in col]


# In[59]:


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)


# In[37]:


df.head()


# # Transforming the data into pandas dataframe

# To create the above dataframe:
# 
# The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
# 
# Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.
# 
# More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: 
# Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table.
# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. So for the 9th cell in the table on the Wikipedia page, the value of the Borough and the Neighborhood columns will be Queen's Park.
# Clean your Notebook and add Markdown cells to explain your work and any assumptions you are making.
# In the last cell of your notebook, use the .shape method to print the number of rows of your dataframe.

# # Rearranging and renaming the column

# In[69]:


df.columns = ['Borough', 'Neighbourhood','Postcode']

cols = df.columns.tolist()
cols


# In[70]:


cols = cols[-1:] + cols[:-1]
cols
df = df[cols]
df.head()


# In[71]:


df = df.replace('\n',' ', regex=True)
df.head()


#  **Droppig the cells in the Borough which are not assigned**

# In[72]:


df.drop(df.index[df['Borough'] == 'Not assigned'], inplace = True)

# Reset the index and dropping the previous index
df = df.reset_index(drop=True)

df.head(10)


# In[73]:


df = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(','.join).reset_index()
df.columns = ['Postcode','Borough','Neighbourhood']
df.head(10)


# In[74]:


df['Neighbourhood'] = df['Neighbourhood'].str.strip()


# In[75]:


df.loc[df['Neighbourhood'] == 'Not assigned', 'Neighbourhood'] = df['Borough']


# In[76]:


# Check if the Neighbourhood for Queen's Park changed 
df[df['Borough'] == 'Queen\'s Park']


# In[77]:


df.shape


# **The total number of rows are 210**
