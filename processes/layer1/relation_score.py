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
from models.layer1_model import A01,A864,A865,E01


def cal_relation_score(session):
    # 岗位编码
    position_code = pd.read_sql(session.query(E01).statement, session.bind)

    #家庭成员得分
    df_jiating = pd.read_sql(session.query(A864).statement, session.bind)

    df_jiating_g = df_jiating[df_jiating.notnull().all(axis=1)].groupby('a0188').count()

    def cal_jiating_score(x):
        score = 0
        if x == 1:
            score = 90
        else:
            score = 90 + (x - 1) * 5
        return score


    df_jiating_g = df_jiating_g[['name']]
    df_jiating_g.rename(columns={'name': '完整条数'}, inplace=True)

    df_jiating_g['家庭成员关系得分'] = df_jiating_g['完整条数'].apply(cal_jiating_score)


    #社会兼职
    df_jianzhi = pd.read_sql(session.query(A865).statement, session.bind)
    df_jianzhi_g = df_jianzhi.groupby('a0188').count()
    df_jianzhi_g.rename(columns={'a0188': '完整条数'}, inplace=True)
    df_jianzhi_g['社会关系得分'] = df_jianzhi_g['完整条数'] * 50


    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a0141', 'a01145','a01686']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任'] # TODO 没有任职形式
    df_base = df_base[df_base['dept_code'] != position_code.loc[position_code['mc0000']=='高管','dept_code']]
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['a0188']], df_jiating_g[['家庭成员关系得分']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_jianzhi_g[[ '社会关系得分']], on='a0188', how='left')

    df_result.fillna(0, inplace=True)

    return df_result

