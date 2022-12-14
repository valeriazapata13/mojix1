import streamlit as st
import pandas as pd


###### FUENTE DE DATOS ######
df_expected = pd.read_csv("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Expected.csv", encoding="latin-1", dtype=str)
df_counted = pd.read_csv("https://storage.googleapis.com/mojix-devops-wildfire-bucket/analytics/bootcamp_2_0/Bootcamp_DataAnalysis_Counted.csv", encoding="latin-1", dtype=str)

###### LIMPIEZA DE DATOS ######
df_counted = df_counted.drop_duplicates("RFID")
df_B = df_counted.groupby("Retail_Product_SKU").count()[["RFID"]].reset_index().rename(columns={"RFID":"Retail_CCQTY"})

my_cols_selected_A= ["Retail_Product_Level1Name",
"Retail_Product_Name",
"Retail_Product_Color",
"Retail_Product_SKU",
"Retail_Product_Size",
"Retail_Product_Style",
"Retail_SOHQTY"]

df_A = df_expected[my_cols_selected_A]


df_discrepancy = pd.merge(df_A, df_B, how="outer", left_on="Retail_Product_SKU", right_on="Retail_Product_SKU", indicator=True)
df_discrepancy['Retail_CCQTY'] = df_discrepancy['Retail_CCQTY'].fillna(0)
df_discrepancy["Retail_CCQTY"] = df_discrepancy["Retail_CCQTY"].astype(int)
df_discrepancy["Retail_SOHQTY"] = df_discrepancy["Retail_SOHQTY"].fillna(0).astype(int)
df_discrepancy["Diff"] = df_discrepancy["Retail_CCQTY"] - df_discrepancy["Retail_SOHQTY"]
df_discrepancy.loc[df_discrepancy["Diff"]<0, "Unders"] = df_discrepancy["Diff"] * (-1)
df_discrepancy["Unders"] = df_discrepancy["Unders"].fillna(0).astype(int)
df_discrepancy=df_discrepancy.rename(columns={"Retail_Product_Level1Name":"Retail_Category"})


###### DISEÑO DE APP ######
st.title ('My First App')
st.subheader('Data Set')
st.markdown('-----')
st.dataframe(df_discrepancy)
st.markdown('-----')

col1, col2 ,col3 = st.columns(3)
col1.metric(label="Retail_SOHQTY", value= df_discrepancy["Retail_SOHQTY"].sum() )
col2.metric(label="Retail_CCQTY", value= df_discrepancy["Retail_CCQTY"].sum() )
col3.metric(label="Unders", value= df_discrepancy["Unders"].sum() )

st.markdown('-----')


st.subheader('Requested Products per Category')

#st.bar_chart(df_discrepancy.groupby(['Retail_Category']).sum()[['Unders']])

import matplotlib.pyplot as plt
import numpy as np

#dfc=df_discrepancy.groupby(['Retail_Category']).sum()[['Unders']]
dfc=df_discrepancy.groupby(['Retail_Category']).sum()[['Unders']].reset_index()
dfca=dfc['Retail_Category']
dfcb=dfc['Unders']
colores = ["#be2596","#96be25","#2596be"]
fig, ax = plt.subplots()
ax.pie(dfcb,labels=dfca,colors=colores)

st.pyplot(fig)



st.markdown('-----')
st.subheader('Top 10 most requested Products')

dfd=df_discrepancy.groupby(['Retail_Product_Name']).sum()[['Retail_CCQTY']].sort_values('Retail_CCQTY',ascending=False)
dfd= dfd.head(10)
st.bar_chart(dfd)


st.markdown('-----')





