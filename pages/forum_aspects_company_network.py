import pandas as pd
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
import pyvis
import random
from annotated_text import annotated_text

st.set_page_config(layout="wide")
st.sidebar.title('參數設定')

structure = pd.read_csv('data/fourm/structure.csv')[['class','name','alias']]
structure = structure[structure['class'] != '產品與服務'].reset_index(drop=True)

# colors_uni = getColors()

colors_uni = []
while len(colors_uni) < 7:
    r = lambda: random.randint(0,255)
    r = '#%02X%02X%02X' % (r(),r(),r())
    if r not in colors_uni:
        colors_uni.append(r)
colors = []
for i,c in enumerate(structure['class'].unique()):
    l = structure[structure['class'] == c].shape[0]
    colors += [colors_uni[i]]*l
structure['color'] = colors
color_map_all = {}
for n,c in structure[['name','color']].to_numpy():
    color_map_all[n] = c


def plot_graph(df_corr,comp):

    corr_df = df_corr[(df_corr['company'] == comp) & (df_corr['corr']>0)]
    max_co_val = np.power(10,round(np.log10(corr_df['corr'].max())))

    net =  pyvis.network.Network("650px","100%",notebook=True,cdn_resources='in_line')
    nodes = list(set(corr_df.struct1.unique().tolist()+corr_df.struct2.unique().tolist()))
    color_list = []
    for n in nodes:
        color_list.append(color_map_all[n])
    
    net.add_nodes(nodes,color=color_list)
    
    for i in corr_df[['struct1','struct2','corr']].to_numpy():

        net.add_edge(i[0],i[1],width = i[2]/max_co_val*5,title = str(i[2]))

    # net.show_buttons(filter_=True)
    net.repulsion()
    net.show('struct_of_comp_corr.html')
    HtmlFile = open('struct_of_comp_corr.html', 'r', encoding='utf-8')
    components.html(HtmlFile.read(),height=660, scrolling=True)
    aspect_color_tuple_list = []
    for n,c in structure[['class','color']].drop_duplicates(keep='first').to_numpy():
        tmp_tuple = ("", "", c)
        tmp_list = []
        tmp_list.append(tmp_tuple)
        tmp_list.append(n)
        aspect_color_tuple_list.append(tmp_list)
    return aspect_color_tuple_list

st.title('公司底下之構面關係')
choice = st.sidebar.selectbox('Choose one:', ['_', '技術相關', '企劃相關'])

@st.cache_data
def getData(name):
    df_corr = pd.read_csv(name)
    return df_corr

col1, col2 = st.columns([8, 1])
if choice == '技術相關':
    # df_dtm = pd.read_csv("mach_dtm_with_ner.csv")
    # df_corr = pd.read_csv('mach_corr_of_class.csv')
    df_corr = getData('data/fourm/mach_corr_of_class.csv')
    companies = df_corr['company'].unique().tolist()
    company = st.sidebar.selectbox('Choose one:', companies)
    with col1:
        color_tuple = plot_graph(df_corr,company)
    with col2:
        for i in color_tuple:
            annotated_text(i)
elif choice == '企劃相關':
    # df_dtm = pd.read_csv("mark_dtm_with_ner.csv")
    # df_corr = pd.read_csv('mark_corr_of_class.csv')
    df_corr = getData('data/fourm/mark_corr_of_class.csv')
    companies = df_corr['company'].unique().tolist()
    company = st.sidebar.selectbox('Choose one:', companies)
    with col1:
        color_tuple = plot_graph(df_corr,company)
    with col2:
        for i in color_tuple:
            annotated_text(i)