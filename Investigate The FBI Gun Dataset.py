#!/usr/bin/env python
# coding: utf-8

# # Investigate The FBI Gun Dataset
# 
# ## Table of content
# <ul>
#     <li><a href="#Introduction">Introduction</a></li>
#      <li><a href="#Data Wrangling">Data Wrangling</a></li>
#      <li><a href="#Exploratory Data Analysis">Exploratory Data Analysis</a></li>
#      <li><a href="#Conclusions">Conclusions</a></li>
# </ul>

# <a id="Introduction"></a>
# ## Introduction
# 
# > **Key notes**: The data comes from the FBI's National Instant Criminal Background Check System. The NICS is used by to determine whether a prospective buyer is eligible to buy firearms or explosives. Gun shops call into this system to ensure that each customer does not have a criminal record or isn’t otherwise ineligible to make a purchase. The data has been supplemented with state level data from [census.gov](https://www.census.gov/).
# 
# > The NICS data is found in one sheet of an .xlsx file. It contains the number of firearm checks by month, state, and type.
# 
# > The U.S. census data is found in a .csv file. It contains several variables at the state level. Most variables just have one data point per state (2016), but a few have data for more than one year.
# 
# > **Questions to explore**: 
# ><ol>
# ><li><a href="#q1">  The highest purchages record happened in which state for the persons under 18 years, percent on April 1, 2010?</a></li>
# ><li><a href="#q2">  What census data is most associated with high gun per capita?</a></li>
# ><li><a href="#q3">  Which states have had the highest growth in gun registrations?</a></li>
# ><li><a href="#q4">  What is the overall trend of gun purchases?</a></li>
# ><li><a href="#q5">  What type of gun has highest quantity, and the relationship to totals?</a></li>
# ><li><a href="#q6">  What is the sum of registered gun in each state over time?</a></li>
# </ol>

# In[98]:


#Set up import statment for all packages that are planed to use.
#Include a 'magic word' so that the visulaisations are polted.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='Data Wrangling'></a>
# ## Data Wrangling
# **This section contains the following:**
# ><ul>
# ><li>Loading the data.</li>
# ><li>Exploring the data general properties.</li>
# ><li>Trim and clean the dataset for analysis.</li>
# ></ul>    

# In[99]:


#Loading the data into the DataFarme.
df =pd.read_csv("U.S. Census Data.csv",sep=',')
df1 =pd.read_csv("gun_data.csv",sep=',')


# ### U.S. Census Data:

# In[100]:


#call on datafame to display a few rows.
df.head(5)


# In[101]:


#return atuple of the fimention of the data frame.
df.shape


# In[102]:


#display a concise summary of the dataframe.
df.info()


# In[103]:


#counting the hole numper of duplicated values in the data frame.
df.duplicated().sum()


# In[104]:


#selecting the rws with the nan values.
df_dup=df[df.duplicated()]
df_dup


# In[105]:


# drop all duplicated values in the entire dataframe.
# Confirm changes
df.drop_duplicates(inplace=True)
df.duplicated().sum()


# In[106]:


#check for nan values in which column. 
df.isnull().any()


# In[107]:


#counting the hole numper of NAN values in the entire dataframe.
df.isnull().sum().sum()


# In[108]:


# Checking useless rows in the census dataset inferred using info() & isnull() methods.
df.iloc[65:,:]


# In[109]:


#looking for all rows contain NAN values.
is_NaN = df.isnull()
row_has_NaN = is_NaN.any(axis=1)
rows_with_NaN = df[row_has_NaN]
rows_with_NaN 


# In[110]:


# generats some helpful descriptive statistics.
df.describe()


# In[111]:


# Change column name in df1 into lower case for the convenience of analysis
# Confirm changes
df.rename(columns = lambda x: x.lower(), inplace = True)
df.columns


# In[112]:


# As the NaN values are of string type therefore thty can't treated by filling with means 
# since they don't affect the arithmetic calculation nor satistical analysis
# so it is better to replace those NaN values with a common string type value which doesn't indicate anything
# For the numerical type of NaN, as each row has specific meaning, thus we can't fill them with mean

# As for df, numericial type of data was mispresented as string type, thus first task is to convert them into float
# Skip the first 2 columns as they should be string type, so leave them unchanged

columns = df.iloc[:,2:].columns
for col in columns:
    df[col] = df[col].str.extract('(\d+)').astype(float)
df.info()


# In[113]:


# Replace the all NaN in df with 'No Record' 
df.fillna('No record', inplace = True)
# Confirm changes 
df.isnull().any()


# ### gun_data:

# In[114]:


#call on datafame to display a few rows.
df1.head(5)


# In[115]:


