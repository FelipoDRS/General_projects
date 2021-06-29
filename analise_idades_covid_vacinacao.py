# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 17:17:42 2021

@author: Felipo Soares
"""
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
collect_data=pd.read_csv(r'C:\Users\Felipo Soares\Documents\Python Scripts\idade_obitos_covid_brasil.csv',index_col=0)
collect_data['data']=pd.to_datetime(collect_data['data'])
collect_data.index=collect_data['data']

#Seleciona dados de todo o brasil
data_M=collect_data.loc[np.logical_and(collect_data['genero']=='M',collect_data['UF']=='all')]
data_F=collect_data.loc[np.logical_and(collect_data['genero']=='F',collect_data['UF']=='all')]
#Nan ocorre quando o portal da transperância não registra 
#óbito para determinada faixa etária em um determinado dia
data_M.fillna(value=0,inplace=True)
data_F.fillna(value=0,inplace=True)

#Soma dos óbitos da semana para suavizar os dados
data_M_val=data_M.loc[:,['< 9', '10 - 19', '20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69',
       '70 - 79', '80 - 89', '90 - 99','> 100']].rolling(7).sum()
data_F_val=data_F.loc[:,['< 9', '10 - 19', '20 - 29', '30 - 39', '40 - 49', '50 - 59', '60 - 69',
       '70 - 79', '80 - 89', '90 - 99','> 100']].rolling(7).sum()
    
                             
#Calcula a distribuição cumulativa dos óbitos por dados
data_M_cdf=np.cumsum(data_M_val,axis=1)/np.sum(data_M_val,axis=1)[:,None]
data_M_cdf=data_M_cdf.dropna(axis=0)

#Calcula a distribuição probabilistica dos óbitos por dados
data_M_pdf=data_M_val/np.sum(data_M_val,axis=1)[:,None]
data_M_pdf=data_M_pdf.dropna()

data_F_cdf=np.cumsum(data_F_val,axis=1)/np.sum(data_F_val,axis=1)[:,None]
data_F_cdf=data_F_cdf.dropna(axis=0)

data_F_pdf=data_F_val/np.sum(data_F_val,axis=1)[:,None]
data_F_pdf=data_F_pdf.dropna()

# Mediana é calculada fazendo-se um spline do CDF e 
#encontrando o valor mais próximo de 50%

from scipy.interpolate import interp1d

x=np.arange(10,120,10)
x_look=np.arange(30,90,0.05)
interpol_M=interp1d(x,data_M_cdf)
yhat_M=interpol_M(x_look)
erro_M=np.abs(yhat_M-0.5)
ind_M=np.argmin(erro_M,axis=1)
mediana_M=[]
for i in range(data_M_cdf.shape[0]):
    mediana_M.append(x_look[ind_M[i]])
# Mulheres
interpol_F=interp1d(x,data_F_cdf)
yhat_F=interpol_F(x_look)
erro_F=np.abs(yhat_F-0.5)
ind_F=np.argmin(erro_F,axis=1)
mediana_F=[]
for i in range(data_M_cdf.shape[0]):
    mediana_F.append(x_look[ind_F[i]])
#plt.figure();plt.plot(data_man_cdf.index,mediana,'o-')

sns.set_theme(style="darkgrid")
plt.figure(figsize=(8,4.5));sns.lineplot(x=data_F_cdf.index,y=mediana_F)
sns.lineplot(x=data_M_cdf.index,y=mediana_M)
plt.legend(['Mulheres','Homens'])
plt.text(datetime.datetime(2020,9,1),65,'Vacinação começa \n dia 18/01/2021')
plt.plot([datetime.datetime(2021,1,18),datetime.datetime(2021,1,18)],[np.max(mediana_F),np.min(mediana_M)],'r--')
#plt.plot([datetime.datetime(2021,1,18)+datetime.timedelta(days=15),datetime.datetime(2021,1,18)+datetime.timedelta(days=15)],[np.max(mediana),np.min(mediana)],'g--')
plt.ylabel('Idade mediana dos óbitos por COVID')
plt.title('Redução da idade mediana dos óbitos por COVID no Brasil')
plt.savefig('mediana_obitos_covid.png',dpi=200)

#tick_x=np.arange(10,465,step=15)
#label_tick=data_man['data'].iloc[tick_x].values
#plt.xticks(tick_x,label_tick,rotation=45)
plt.yticks(np.arange(54,80,step=2))
plt.grid()

#Média se vocês estiverem interessados
x_media=np.arange(5,115,10)
media_F=np.matmul(data_F_pdf.values,x_media)
media_M=np.matmul(data_M_pdf.values,x_media)

plt.figure(figsize=(8,4.5));sns.lineplot(x=data_F_pdf.index,y=media_F)
sns.lineplot(x=data_M_pdf.index,y=media_M)
plt.legend(['Mulheres','Homens'])
plt.text(datetime.datetime(2020,9,1),65,'Vacinação começa \n dia 18/01/2021')
plt.plot([datetime.datetime(2021,1,18),datetime.datetime(2021,1,18)],[np.max(mediana_F),np.min(mediana_M)],'r--')
#plt.plot([datetime.datetime(2021,1,18)+datetime.timedelta(days=15),datetime.datetime(2021,1,18)+datetime.timedelta(days=15)],[np.max(mediana),np.min(mediana)],'g--')
plt.ylabel('Idade média dos óbitos por COVID')
plt.title('Redução da idade média dos óbitos por COVID no Brasil')
plt.savefig('media_obitos_covid.png',dpi=200)


