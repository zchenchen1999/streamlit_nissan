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

@st.cache_data
def getCorr(name):
    df_dtm = pd.read_csv(name)
    return df_dtm

if choice == '技術相關':
    
    # df_corr = pd.read_csv('mach_corr_with_ner.csv')
    df_corr = getCorr('data/fourm/mach_corr_with_ner.csv')
    plot_graph(df_corr,time_st,time_ed)
    
elif choice == '企劃相關':
    
    # df_corr = pd.read_csv('mark_corr_with_ner.csv')
    df_corr = getCorr('data/fourm/mark_corr_with_ner.csv')
    plot_graph(df_corr,time_st,time_ed)


   