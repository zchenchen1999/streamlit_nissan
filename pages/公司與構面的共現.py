import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import pyvis

st.set_page_config(layout="wide")#,page_title="公司與構面的共現",page_icon="")

st.sidebar.title('參數設定')
# st.markdown("# 共現關係")
def plot_graph(df_corr,time_st,time_ed):


    corr_df = df_corr[(df_corr['corr']>time_st) & (df_corr['corr']<time_ed)].sort_values('corr',ascending=False)
    max_co_val = np.power(10,round(np.log10(corr_df['corr'].max())))

    net =  pyvis.network.Network(notebook=True,cdn_resources='in_line')
    net.add_nodes(corr_df.comp.unique().tolist(),color=['#FF2D2D']*len(corr_df.comp.unique().tolist()))
    net.add_nodes(corr_df.struct.unique().tolist(),color = ['#A5A552']*len(corr_df.struct.unique().tolist()))

    for i in corr_df.to_numpy():

        net.add_edge(i[0],i[1],width = i[2]/max_co_val*5,title = str(i[2]))

    # net.show_buttons(filter_=True)
    net.repulsion()

    net.show('company_struct_corr.html')
    HtmlFile = open('company_struct_corr.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(),width=800,height=600)


st.title('公司與構面的共現')


choice = st.sidebar.selectbox('Choose one:', ['_', '技術相關', '企劃相關'])
time_st,time_ed = st.sidebar.slider('共現次數:', 0, 300, (0, 100))


if choice == '技術相關':
    # df_dtm = pd.read_csv("mach_dtm_with_ner.csv")
    df_corr = pd.read_csv('mach_corr_with_ner.csv')
    plot_graph(df_corr,time_st,time_ed)
    
elif choice == '企劃相關':
    # df_dtm = pd.read_csv("mark_dtm_with_ner.csv")
    df_corr = pd.read_csv('mark_corr_with_ner.csv')
    plot_graph(df_corr,time_st,time_ed)


# ner_company_mach_list = '台積電、裕隆、鴻海、廣達、美光、中鋼、ASML、長春、台塑、聯發科、工研院、中科院、聯電、台電、日月光、台達、上銀、和泰、光寶、緯創、KLA、仁寶、台鐵、CSE、欣興、中油、漢翔、國瑞、IBM、穩懋、佳世達、華映、Apple、中華電信、群聯、華碩、友達、ODM、海思'.lower().split("、")
# ner_company_mark_list = '和泰、台積、元大、富邦、台電、好市多、奧美、鴻海、FMCG、國泰、日立、緯創、台哥大、中信、台塑、納智捷、全聯、網家、中華電信、中油、博弈遊戲公司、聯詠、大立光、陽明、台新'.lower().split("、")
# struct_df = pd.read_csv('structure.csv')[['class','name','alias']]
# struct_df = struct_df[struct_df['class'] != '產品與服務'].reset_index(drop=True)
# struct_name = struct_df['name'].tolist()
# if choice == '技術相關':
#     comp_choices = st.multiselect("公司",ner_company_mach_list)    
# elif choice == '企劃相關':
#     comp_choices = st.multiselect("公司",ner_company_mark_list)    