from pymongo import MongoClient
import configparser
import pandas as pd
import re
from nltk.corpus import wordnet
import numpy as np
from flask import Flask, render_template


## preprocess
# Load csv file
df_ = pd.read_csv('./total/interview_clean_tokenize_with_marks.csv', encoding='utf-8')
df_open = df_[~df_['suggestion'].isna()].reset_index(drop=True)
_df = df_open[['aID','company_name', 'vacancies', 'post_time', 'content', 'sentence','word']]
_df.rename(columns = {'content':'result'}, inplace = True)
_df = _df[~_df['vacancies'].str.contains('客服|專員')].reset_index(drop='index')
_df['word'] = _df['word'].apply(lambda x: eval(x))

# # 篩選公司
# company_name = "裕隆集團_裕隆汽車製造股份有限公司"
# _df = _df[_df['company_name'] == company_name].reset_index(drop='index')

# 構面字典
dict_ = pd.read_csv('./構面字典_4.csv')
df_dict = dict_[['name','alias']]
d_list = df_dict.to_dict(orient='records')
structure_dict = {} # 構面字典 => name:alias
for i in d_list:
    structure_dict[i['name']] = i['alias']
structure_dict.keys()#key:成就感,...
structure_origin = dict_[['class','name']]
structures_list = structure_origin['class'].unique().tolist() # 有哪些構面字陣列
structure_origin_list = pd.DataFrame(structure_origin.groupby('class')['name'].apply(list)).reset_index().to_dict(orient='records')
transformed_data = [{item['class']: item['name']} for item in structure_origin_list] # 取得構面字典，型態為list of dict
new_dict = {}
for i in transformed_data:
    new_dict[list(i.keys())[0]] = list(i.values())[0]
print("--------load dict done--------")

## Function
# 用斷完的詞去計算構面字的數量
def get_dict_num(pattern_text, word_list):
    count = 0
    for i in word_list:
        for j in structure_dict[pattern_text].split('|'):
            if i == j:
                count += 1
    return count
# 用構面字去找對應的class
def get_class_by_subclass(sub_class):
    for k, v in new_dict.items():
        if (sub_class in v):
            return k
# 將文章轉為dict
dict_ = _df.to_dict(orient='records')
# 計算構面字數量
for structure in list(structure_dict.keys()):
    for data in dict_:
        data[structure] = get_dict_num(structure, data['word'])
# 計算情緒分數
for data in dict_:
    data['sensitive_value'] = data['正向']-data['負向']
# 去除不需要的斷詞欄位，剩下的資料為畫趨勢圖的dtm
data_list = [{k: v for k, v in d.items() if k not in ['word']} for d in dict_]
# 得到for 趨勢圖的 DTM DataFrame
dtm_df = pd.DataFrame(data_list)
# 求算correlation&cooccurrence 的dtm_co
kick_off_ = ['aID','post_time','result','sentence','company_name','vacancies','word','sensitive_value']
co_ = [{k: v for k, v in d.items() if k not in kick_off_} for d in dict_]
dtm_co = pd.DataFrame(co_)
print("--------calculate dtm done--------")

## correlation
df_corre = pd.DataFrame(np.corrcoef(dtm_co.T),columns=dtm_co.columns, index=dtm_co.columns)
df_corre = df_corre.reset_index()
df_corre.rename(columns={'index': 'item1'}, inplace=True)
corr_df = pd.melt(df_corre, id_vars='item1', value_vars=list(df_corre.columns)[1:], var_name='item2', value_name='value')
corr_df.rename(columns={'index':'item1'},inplace=True)
corr_df = corr_df[~corr_df['value'].isnull()].reset_index(drop='index')
corr_df['class'] = corr_df['item1'].apply(lambda x: get_class_by_subclass(x))

## cooccurrence
result_CoOc = np.dot(dtm_co.T.values, dtm_co.values)
CoOc_df = pd.DataFrame(result_CoOc, columns=dtm_co.columns, index=dtm_co.columns)
df_ocurr_vect = CoOc_df.reset_index()
df_ocurr_vect.rename(columns={'index': 'item1'}, inplace=True)
ocurr_df = pd.melt(df_ocurr_vect, id_vars='item1', value_vars=list(df_ocurr_vect.columns)[1:], var_name='item2', value_name='value')
ocurr_df.rename(columns={'index':'item1'},inplace=True)
ocurr_df = ocurr_df[~ocurr_df['value'].isnull()].reset_index(drop='index')
ocurr_df['class'] = ocurr_df['item1'].apply(lambda x: get_class_by_subclass(x))

## save
print("dtm shape:",dtm_df.shape)
dtm_df.to_csv('./test/interview/interview_word_dict_dtm_TWM.csv', encoding='utf-8-sig')
corr_df.to_csv('./test/interview/interview_word_dict_corre_TWM.csv', encoding='utf-8-sig')
ocurr_df.to_csv('./test/interview/interview_word_dict_CoOcurr_TWM.csv', encoding='utf-8-sig')