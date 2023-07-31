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


def cal_working_growing_up_score(now_year):

    now_year = int(now_year)

    #考核得分计算
    def cal_kaohe_score(x):
        if x['考核情况'] == '优秀':
            return 100
        elif x['考核情况'] == '称职':
            return 80
        elif x['考核情况'] == '基本称职':
            return 60
        elif x['考核情况'] == '不称职':
            return 40

    #计算5年考核得分
    def cal_5year_score(x):
        score = 0
        if x['年度'].min() <= now_year - 5:
            score = x['考核得分'].mean()
        else:
            score = 0
        return score

    #计算3年考核得分
    def cal_3year_score(x):
        score = 0
        if x['年度'].min() <= now_year - 3:
            score = x['考核得分'].mean()
        else:
            score = 0
        return score


    #年度考核
    df_kaohe = pd.read_excel('seqdata\年度考核子集_20230504141856.xlsx', dtype=str)
    df_kaohe = df_kaohe[df_kaohe['任职形式'] == '担任']
    df_kaohe['年度'] = df_kaohe['年度'].astype(int)
    df_kaohe['考核得分'] = df_kaohe.apply(cal_kaohe_score, axis=1)
    df_kaohe_5year = df_kaohe[df_kaohe['年度'].apply(lambda x: x >= now_year - 5 and x <= now_year - 1)]
    df_kaohe_3year = df_kaohe[df_kaohe['年度'].apply(lambda x: x >= now_year - 3 and x <= now_year - 1)]
    df_kaohe_5year_g = df_kaohe_5year.groupby(['员工号']).apply(cal_5year_score)
    df_kaohe_3year_g = df_kaohe_3year.groupby(['员工号']).apply(cal_3year_score)
    df_kaohe_5year_g.rename('5年内考核评分成长',inplace=True)
    df_kaohe_3year_g.rename('3年内考核评分成长',inplace=True)


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
        if x['年度'].min() <= now_year - 5:
            score = x['龙虎榜得分'].mean()
        else:
            score = 0
        return score

    def cal_longhu_3year_score(x):
        score = 0
        if x['年度'].min() <= now_year - 3:
            score = x['龙虎榜得分'].mean()
        else:
            score = 0
        return score


    df_longhu = pd.read_excel('seqdata\龙虎榜排名_20230509153725.xlsx', dtype=str)
    df_longhu['年度'] = df_longhu['年度'].astype(int)
    df_xulie = pd.read_excel('seqdata\员工序列表.xlsx', dtype=str)
    df_longhu= pd.merge(df_longhu, df_xulie[['员工号', '二级序列']], on = '员工号', how='left')
    df_longhu['二级序列'].fillna('未知分类', inplace=True)
    df_longhu['月均绩效金额'].fillna(0, inplace=True)
    df_longhu['月均绩效金额'] = df_longhu['月均绩效金额'].astype(float)
    df_longhu['rank'] = df_longhu.groupby(['年度','二级序列'])['月均绩效金额'].rank(ascending=False)
    total_counts = df_longhu.groupby(['年度', '二级序列'])['员工号'].count()
    df_longhu['龙虎榜排名1'] = df_longhu.apply(lambda x: str(int(x['rank'])) + '/' + str(total_counts[x['年度'], x['二级序列']]), axis=1 )


    df_longhu['龙虎榜得分'] = df_longhu.apply(cal_longhu_score, axis=1)
    df_longhu_5year = df_longhu[df_longhu['年度'].apply(lambda x: x >= now_year - 5 and x <= now_year - 1)]
    df_longhu_3year = df_longhu[df_longhu['年度'].apply(lambda x: x >= now_year - 3 and x <= now_year - 1)]
    df_longhu_5year_g = df_longhu_5year.groupby(['员工号']).apply(cal_longhu_5year_score)
    df_longhu_3year_g = df_longhu_3year.groupby(['员工号']).apply(cal_longhu_3year_score)
    df_longhu_5year_g.rename('5年内龙虎榜成长',inplace=True)
    df_longhu_3year_g.rename('3年内龙虎榜成长',inplace=True)


    #员工统计
    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '入行时间', '任现岗位时间','行员等级']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]


    df_result = pd.merge(df_base[['员工号']], df_kaohe_5year_g, on='员工号', how='left')
    df_result = pd.merge(df_result, df_kaohe_3year_g, on='员工号', how='left')
    df_result = pd.merge(df_result, df_longhu_5year_g, on='员工号', how='left')
    df_result = pd.merge(df_result, df_longhu_3year_g, on='员工号', how='left')

    df_result.fillna(0,inplace=True)

    df_result['绩效考核成长得分'] = 0.25 * (df_result['5年内考核评分成长'] + df_result['3年内考核评分成长'] + df_result['5年内龙虎榜成长'] + df_result['3年内龙虎榜成长'])

    return df_result





