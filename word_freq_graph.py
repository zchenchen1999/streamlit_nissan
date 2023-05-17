# # 詞頻計算圖
# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px

# # 標題、文字
# st.title("Sentiment Analysis of Tweets about US Airlines")
# st.markdown("This application is a Streamlit dashboard to analyze the sentiment of tweets")

# # sidebar 標題、文字
# st.sidebar.title("Sentiment Analysis of Tweets about US Airline")
# st.sidebar.markdown("This application is a Streamlit dashboard to analyze the sentiment of tweets")


import streamlit as st
import plotly.graph_objs as go
from datetime import datetime
from plotly.subplots import make_subplots
import pandas as pd
import datetime

#利用st.cache()快取沒有改變過的data
# @st.cache()
# 爬蟲程式
def get_df(path=None):
    # 轉換日期
    date_format = '%Y.%m.%d'
    try:
        df = pd.read_csv(path)
        date_format = '%Y.%m.%d'
        df['post_time'] = df['post_time'].apply(lambda x: datetime.datetime.strptime(x, date_format).date())
    except:
        print("讀取資料失敗，請檢查路徑")
    return df
    #會返回一個DF
df = get_df("data/dtm_result.csv")
min_day = df['post_time'].min()
max_day = df['post_time'].max()

# ---------------------------------- sidebar --------------------------------- #



st.sidebar.header('參數設定')
start_date = st.date_input(label='選擇起始日期', value=min_day, min_value=min_day, max_value=max_day)
end_date = st.date_input(label='選擇結束日期', value=start_time, min_value=start_time, max_value=max_day)
aspect_list = ['成就感', '學習成長','創新', '薪資', '福利', '管理制度', '工作氛圍', '同事互動', '主管風格', '工作地點', '公司規模','工作環境', '產業前景', '輪調', '外派', '出差', '引擎', '馬力', '避震', '外觀', '操控', '安全','堅固', '配備', '價錢', '科技', '品質', '折舊', '品牌', '空間', '保養', '續航', '尺寸', '車種','驅動', '變速箱', '電資', '機械', '製造', '車輛工程', '品管', '多元性', '企業社會責任', '企業永續目標','面試', '徵才', '實習', '工作', '離職', '轉職', '新鮮人', '畢業', '出路', '能力', '招募人員','正向', '負向']
aspect_option = st.selectbox('選擇構面',aspect_list)

# ----------------------------------- body ----------------------------------- #
# st.image('./icon.png')
st.title('面試趣-構面討論趨勢圖')

# ----------------------------------- plotly --------------------------------- #

if start_date and end_date and aspect_option:
    #如果stock_code與month都有值的話，則畫圖
    df_select = df[(df['post_time'] > start_date) & (df['post_time'] < end_date)]
    st.dataframe(df_select)
    st.success('Load data success !')

    # if Bubble_info != '成交量':
    #     #如果選項不同，畫圖則不同
    #     trace1 = go.Scatter(
    #         x=data['日期'],
    #         y=data['收盤價'],
    #         mode='lines+markers',
    #         marker=dict(size=data[f'{Bubble_info}'].abs(),
    #                     sizeref=data[f'{Bubble_info}'].abs().mean() /
    #                     Bubble_size,
    #                     color=data[f'{Bubble_info}買賣顏色']),
    #         line =dict(dash= 'dot'),
    #         hovertemplate="<b>日期%{x}</b><br> 收盤價 %{y} " + f"{Bubble_info} :" +
    #         "%{marker.size}<br>",
    #         name='收盤價')
    # else:
    #     trace1 = go.Scatter(x=data['日期'],
    #                         y=data['收盤價'],
    #                         mode='lines+markers',
    #                         marker=dict(
    #                             size=data[f'{Bubble_info}'].abs(),
    #                             sizeref=data[f'{Bubble_info}'].abs().mean() /
    #                             Bubble_size,
    #                         ),
    #                         line =dict(dash= 'dot'),
    #                          hovertemplate="<b>日期%{x}</b><br> 收盤價 %{y}",
    #                         name='收盤價')


    # trace2 = go.Bar(x=data['日期'],
    #                 y=data[f'{sub_info}'],
    #                 name=f'{sub_info}',
    #                 marker_color=data[f'{sub_info}買賣顏色'])

    
    # fig = make_subplots(rows=2,
    #                     cols=1,
    #                     shared_xaxes=True,
    #                     row_heights=[0.7, 0.3])
    # fig.add_trace(trace1, row=1, col=1)
    # fig.add_trace(trace2, row=2, col=1)

    # fig.update_layout(title=f'{stock_code}_chart', template='plotly_dark')


    # st.plotly_chart(fig)
    #st.繪圖呈現
# view rawapp.py hosted with ❤ by GitHub