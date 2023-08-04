'''
计算违规惩处扣分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
import re
from models.layer1_model import A01,A8145,A8192,E01


def cal_punish_score(now_year,session):

    now_year = int(now_year)

    # 岗位编码
    position_code = pd.read_sql(session.query(E01).statement, session.bind)

    df_weigui = pd.read_sql(session.query(A8145).statement, session.bind)

    #当年违规惩处积分
    df_weigui_now = df_weigui[df_weigui['a81452'].apply(lambda x: x.year == str(now_year))]
    df_weigui_now['a81453'] = df_weigui_now['a81453'].astype(float)

    df_weigui_now_group = df_weigui_now[['a0188', 'a81453']].groupby(['a0188']).sum().reset_index()

    def cal_weigui_score_now(x):
        if x >= 100:
            return -100
        elif 70 <= x and x < 100:
            return -80
        elif 50 <= x and x < 70:
            return -60
        elif 40 <= x and x < 50:
            return -50
        elif 30 <= x and x < 40:
            return -40
        elif 20 <= x and x < 30:
            return -30
        elif 10 <= x and x < 20:
            return -20
        else:
            return 0


    df_weigui_now_group['当年违规惩处扣分'] = df_weigui_now_group['a81453'].apply(cal_weigui_score_now)


    #过去违规惩处扣分
    df_weigui_past = df_weigui[df_weigui['a81452'].apply(lambda x: int(x.year) < now_year)]
    df_weigui_past['a81453'] = df_weigui_past['a81453'].astype(float)


    def cal_weigui_past_score(x, now_year):
        sum_score = 0
        max_year = 0
        x.pop(0)
        for p in x:
            y = p[0].year
            if y > max_year:
                max_year = y
            this_score = 0
            if p[1] >= 100:
                this_score = -100
            elif 70 <= p[1] and p[1] < 100:
                this_score = -80
            elif 50 <= p[1] and p[1] < 70:
                this_score = -60
            elif 40 <= p[1] and p[1] < 50:
                this_score = -50
            elif 30 <= p[1] and p[1] < 40:
                this_score = -40
            elif 20 <= p[1] and p[1] < 30:
                this_score = -30
            elif 10 <= p[1] and p[1] < 20:
                this_score = -20
            else:
                this_score = 0
            sum_score += this_score
        near = now_year - max_year
        coe = 1
        if near > 5:
            coe = 0
        elif 5 >= near and near > 3:
            coe = 0.3
        elif 3 >= near and near > 1:
            coe = 0.5    
        elif near <= 1:
            coe = 0.8
        final_score = sum_score * coe
        return final_score


    df_weigui_past_group = df_weigui_past[['a0188', 'a81452', 'a81453']].groupby(['a0188']).apply(lambda x: cal_weigui_past_score(x.values.tolist(), now_year))

    df_weigui_past_group.rename('累计违规扣分',inplace=True)

    #员工统计
    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a0141', 'a01145','a01686']]

    #筛选出非高管和首席的员工
    # df_base = df_base[df_base['任职形式'] == '担任'] # TODO 没有任职形式字段
    df_base = df_base[df_base['dept_code'] != position_code.loc[position_code['mc0000']=='高管','dept_code']]
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['a0188', 'a0101']], df_weigui_now_group[['a0188', '当年违规惩处扣分']], how='left')
    df_result = pd.merge(df_result, df_weigui_past_group, on='a0188', how='left')

    df_result.fillna(0, inplace=True)

    #违规惩处数据
    df_chengchu = pd.read_sql(session.query(A8192).statement, session.bind)


    def cal_single_chengchu_score(x):
        score = 0
        if re.search('降级|察看|撤职|开除|降职|解除劳动合同|解聘', x):
            score = -100
        elif re.search('大过|党内严重警告', x):
            score = -80
        elif re.search('记过|党内警告', x):
            score = -60
        elif re.search('警告', x):
            score = -40
        elif re.search('通报批评|谈话|经济处罚|罚款|扣减|函询|清收|书面检查', x):
            score = -20
        else:
            score = 0
        return score
    

    df_chengchu['单一惩处扣分'] = df_chengchu['a81923'].apply(cal_single_chengchu_score)

    #当年惩处
    df_chengchu_now = df_chengchu[df_chengchu['a81921'].astype(int) == now_year]
    df_chengchu_now_g = df_chengchu_now[['a0101', '单一惩处扣分']].groupby('a0101').sum()
    df_chengchu_now_g.rename(columns = {'单一惩处扣分': '当年违规惩处扣分'}, inplace=True)


    def cal_chengchu_score(x, now_year):
        max_year = 0
        sum_score = 0
        for p in x:
            if int(p[0]) > max_year:
                max_year = int(p[0])
            sum_score += p[1]
        from_now = now_year - max_year
        coe = 1
        if from_now == 1:
            coe = 0.8
        elif 3 <= from_now < 1:
            coe = 0.5
        elif 5 <= from_now < 3:
            coe = 0.3
        elif 8 <= from_now < 5:
            coe = 0.1
        elif from_now > 8:
            coe = 0
        final_score = sum_score * coe
        return final_score


    #往年惩处扣分
    df_chengchu_past = df_chengchu[df_chengchu['a81921'].astype(int) < now_year]
    df_chengchu_past_g = df_chengchu_past[['a0101', 'a81921', '单一惩处扣分']].groupby('a0101').apply(lambda x: cal_chengchu_score(x.values.tolist(), now_year))
    df_chengchu_past_g.rename('过去违规惩处扣分', inplace=True)


    df_names1 = pd.merge(df_chengchu_now_g, df_result, on='a0101', how='left', indicator=True)
    df_names1 = df_names1[df_names1['_merge'] == 'both']
    du_names1 = set(df_names1[df_names1['a0101'].duplicated()]['a0101'].values.tolist())
    df_names2 = pd.merge(df_chengchu_past_g, df_result, on='a0101', how='left', indicator=True)
    df_names2 = df_names2[df_names2['_merge'] == 'both']
    du_names2 = set(df_names2[df_names2['a0101'].duplicated()]['a0101'].values.tolist())
    du_names = du_names1 and du_names2

    df_result = pd.merge(df_result,df_chengchu_now_g, on='a0101', how='left')
    df_result = pd.merge(df_result, df_chengchu_past_g, on='a0101', how='left')

    df_result.fillna(0, inplace=True)


    df_result[df_result['a0101'].apply(lambda x: x in du_names)]['当年违规惩处扣分'] = 0
    df_result[df_result['a0101'].apply(lambda x: x in du_names)]['过去违规惩处扣分'] = 0
    df_result = df_result.drop('a0101', axis=1)


    return df_result