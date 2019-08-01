from bs4 import BeautifulSoup
import  pandas as pd
import  numpy as np
import requests as req

url = 'https://www.canada.ca/en/immigration-refugees-citizenship/services/study-canada/study-permit/prepare/designated-learning-institutions-list.html'
source = req.get(url).text

df_bc = pd.read_html(source)[0] # British Columbia
df_al = pd.read_html(source)[1] # Alberta
df_sask = pd.read_html(source)[2] # Saskatchewan
df_mn = pd.read_html(source)[3] # Manitoba
df_on = pd.read_html(source)[4] # Ontario
df_qc = pd.read_html(source)[5] # Quebec
df_pei = pd.read_html(source)[6] # Prince Edward Island
df_nb = pd.read_html(source)[7] # New Brunswick
df_nv = pd.read_html(source)[8] # Nova Scotia
df_nl = pd.read_html(source)[9] # Newfoundland and Labrador
df_yk = pd.read_html(source)[10] # Yukon
df_nt = pd.read_html(source)[11] # Northwest Territories

df = {
    'British Columbia' : df_bc, 
    'Alberta' : df_al,
    'Saskatchewan' : df_sask,
    'Manitoba' : df_mn,
    'Ontario' :df_on,
    'Quebec' : df_qc,
    'Prince Edward Island' : df_pei,
    'New Brunswick' : df_nb,
    'Nova Scotia' : df_nv,
    'Newfoundland & Labrador' : df_nl,
    'Yukon' : df_yk,
    'Northwest Territories' : df_nt,
    } #dict of dataframes for concating (see below)

df_canada = pd.concat(df, sort=False) #concats into one dataframe
filter_ = ['Helicopters','Flying','Aviation','Flight','Air'] #list of strings to filter
df_canada = df_canada[~df_canada['Name of institution'].str.contains('|'.join(filter_))] # filters flying schools out

_filter = np.in1d(df_canada['Offers PGWP-eligible programs'].values, ['No'], invert=True) #removes those that don't have a pgwp eligible program
df_canada = df_canada[_filter]

with pd.ExcelWriter('Canada_List.xlsx') as writer:
    df_canada.to_excel(writer, 'Sheet 1')
    writer.save()