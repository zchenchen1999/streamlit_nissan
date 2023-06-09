import streamlit as st
import plotly.graph_objs as go
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.express as px
import pandas as pd
import datetime
import json

# 預設顯示 wide mode
st.set_page_config(layout="wide")
#利用st.cache()快取沒有改變過的data
# @st.cache()
def get_df(path=None):
    # 轉換日期
    date_format = '%Y.%m.%d'
    try:
        df = pd.read_csv(path)
        df.drop(['Unnamed: 0'], axis=1,inplace=True)
        date_format = '%Y.%m.%d'
        df['post_time'] = df['post_time'].apply(lambda x: datetime.datetime.strptime(x, date_format).date())
        # 篩選掉不要的職位
        df = df[~df['vacancies'].str.contains('客服|專員')]
    except:
        print("讀取資料失敗，請檢查路徑")
    return df
    #會返回一個DF
df = get_df("data/dtm_corre_cooc/interview/interview_word_dict_dtm_TWM.csv")

# --------------------------------- 設定基本資料 -------------------------------- #

# 資料內最早、最晚出現時間
min_day = datetime.datetime.strptime('2022.10.12', '%Y.%m.%d').date()
max_day = df['post_time'].max()


# 公司清單
company_list = list(df['company_name'].unique())
# company_list.insert(0, "全部")

# 構面字典
tf = open("./data/aspect.json", "r")
aspect_dict = json.load(tf)
# 依照 value 找 key
def get_class_by_subclass(sub_class):
    for k, v in aspect_dict.items():
        if (sub_class in v):
            return k

# 構面清單
# aspect_list = ['成就感', '學習成長', '創新', '薪資', '福利', '管理制度', '工作氛圍', '同事互動', '主管風格', '工作地點', '公司規模', '工作環境', '產業前景', '多元性', '企業社會責任', '企業永續目標', '變化性', '工學院', '面試', '徵才', '實習', '工作', '離職', '轉職', '新鮮人', '畢業', '出路', '能力', '招募人員', '正向', '負向']
aspect_list = []
for k, v in aspect_dict.items():
    for i in v:
        aspect_list.append(i)


# --------------------------- 定義趨勢圖呈現資料處理函式 ------------------------- #

def get_companys_counts_by_aspect(companys, df, start_date, end_date):
    # 生成日期範圍並轉換為所需的字符串格式
    # ----------------------------------- 設定每個月出現次數字典 --------------------------------- #
    date_range = pd.date_range(start="{}-{}".format(start_date.year, start_date.month), end="{}-{}".format(end_date.year+1 if end_date.month == 12 else end_date.year , 1 if end_date.month == 12 else end_date.month+1), freq='M').strftime('%Y-%m').tolist()
    all_company_count = pd.DataFrame(date_range, columns=['year_month'])
    # 每間公司
    for c in companys:
        # 篩選出公司資料
        company_df = df[df['company_name'] == c]
        # 創建字典，將每個日期設置為0
        tmp_dict = {date: 0 for date in date_range}
        # 以年月來 group，將那個月的構面出現的文章數相加
        grouped = pd.DataFrame(company_df.groupby(company_df['p_year_month']).count()).reset_index()
        # 將每個月構面出現次數加入 dict
        for index, row in grouped.iterrows():
            tmp_dict[row['p_year_month']] = row["company_name"]
        # 將這個公司計算結過加入此構面結果
        all_company_count[c] = tmp_dict.values()
    # 轉換成 tidy data (long data)
    all_company_count = pd.melt(all_company_count, id_vars=all_company_count.columns[0], value_vars=all_company_count.columns[1:])

    return all_company_count

# ---------------------------------- sidebar --------------------------------- #

st.sidebar.header('參數設定')
# 日期選擇器
start_date = st.sidebar.date_input(label='選擇起始日期', value=min_day, min_value=min_day, max_value=max_day)
end_date = st.sidebar.date_input(label='選擇結束日期', value=max_day, min_value=start_date, max_value=max_day)
# 單選列表
company_option = st.sidebar.multiselect('選擇公司', company_list)

# # 構面選擇器 label 呈現 format
def label_foramt(option):
    return f'[{get_class_by_subclass(option)}] - {option}'

# 多選列表
aspect_option = st.sidebar.multiselect('選擇構面', aspect_list, format_func=label_foramt)

# ----------------------------------- body ----------------------------------- #
# st.image('./icon.png')
st.title('面試趣-構面討論趨勢圖')

# ----------------------------------- plotly --------------------------------- #

if start_date and end_date and aspect_option:
    #如果stock_code與month都有值的話，則畫圖
    df_select = df[(df['post_time'] >= start_date) & (df['post_time'] <= end_date)]
    df_select = df_select.loc[df_select['company_name'].isin(company_option)]
    # if (company_option != "全部" and company_option != None):
    #     df_select = df_select[df_select['company_name'] == company_option]
    if (df_select.shape[0] == 0):
        st.warning('時間區間內無資料 !')
    else:
        # 創建所有構面的 tab 顯示頁面
        aspect_option.append("共現構面")
        tab_name_list = aspect_option.copy()
        # tab_name_list.append("共現構面")
        tab_list_trend = st.tabs(tab_name_list)
        for i in range(len(tab_list_trend)):
            # 篩選構面
            if (tab_name_list[i] == "共現構面"):
                # 共現構面利用所有選擇構面去篩選 data
                df_tmp = df_select
                for a in aspect_option:
                    if (a != "共現構面"):
                        df_tmp = df_tmp[df_tmp[a] > 0]
            else:
                df_tmp = df_select[df_select[aspect_option[i]]> 0]
            # ---------------------------------------- 呈現趨勢圖 --------------------------------------- #
            # 取得計算資料
            tidy_data = get_companys_counts_by_aspect(company_option, df_tmp, start_date, end_date)
            fig = px.line(tidy_data, x=tidy_data.year_month, y=tidy_data.value, color=tidy_data.variable, markers=True)
            line_chart_title = "[時間區間]："+start_date.strftime("%Y/%m/%d") + "~" + end_date.strftime("%Y/%m/%d")
            fig.update_layout(title=line_chart_title, template='plotly_dark', xaxis_title="日期", yaxis_title="次數", showlegend=True)
            # 在此頁籤中畫圖
            tab_list_trend[i].plotly_chart(fig, use_container_width=True)

            # ---------------------------------------- 呈現 dataframe --------------------------------------- #
            df_tmp.reset_index(drop=True, inplace=True)
            df_tmp = df_tmp[['company_name', 'vacancies', 'post_time', 'sentence', 'sensitive_value']]
            tab_list_trend[i].success(f'{tab_name_list[i]}{"" if tab_name_list[i] == "共現構面" else "構面"}資料共有 {df_tmp.shape[0]} 筆面試資料!')
            # 在此頁籤中呈現 dataframe
            tab_list_trend[i].dataframe(data=df_tmp, use_container_width=True)