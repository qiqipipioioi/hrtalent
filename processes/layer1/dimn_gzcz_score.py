'''
工作成长得分
'''

#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
import re
from models.layer1_model import A01,A875,Gxlygydjx,E01


def cal_working_growing_up_score(now_year,session):

    now_year = int(now_year)

    # 岗位编码
    position_code = pd.read_sql(session.query(E01).statement, session.bind)

    #考核得分计算
    def cal_kaohe_score(x):
        if x['khqk'] == '优秀':
            return 100
        elif x['khqk'] == '称职':
            return 80
        elif x['khqk'] == '基本称职':
            return 60
        elif x['khqk'] == '不称职':
            return 40

    # #计算5年考核得分
    # def cal_5year_score(x):
    #     score = 0
    #     if x['a8759'].min() <= now_year - 5:
    #         score = x['考核得分'].mean()
    #     else:
    #         score = 0
    #     return score
    #
    # #计算3年考核得分
    # def cal_3year_score(x):
    #     score = 0
    #     if x['a8759'].min() <= now_year - 3:
    #         score = x['考核得分'].mean()
    #     else:
    #         score = 0
    #     return score


    #年度考核
    df_kaohe = pd.read_sql(session.query(A875).statement, session.bind)
    df_kaohe = df_kaohe[df_kaohe['任职形式'] == '担任'] # TODO 没有任职形式字段
    df_kaohe['a8759'] = df_kaohe['a8759'].astype(int)
    df_kaohe['考核得分'] = df_kaohe.apply(cal_kaohe_score, axis=1)
    # df_kaohe_5year = df_kaohe[df_kaohe['a8759'].apply(lambda x: x >= now_year - 5 and x <= now_year - 1)]
    # df_kaohe_3year = df_kaohe[df_kaohe['a8759'].apply(lambda x: x >= now_year - 3 and x <= now_year - 1)]
    # df_kaohe_5year_g = df_kaohe_5year.groupby(['a0188']).apply(cal_5year_score)
    # df_kaohe_3year_g = df_kaohe_3year.groupby(['a0188']).apply(cal_3year_score)
    # df_kaohe_5year_g.rename('5年内考核评分成长',inplace=True)
    # df_kaohe_3year_g.rename('3年内考核评分成长',inplace=True)
    df_kaohe_past = df_kaohe[df_kaohe['a8759'].apply(lambda x:x>=now_year - 5 and x<=now_year-1)]
    df_kaohe_past.drop('a8759',axis=1,inplace=True)
    df_kaohe_past = df_kaohe_past.groupby(['a0188']).mean()
    df_kaohe_past.rename(columns={'考核得分':'考核评分成长'},inplace=True)

    #过往绩效
    def cal_longhu_score(x):
        a, b = x['龙虎榜排名'].split('/')
        a = int(a)
        b = int(b)

        score = 0
        if 0 <= b and b < 5:
            if a == 1:
                score = 100
            else:
                score = 80
        elif 5 <= b and b < 15:
            if a == 1:
                score = 100
            elif a == b:
                score = 70
            else:
                score = 80
        elif 15 <= b and b < 30:
            if a == 1:
                score = 100
            elif a == 2:
                score = 95
            elif a == 3:
                score = 90
            elif b - 1 <= a and a <= b:
                score = 60
            else:
                score = 80
        elif 30 <= b and b < 50:
            if a == 1:
                score = 100
            elif a == 2:
                score = 95
            elif a == 3:
                score = 90
            elif a == 4:
                score = 85
            elif a == 5:
                score = 80
            elif b - 2 <= a and a <= b:
                score = 60
            else:
                score = 75
        elif 50 <= b and b < 100:
            if a == 1:
                score = 100
            elif a == 2:
                score = 95
            elif a == 3:
                score = 90
            elif a == 4:
                score = 85
            elif 5 <= a and a <= 8:
                score = 80
            elif b - 2 <= a and a <= b:
                score = 60
            else:
                score = 75
        elif 100 <= b and b <= 200:
            if a == 1 or a == 2:
                score = 100
            elif 3 <= a and a <= 5:
                score = 95
            elif 5 < a and a <= 8:
                score = 90
            elif 8 < a and a <= 10:
                score = 85
            elif 10 < a and a <= 15:
                score = 80
            elif b - 7 <= a and a <= b:
                score = 60
            else:
                score = 75
        elif 200 < b:
            if 1 <= a and a <= int(0.01 * b):
                score = 100
            elif int(0.01 * b) <= a and a <= int(0.03 * b):
                score = 95
            elif int(0.03 * b) < a and a <= int(0.05 * b):
                score = 90
            elif int(0.05 * b) < a and a <= int(0.08 * b):
                score = 85
            elif int(0.08 * b) < a and a <= int(0.12 * b):
                score = 80
            elif int(0.95 * b) <= a and a <= b:
                score = 60
            else:
                score = 75   
        return score


    def cal_longhu_5year_score(x):
        score = 0
        if x['year'].min() <= now_year - 5:
            score = x['龙虎榜得分'].mean()
        else:
            score = 0
        return score

    def cal_longhu_3year_score(x):
        score = 0
        if x['year'].min() <= now_year - 3:
            score = x['龙虎榜得分'].mean()
        else:
            score = 0
        return score


    df_longhu = pd.read_sql(session.query(Gxlygydjx).statement, session.bind)
    df_longhu['year'] = df_longhu['year'].astype(int)
    df_xulie = pd.read_excel('seqdata\员工序列表.xlsx', dtype=str) # TODO 没有员工序列表
    df_longhu= pd.merge(df_longhu, df_xulie[['a0188', '二级序列']], on = 'a0188', how='left')
    df_longhu['二级序列'].fillna('未知分类', inplace=True)
    df_longhu['yjjxje'].fillna(0, inplace=True)
    df_longhu['yjjxje'] = df_longhu['yjjxje'].astype(float)
    df_longhu['rank'] = df_longhu.groupby(['year','二级序列'])['yjjxje'].rank(ascending=False)
    total_counts = df_longhu.groupby(['year', '二级序列'])['a0188'].count()
    df_longhu['龙虎榜排名1'] = df_longhu.apply(lambda x: str(int(x['rank'])) + '/' + str(total_counts[x['year'], x['二级序列']]), axis=1 )


    df_longhu['龙虎榜得分'] = df_longhu.apply(cal_longhu_score, axis=1)
    # df_longhu_5year = df_longhu[df_longhu['year'].apply(lambda x: x >= now_year - 5 and x <= now_year - 1)]
    # df_longhu_3year = df_longhu[df_longhu['year'].apply(lambda x: x >= now_year - 3 and x <= now_year - 1)]
    # df_longhu_5year_g = df_longhu_5year.groupby(['a0188']).apply(cal_longhu_5year_score)
    # df_longhu_3year_g = df_longhu_3year.groupby(['a0188']).apply(cal_longhu_3year_score)
    # df_longhu_5year_g.rename('5年内龙虎榜成长',inplace=True)
    # df_longhu_3year_g.rename('3年内龙虎榜成长',inplace=True)
    df_longhu_past = df_kaohe[df_kaohe['year'].apply(lambda x: x >= now_year - 5 and x <= now_year - 1)]
    df_longhu_past.drop('year', axis=1, inplace=True)
    df_longhu_past = df_kaohe_past.groupby(['a0188']).mean()
    df_longhu_past.rename(columns={'龙虎榜得分': '龙虎榜成长'}, inplace=True)

    #员工统计
    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a0141', 'a01145','a01686']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任'] # TODO 没有任职形式
    df_base = df_base[df_base['dept_code'] != position_code.loc[position_code['mc0000']=='高管','dept_code']]
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]


    # df_result = pd.merge(df_base[['a0188']], df_kaohe_5year_g, on='a0188', how='left')
    # df_result = pd.merge(df_result, df_kaohe_3year_g, on='a0188', how='left')
    # df_result = pd.merge(df_result, df_longhu_5year_g, on='a0188', how='left')
    # df_result = pd.merge(df_result, df_longhu_3year_g, on='a0188', how='left')
    #
    # df_result.fillna(0,inplace=True)
    #
    # df_result['绩效考核成长得分'] = 0.25 * (df_result['5年内考核评分成长'] + df_result['3年内考核评分成长'] + df_result['5年内龙虎榜成长'] + df_result['3年内龙虎榜成长'])

    df_result = pd.merge(df_base[['a0188']],df_kaohe_past,on='a0188',how='left')
    df_result = pd.merge(df_result,df_longhu_past,on='a0188',how='left')

    df_result['绩效考核成长得分'] = 0.5 * df_result['考核评分时常'] + 0.5 * df_result['龙虎榜成长']

    return df_result





