#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Zaimportowanie bibliotek
import pandas as pd
import numpy as np


# In[2]:


#Wczytanie danych z transportu do ramki danych 'data' oraz jej wyświetlenie
data=pd.read_csv("C:/Users/piotr/Desktop/dane.csv", sep=';')

data


# In[3]:


#Pokazanie najniższej temperatury w ramce danych 'data'
data.Temperatura.min()


# In[4]:


#Pokazanie najwyższej temperatury w ramce danych 'data'
data.Temperatura.max()


# In[5]:


#Pokazanie średniej temperatury w ramce danych 'data' z dokładnością do 2 miejsc po przecinku
get_ipython().run_line_magic('precision', '%.2f')
data.Temperatura.mean()


# In[6]:


#Połączenie kolum 'Dzien' i 'Godzina' w jedną, o nazwie 'czas'
czas = data['Dzien'] + " " + data['Godzina']
czas


# In[7]:


#Import bibliotek do stworzenia wykresu
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# In[8]:


#Wykres przedstawiający temperaturę podczas transportu jabłek drogą morską w kontenerze
plt.rcParams['figure.figsize'] = [15, 8]

fig = plt.figure()
x = czas
y = data['Temperatura']

plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=120))
plt.xticks(rotation=90, size=7)
plt.xticks(size = 15)
plt.yticks(size = 15)
plt.title('Temperatura podczas transportu jabłek drogą morską w kontenerze', fontsize=30)
plt.xlabel('Data i godzina', fontsize=25, labelpad=20)
plt.ylabel('Temperatura [°]', fontsize=25, labelpad=20)

plt.plot(x, y)
plt.show()

