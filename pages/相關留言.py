import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
st.set_page_config(layout="wide")
st.sidebar.title('參數設定')
st.title('相關留言')
ner_company_mach_list = '台積電、裕隆、鴻海、廣達、美光、中鋼、ASML、長春、台塑、聯發科、工研院、中科院、聯電、台電、日月光、台達、上銀、和泰、光寶、緯創、KLA、仁寶、台鐵、CSE、欣興、中油、漢翔、國瑞、IBM、穩懋、佳世達、華映、Apple、中華電信、群聯、華碩、友達、ODM、海思'.lower().split("、")
ner_company_mark_list = '和泰、台積、元大、富邦、台電、好市多、奧美、鴻海、FMCG、國泰、日立、緯創、台哥大、中信、台塑、納智捷、全聯、網家、中華電信、中油、博弈遊戲公司、聯詠、大立光、陽明、台新'.lower().split("、")
struct_df = pd.read_csv('structure.csv')[['class','name','alias']]
struct_df = struct_df[struct_df['class'] != '產品與服務'].reset_index(drop=True)
struct_name = struct_df['name'].tolist()
choice = st.sidebar.selectbox('Choose one:', ['_', '技術相關', '企劃相關'])

def show_df(df_dtm,comp_choices,struct_choices):
    tab_list = []
    tab_tuple = []
    for c in comp_choices:
        for s in struct_choices:
            tab_list.append(f":clipboard: {c}_{s}")
            tab_tuple.append((c,s))
    tab_list = st.tabs(tab_list)
    for i,t in enumerate(tab_tuple):
        with tab_list[i]:
            st.markdown(f"### {t[0]} 和 {t[1]}")
            temp_df = df_dtm[(df_dtm[t[0]]>0) & (df_dtm[t[1]]>0)][['artUrl','artDate','artTitle','artContent','comment_list']]
            st.write(temp_df.drop_duplicates(['artUrl','comment_list'],keep="first"))

if choice == '技術相關':
    df_dtm = pd.read_csv("mach_dtm_with_ner.csv")
    comp_choices = st.sidebar.multiselect("公司",ner_company_mach_list)
    struct_choices = st.sidebar.multiselect("構面",struct_name)
    if len(comp_choices)>0 and len(struct_choices)>0:
        show_df(df_dtm,comp_choices,struct_choices)
    
elif choice == '企劃相關':
    df_dtm = pd.read_csv("mark_dtm_with_ner.csv")
    comp_choices = st.sidebar.multiselect("公司",ner_company_mark_list)
    struct_choices = st.sidebar.multiselect("構面",struct_name)
    if len(comp_choices)>0 and len(struct_choices)>0:
        show_df(df_dtm,comp_choices,struct_choices)
    


        
        
        




