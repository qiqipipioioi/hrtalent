'''
关系拓扑得分计算
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
import re


def cal_relation_score():

    #家庭成员得分
    df_jiating = pd.read_excel('seqdata\jiatingchengyuan.xlsx', dtype=str)

    df_jiating_g = df_jiating[df_jiating.notnull().all(axis=1)].groupby('员工号').count()

    def cal_jiating_score(x):
        score = 0
        if x == 1:
            score = 90
        else:
            score = 90 + (x - 1) * 5
        return score


    df_jiating_g = df_jiating_g[[ '姓名']]
    df_jiating_g.rename(columns={'姓名': '完整条数'}, inplace=True)

    df_jiating_g['家庭成员关系得分'] = df_jiating_g['完整条数'].apply(cal_jiating_score)


    #社会兼职
    df_jianzhi = pd.read_excel('seqdata\社会兼职子集_20230706102550.xlsx', dtype=str)
    df_jianzhi_g = df_jianzhi.groupby('员工号').count()
    df_jianzhi_g.rename(columns={'姓名': '完整条数'}, inplace=True)
    df_jianzhi_g['社会关系得分'] = df_jianzhi_g['完整条数'] * 50


    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '入行时间', '任现岗位时间','行员等级']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['员工号']], df_jiating_g[['家庭成员关系得分']], on='员工号', how='left')
    df_result = pd.merge(df_result, df_jianzhi_g[[ '社会关系得分']], on='员工号', how='left')

    df_result.fillna(0, inplace=True)

    return df_result

