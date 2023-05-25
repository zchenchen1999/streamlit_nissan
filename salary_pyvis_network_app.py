# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network
import json
import random

# =========================================================================================================================================#
# Streamlit runs from top to bottom, 
# so a new network graph will be generated based on the new item set when there is a change in the selection (e.g., add or remove item).
# =========================================================================================================================================#

# 預設顯示 wide mode
st.set_page_config(layout="wide")

# 設定標題
st.title('比薪水-字詞網路圖')

# 設定 side bar 標題
st.sidebar.title('參數設定')
# 選擇要畫 correlatoin 還是 co-occurance
option = st.sidebar.selectbox('選擇網路圖要呈現的關係',('correlatoin', 'co-occurrence'), index=0)

# silder
if (option == 'correlatoin'):
    # 實作 silder （選取關聯度）
    values = st.sidebar.slider(
        '選擇關聯度區間',
        0.0, 1.0, (0.2, 1.0))
    st.sidebar.write('關聯度:', values)
else:
    # 實作 silder （選取關聯度）
    values = st.sidebar.slider(
        '選擇共現次數區間',
        0, 2000, (100, 500))
    st.sidebar.write('共現次數:', values)

# 讀取資料 (CSV)
if (option=='correlatoin'):
    df_interact = pd.read_csv('data/salary/salary_dict_corre.csv')
else:
    df_interact = pd.read_csv('data/salary/salary_dict_CoOcurr.csv')


tf = open("./data/aspect.json", "r")
# 構面字典
aspect_dict = json.load(tf)

# 設定構面顏色
# 隨機挑選顏色
def generate_color():
    random_number = random.randint(0,16777215)
    hex_number = str(hex(random_number))
    hex_number ='#'+ hex_number[2:]
    return hex_number

# 固定顏色色碼
color_tag = ['#E74646', '#F79327', '#FFD966', '#8BDB81', '#93BFCF', '#1D267D', '#AB46D2', '#20262E', '#B7B7B7', '#FFF2CC', '#B99B6B']
aspect_color = {}
color_idx = 0
for k, v in aspect_dict.items():
    # aspect_color[k] = generate_color()
    aspect_color[k] = color_tag[color_idx]
    color_idx += 1

# 依照 value 找 key
def get_class_by_subclass(sub_class):
    for k, v in aspect_dict.items():
        if (sub_class in v):
            return k



# 定義下拉式選單選項（使用字母排序）
aspect_list = list(df_interact['class'].unique())
aspect_list.sort()

# 實作下來式選單（回傳一個 list）
selected_aspect = st.sidebar.multiselect('選一個構面繪圖', aspect_list)



# 設定初始化顯示內容（當使用者沒有選擇任何東西時）
if len(selected_aspect) == 0:
    st.sidebar.text('請至少選擇一項構面開始繪圖！')

# 當使用者選擇至少一項內容時
else:
    # 依照構面該選資料
    df_select = df_interact.loc[df_interact['class'].isin(selected_aspect)]
    # 依照關聯度篩選資料
    df_select = df_select[(df_select['value'] > values[0]) & (df_select['value'] < values[1])]
    df_select = df_select.reset_index(drop=True)
    # 移除 corr 為 1 的資料
    df_select = df_select[df_select['item1'] != df_select['item2']]


    # # Create networkx graph object from pandas dataframe
    # G = nx.from_pandas_edgelist(df_select, 'item1', 'item2', 'correlation')

    # # Initiate PyVis network object
    # interview_net = Network(height='800px', width='1700px', bgcolor='white', font_color='black')

    # # Take Networkx graph and translate it to a PyVis graph format
    # interview_net.from_nx(G)

    # # Generate network with specific layout settings
    # # 設定重力
    # interview_net.repulsion(node_distance=420, central_gravity=0.33,
    #                    spring_length=110, spring_strength=0.10,
    #                    damping=0.95)
    In_Graph = {}
    # color = [aspect_color[get_class_by_subclass(i)] for i in df_select['item1']]
    interview_net = Network(height='550px',width="100%")
    nid=1
    # 加入 node
    for i in df_select['item1']:
        if (i not in In_Graph.keys()): 
            interview_net.add_node(n_id=nid, 
                                label=i, 
                                color=aspect_color[get_class_by_subclass(i)],
                                title=get_class_by_subclass(i))
            In_Graph[i] = nid
            nid += 1
    for i in df_select['item2']:
        if (i not in In_Graph.keys()): 
            interview_net.add_node(n_id=nid, 
                                label=i, 
                                color=aspect_color[get_class_by_subclass(i)],
                                title=get_class_by_subclass(i))
            In_Graph[i] = nid
            nid += 1
    # 加入 edge
    for i, row in df_select.iterrows():
        # print(row['item1'])
        interview_net.add_edge(In_Graph[row['item1']], In_Graph[row['item2']], weight=row['value'], title=row['value'], value=row['value'])

    # 利用 try, expect 來配合 streamlit server 或 local 的路徑（因為 server 有 /tmp，但沒有與 loacl 一樣的路徑）
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        interview_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        interview_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=600, scrolling=True)