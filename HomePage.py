import streamlit as st
import time
import numpy as np
import pandas as pd
import plotly.express as px


# 預設顯示 wide mode
st.set_page_config(page_title="裕日僱主品牌輿情系統", layout="wide")

# title
st.title("裕日僱主品牌輿情系統")

st.divider()

st.subheader("公司概況統計")
df_company = pd.read_csv('./data/company_info.csv').drop(columns='Unnamed: 0')
df_company.rename(columns = {'company_name':'公司名稱', 'industry':'產業別', 'location':'地區', 'grade':'面試評價', 'degree':'面試難度', 'mood':'上班心情', 'frequence':'加班頻率', 'salary_month':'平均月薪', 'interview_num':'面試心得數', 'salary_num':'薪水情報數', 'account':'資本額'}, inplace = True)
st.caption("「面試評價、面試難度、上班心情、加班頻率、平均月薪、面試心得數、薪水情報數」為面試趣與比薪水爬取資訊")
st.dataframe(df_company)


st.divider()

st.subheader("面試趣 / 比薪水解鎖文章統計")
st.caption("已過濾掉「客服」、「專員」相關職位")

# 取資料
df_list = [[] for i in range(2)]
# 0:面試趣總體, 1:面試趣汽車公司, 2:比薪水總體, 3:比薪水汽車公司
df_list[0].append(pd.read_csv('./data/art_count/interview/total.csv').drop(columns='Unnamed: 0'))
df_list[0].append(pd.read_csv('./data/art_count/interview/each_company.csv').drop(columns='Unnamed: 0'))
df_list[1].append(pd.read_csv('./data/art_count/salary/total.csv').drop(columns='Unnamed: 0'))
df_list[1].append(pd.read_csv('./data/art_count/salary/each_company.csv').drop(columns='Unnamed: 0'))

# 建立頁籤
tab_list = st.tabs(["面試趣","比薪水"])
# 每個頁籤建立內容
for i in range(2):
    
    tab_list[i].write("總體文章數")
    tab_list[i].dataframe(data=df_list[i][0], use_container_width=True)
    tab_list[i].write("汽車產業公司解鎖文章數")
    tab_list[i].dataframe(data=df_list[i][1], use_container_width=True, height=600)
    
    # fig = px.pie(df_list[i][1], values='未解鎖', names='公司', title='未解鎖汽車產業公司佔比')
    # tab_list[i].plotly_chart(fig, use_container_width=True)
    fig = px.pie(df_list[i][1], values='已解鎖', names='公司', title='已解鎖汽車產業公司佔比')
    tab_list[i].plotly_chart(fig, use_container_width=True)

