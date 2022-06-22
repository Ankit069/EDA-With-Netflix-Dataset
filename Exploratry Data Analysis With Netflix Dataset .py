#!/usr/bin/env python
# coding: utf-8

# # Import Basic Libraries

# In[1]:


import pandas as pd 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# In[2]:


data=pd.read_csv('Downloads//8. Netflix Dataset.csv')


# In[3]:


data.head()


# In[4]:


data.tail()


# # Data Preparation and Cleaning
# 
# Now will explore our data in more detail like : 
# number of rows and columns peresnt in Dataset, range of values, check and handle missing, incorrect and invalid data and perform some more analysis as per requirment.
# 

# In[5]:


data.shape


# In[6]:


data.size


# In[7]:


data.info()


# In[8]:


data.describe().T


# In[9]:


data[data.duplicated()]


# In[10]:


data.drop_duplicates(inplace=True)


# In[11]:


data.shape


# In[12]:


data.isnull().sum().sum()


# In[13]:


data.isnull().sum()


# In[14]:


plt.figure(figsize=(15,8))
sns.heatmap(data.isnull())


# **Observation:** 
#     
# **Director has 2388 missing values**
# \
# **Cast has 718 missing values**
# \
# **Country has 507 missing values**
# \
# **Release_Date has 10 missing values**
# \
# **Rating has 7 missing values**    

# In[15]:


# creating a copy of dataset so that will not affect our original dataset.
netflix= data.copy()


# In[16]:


# dealing with null values
netflix['Director'].fillna('No Director', inplace=True)
netflix['Cast'].fillna('No Cast', inplace=True)
netflix['Country'].fillna('Country Unavailable', inplace=True)
netflix.dropna(subset=['Release_Date','Rating'],inplace=True)


# In[17]:


#check if there is null value available or not
netflix.isnull().any()


# In[18]:


netflix["Release_Date"].value_counts()


# In[19]:


netflix["Release_year"]=netflix["Release_Date"].str.split(" ").str[-1]
netflix["Release_year"]


# In[20]:


netflix["Release_Day"]=netflix["Release_Date"].str.split(" ").str[-2].str.split(",").str[-2]
netflix["Release_Day"]


# In[21]:


netflix["Release_month"]=netflix["Release_Date"].str.split(" ").str[-3]
netflix["Release_month"]


# # Exploratory Data Analysis And Visualization

# # For 'house of cards',whats is the show id and who is the director of this show

# In[22]:


data[data['Title'].isin(['House of Cards'])]


# **Show id-s2833**
# \
# **Director -Robin Wright, David Fincher, Gerald McRaney**

# # Category is movie and type is Dramas

# In[23]:


data[(data['Category']=='Movie') & (data['Type']=='Dramas')]


# # Show all the movies that were released in 2009

# In[24]:


#grouping
netflix.groupby(["Category","Release_year"]).size().reset_index().head(2)


# # Show top 10 directors ,who gives the highest number of TV shows and movies

# In[25]:


data['Director'].value_counts().head(10)


# # Show all the records ,where Category is movie and type is comedy or country is 'United Kingdom'

# In[26]:


netflix[(netflix["Category"]=="Movie")&(netflix["Type"]=="Comedy")|(netflix["Country"]=="United Kingdom")]


# # What are different ratings defined by netflix

# In[27]:


netflix['Rating'].unique()


# # How many movies got TV-14 rating in canada

# In[28]:


#filtering
netflix[(netflix['Category']=='Movie')&(netflix['Rating']=='TV-14')&(netflix['Country']=='Canada')]


# **There are total 11 movies ,got rating "TV-14" in Canada**

# # What is the maximum duration in the data set

# In[29]:


#we need to split the numeric and categorical elements
netflix[['Minutes','Unit']]=netflix['Duration'].str.split(' ',expand=True)
netflix.head(2)


# In[30]:


#maximum duration 
netflix.Minutes.max()


# # In which year Highest number of tv shows and movies were released

# In[31]:


#To know the year in which the highest number of TV shows and movies were released We will use value_Counts
netflix['Release_year'].value_counts()


# **Hence the Answer is year 2019 ,in which highest number of TV shows and movies were released**

