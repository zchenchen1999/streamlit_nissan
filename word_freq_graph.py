import streamlit as st
import plotly.graph_objs as go
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.express as px
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
        df.drop(['Unnamed: 0'], axis=1,inplace=True)
        date_format = '%Y.%m.%d'
        df['post_time'] = df['post_time'].apply(lambda x: datetime.datetime.strptime(x, date_format).date())
    except:
        print("讀取資料失敗，請檢查路徑")
    return df
    #會返回一個DF
df = get_df("data/dtm_result.csv")

# --------------------------------- 設定基本資料 -------------------------------- #

# 資料內最早、最晚出現時間
min_day = datetime.datetime.strptime('2022.10.12', '%Y.%m.%d').date()
max_day = df['post_time'].max()
# 構面清單
aspect_list = ['成就感', '學習成長','創新', '薪資', '福利', '管理制度', '工作氛圍', '同事互動', '主管風格', '工作地點', '公司規模','工作環境', '產業前景', '輪調', '外派', '出差', '引擎', '馬力', '避震', '外觀', '操控', '安全','堅固', '配備', '價錢', '科技', '品質', '折舊', '品牌', '空間', '保養', '續航', '尺寸', '車種','驅動', '變速箱', '電資', '機械', '製造', '車輛工程', '品管', '多元性', '企業社會責任', '企業永續目標','面試', '徵才', '實習', '工作', '離職', '轉職', '新鮮人', '畢業', '出路', '能力', '招募人員','正向', '負向']

# ---------------------------------- sidebar --------------------------------- #

st.sidebar.header('參數設定')
# 日期選擇器
start_date = st.sidebar.date_input(label='選擇起始日期', value=min_day, min_value=min_day, max_value=max_day)
end_date = st.sidebar.date_input(label='選擇結束日期', value=start_date, min_value=start_date, max_value=max_day)
# 單選列表
# aspect_option = st.sidebar.selectbox('選擇構面',aspect_list)
# 多選列表
aspect_option = st.sidebar.multiselect('選擇構面', aspect_list)

# ----------------------------------- body ----------------------------------- #
# st.image('./icon.png')
st.title('面試趣-構面討論趨勢圖')

# ----------------------------------- plotly --------------------------------- #

if start_date and end_date and aspect_option:
    #如果stock_code與month都有值的話，則畫圖
    df_select = df[(df['post_time'] >= start_date) & (df['post_time'] <= end_date)]
    if (df_select.shape[0] == 0):
        st.warning('時間區間內無資料 !')
    else:
        st.success(f'資料篩選成功，共有 {df_select.shape[0]} 筆面試資料!')
        # 要呈現給 user 的資料欄位
        df_display = df_select[['vacancies', 'post_time', 'content']]
        st.dataframe(data=df_display)

        # ----------------------------------- 設定每個月出現次數字典 --------------------------------- #
        # 生成日期範圍並轉換為所需的字符串格式
        #
        date_range = pd.date_range(start="{}-{}".format(start_date.year, start_date.month), end="{}-{}".format(end_date.year+1 if end_date.month == 12 else end_date.year , 1 if end_date.month == 12 else end_date.month), freq='M').strftime('%Y-%m').tolist()
        # result_dict = {date: 0 for date in date_range}
        all_aspect_count = pd.DataFrame(date_range, columns=['year_month'])

        for a in aspect_option:
            # 創建字典，將每個日期設置為0
            tmp_dict = {date: 0 for date in date_range}
            grouped = pd.DataFrame(df_select.groupby(df_select['p_year_month'])[a].sum()).reset_index()
            # 將每個月構面出現次數加入 dict
            for index, row in grouped.iterrows():
                tmp_dict[row['p_year_month']] = row[a]
            # add this aspect result to all list
            all_aspect_count[a] = tmp_dict.values()
        # 轉換成 tidt data (long data)
        all_aspect_count = pd.melt(all_aspect_count, id_vars=all_aspect_count.columns[0], value_vars=all_aspect_count.columns[1:])

        # ---------------------------------------- 畫折線圖 --------------------------------------- #

        # 直接利用 dataframe 的 long format (Tidy data) 來畫圖， X=> 時間, Y=> 數量, color=> 不同構面
        fig = px.line(all_aspect_count, x=all_aspect_count.year_month, y=all_aspect_count.value, color=all_aspect_count.variable, markers=True)
        line_chart_title = "[時間區間]："+start_date.strftime("%Y/%m/%d") + "~" + end_date.strftime("%Y/%m/%d")
        fig.update_layout(title=line_chart_title, template='plotly_dark', xaxis_title="日期", yaxis_title="次數", showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

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


    #st.繪圖呈現
# view rawapp.py hosted with ❤ by GitHub