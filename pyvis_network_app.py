# Import dependencies
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# =========================================================================================================================================#
# Streamlit runs from top to bottom, 
# so a new network graph will be generated based on the new item set when there is a change in the selection (e.g., add or remove item).
# =========================================================================================================================================#

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# 讀取資料 (CSV)
df_interact = pd.read_csv('data/processed_drug_interactions.csv')

# 設定標題
st.title('面試趣 - 互動式字詞網路關係圖')

# 定義下拉式選單選項（使用字母排序）
drug_list = ['Metformin', 'Glipizide', 'Lisinopril', 'Simvastatin',
            'Warfarin', 'Aspirin', 'Losartan', 'Ibuprofen']
drug_list.sort()

# 實作下來式選單（回傳一個 list）
selected_drugs = st.multiselect('Select drug(s) to visualize', drug_list)

# 設定初始化顯示內容（當使用者沒有選擇任何東西時）
if len(selected_drugs) == 0:
    st.text('請選擇一項開始繪圖！')

# 當使用者選擇至少一項內容時
else:
    df_select = df_interact.loc[df_interact['drug_1_name'].isin(selected_drugs) | \
                                df_interact['drug_2_name'].isin(selected_drugs)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'drug_1_name', 'drug_2_name', 'weight')

    # Initiate PyVis network object
    drug_net = Network(height='465px', bgcolor='white', font_color='black')

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout settings
    drug_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)

    # 利用 try, expect 來配合 streamlit server 或 local 的路徑（因為 server 有 /tmp，但沒有與 loacl 一樣的路徑）
    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)