# In[32]:


#With the Graph
plt.figure(figsize=(10,8))
netflix['Release_year'].value_counts().plot(kind='bar',color="g")
plt.xlabel("Release_Year")
plt.ylabel("Count of contents");


# # How many movies and tv shows are in the dataset

# In[33]:


#count the values
netflix.Category.value_counts() 


# In[34]:


#with graph
plt.figure(figsize=(10,6))
data.groupby("Category").Category.count().plot(kind='bar')
plt.title("Count of Movie And Tv shows")
plt.xlabel("Type (Movie/TV Show)")
plt.ylabel("Total Count");


# In[35]:


#with pie plot
plt.figure(figsize=(15,10))
sns.set(font_scale=2)
plt.title("Percentation of Netflix Categories that are either Movies or TV Shows")
plt.pie(netflix.Category.value_counts(),labels=netflix.Category.value_counts().index, colors=['green','blue'],autopct='%1.1f%%', startangle=180,explode=(0.025,0.025))
plt.show()


# **The quantity of Movies is more than TV shows**

# **Only 2 movies released in year 2009**

# # Which individual country has highest numbers of tv shows

# In[36]:


#filtering data
netflix_tvshow=netflix[netflix['Category']=='TV Show']


# In[37]:


netflix_tvshow.Country.value_counts()


#  **United State has highest numbers of TV shows**

# In[38]:


plt.figure(figsize=(12,6))
netflix_tvshow.Country.value_counts().head(10).plot(kind='bar',color='green')
plt.xlabel("Country")
plt.ylabel("Total Tv shows");


#  **United State has highest numbers of TV shows**

# # Which individual country has highest numbers of movies

# In[39]:


#Filtering data
netflix_movie=data[data['Category']=='Movie']


# In[40]:


plt.figure(figsize=(12,6))
netflix_tvshow.Country.value_counts().head(10).plot(kind='bar',color='red')
plt.xlabel("Country")
plt.ylabel("Total Tv shows");


#  **United State has highest numbers of movies**

# # Top 15 countries produces most contents
# 

# In[41]:


filtered_countries = netflix.set_index('Type').Country.str.split(', ', expand=True).stack().reset_index(level=1, drop=True);
filtered_countries = filtered_countries[filtered_countries != 'Country Unavailable']

plt.figure(figsize=(7,9))
g = sns.countplot(y = filtered_countries, order=filtered_countries.value_counts().index[:15])
plt.title('Top 15 Countries on Netflix')
plt.xlabel('Types')
plt.ylabel('Country')
plt.show()


# **United state make large numbers of contents**

# # Who are the top 10 Movies actors on Netflix based on number of titles

# In[42]:


filtered_cast = netflix[netflix.Cast != 'No Cast'].set_index('Title').Cast.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
sns.countplot(y = filtered_cast, order=filtered_cast.value_counts().index[:10], palette='rocket')
plt.show()


# **The top actor on Netflix Movies, based on the number of titles, is Anupam Kher.**

# # Who are the top 10 directors on Netflix with the most releases

# In[43]:


plt.figure(figsize=(12,9))
filtered_directors = netflix[netflix.Director != 'No Director'].set_index('Title').Director.str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
sns.countplot(y = filtered_directors, order=filtered_directors.value_counts().index[:10], palette='mako')
plt.show()


# # Conclusion

# **We have drawn many interesting inferences from the dataset Netflix titles; here’s a summary of the few of them:**
# 
# 1. The most content type on Netflix is movies.
# 
# 2. The country by the amount of the produces content is the United States,
# 
# 3. The most popular director on Netflix , with the most titles, is Jan Suter.
# 
# 4. International Movies is a genre that is mostly in Netflix.
# 
# 5. largest count of Netflix content is made with a “TV-14” rating.
# 
# 6. The most popular actor on Netflix TV Shows based on the number of titles is Takahiro Sakurai.
# 
# 7. The most popular actor on Netflix movie, based on the number of titles, is Anupam Kher.
# 
# **It's clear that Netflix has grown over the years. We can see it from the data that the company took certain approaches in their marketing strategy to break into new markets around the world.**
