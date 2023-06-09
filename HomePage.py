import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px


# 預設顯示 wide mode
st.set_page_config(page_title="裕日僱主品牌輿情系統", layout="wide")

# title
st.title("裕日僱主品牌輿情系統")

df_list = [[] for i in range(2)]
# 0:面試趣總體, 1:面試趣汽車公司, 2:比薪水總體, 3:比薪水汽車公司
df_list[0].append(pd.read_csv('./data/art_count/interview/total.csv').drop(columns='Unnamed: 0'))
df_list[0].append(pd.read_csv('./data/art_count/interview/each_company.csv').drop(columns='Unnamed: 0'))
df_list[1].append(pd.read_csv('./data/art_count/salary/total.csv').drop(columns='Unnamed: 0'))
df_list[1].append(pd.read_csv('./data/art_count/salary/each_company.csv').drop(columns='Unnamed: 0'))
print(df_list)
tab_list = st.tabs(["面試趣","比薪水"])
for i in range(2):
    
    tab_list[i].write("總體文章數")
    tab_list[i].dataframe(data=df_list[i][0], use_container_width=True)
    tab_list[i].write("汽車產業公司解鎖文章數")
    tab_list[i].dataframe(data=df_list[i][1], use_container_width=True, height=600)
    
    # 產業別
    # industry_df = 
    # fig = px.pie(df_list[i][1], values='未解鎖', names='公司', title='未解鎖汽車產業公司佔比')
    # tab_list[i].plotly_chart(fig, use_container_width=True)
    fig = px.pie(df_list[i][1], values='未解鎖', names='公司', title='未解鎖汽車產業公司佔比')
    tab_list[i].plotly_chart(fig, use_container_width=True)
    fig = px.pie(df_list[i][1], values='已解鎖', names='公司', title='已解鎖汽車產業公司佔比')
    tab_list[i].plotly_chart(fig, use_container_width=True)