#return atuple of the fimention of the data frame.
df1.shape


# In[116]:


#display a concise summary of the dataframe.
df1.info()


# In[117]:


#counting the hole numper of duplicated values in the data frame.
df1.duplicated().sum()


# In[118]:


#check for nan values in which column. 
df1.isnull().any()


# In[119]:


#counting the hole numper of NAN values in the entire dataframe.
df1.isnull().sum().sum()


# In[120]:


#looking for all rows contain NAN values.
is_NaN1 = df.isnull()
row_has_NaN1 = is_NaN1.any(axis=1)
rows_with_NaN1 = df[row_has_NaN1]
rows_with_NaN1 


# In[121]:


# generats some helpful descriptive statistics.
df1.describe()


# In[122]:


# Change column name in df1 into lower case for the convenience of analysis
# Confirm changes
df1.rename(columns = lambda x: x.lower(), inplace = True)
df1.columns


# In[123]:


# Convert string into datatime format in df1.
df1.month = pd.to_datetime(df1["month"],  errors="coerce")
# Confirm changes
df1.dtypes


# <a id='Exploratory Data Analysis'></a>
# ## Exploratory Data Analysis

# <a id="q1"></a>
#  ### The highest purchages record happened in which state for the persons under 18 years, percent on April 1, 2010.

# In[124]:


# print out a few rows of the data.
df.head(20)


# In[125]:


# print the index of the max value, as .idxmax() doesn't work properly :(
df_line = pd.DataFrame(df.iloc[7,2:]) 
df_line[df_line[7]==df_line[7].max()]


# > **Utah** state had the highest purchages record for persons under 18 years, percent on April 1, 2010, and the percent is 31.

# <a id="q2"></a>
# ### The census data is most associated with high gun per capita.

# In[126]:


df.head()


# <a id="q3"></a>
# ### The states have had the highest growth in gun registrations.

# In[127]:


df.head()


# <a id="q3"></a>
# ### The state that have had the highest growth in gun registrations.

# In[128]:


# Groupby time, state and sum of totals
gun_data_of_alltime = df1.groupby(['month', 'state'])['totals'].sum()


# In[129]:


# Find out the earliest and latest registration date
earliest_data = df1["month"].min()
latest_data = df1["month"].max() 


# In[130]:


# The amount of registed guns from lastest substract the earliest
gun_grow_tot =  gun_data_of_alltime.loc[latest_data] - gun_data_of_alltime.loc[earliest_data]


# In[131]:


#Fined the index of the max value.
gun_grow_tot.idxmax(axis=0, skipna=True)


# > 'kentucky' have had the highest growth in gun registrations over time.

# <a id="q4"></a>
# ### The overall trend of gun purchases.

# In[132]:


#grouping the date and the total numper of gun checks.
Gun_prechase_trend =df1.groupby(["month"])["totals"].sum()


# In[133]:


#the plot of gun perchase relations
Gun_prechase_trend.plot(kind ="line");


# >The over all trend in increasing and becomming faster over time.

# <a id ="q5"></a>
# ### The type of gun that has the highest quantity, and the relationship to totals.

# In[134]:


# select the guns columns
guns_df = df1.loc[:,['permit', 'permit_recheck', 'handgun', 'long_gun',
       'other', 'multiple', 'admin', 'prepawn_handgun', 'prepawn_long_gun',
       'prepawn_other', 'redemption_handgun', 'redemption_long_gun']]


# In[135]:


#total numper of each kind of guns.
gun_highest_quantity = guns_df.sum()


# In[136]:


#The type of gun that has the highest quantity
gun_highest_quantity.idxmax()


# In[137]:


#the value of the highest quantity
gun_highest_quantity.max()


# In[138]:


#The corolation betwen the highest quantity and the total numper of checks. 
df1.plot(kind = "scatter" ,x ="long_gun", y = "totals");


# > Long gun is highest registed type of gun in number among the others, it is positively correlated with totals.

# <a id="q6"></a>
# ### The sum of registered gun in each state over time.

# In[139]:


#grouping the total numper of gun checks per state.
guns_per_state =pd.DataFrame(df1.groupby("state")["totals"].sum())


# In[140]:


#ploting the total numper of gun checks per state. 
guns_per_state.plot(kind ="bar",figsize=(15,15));


# <a id="Conclusions"></a>
# ### Conclusion

# > In the current study,a good amount of perfound analysis has been carried out.Prior to each step,prior to each step,detailed instructions was given and interpretations were provided afterwards.the  data set included two tables, the data was ranged from 1998 to 2017,which consested of detailed information on regestration gunsbased on substin, the analysis would be more reliable opposed to more small_scale analysis.
