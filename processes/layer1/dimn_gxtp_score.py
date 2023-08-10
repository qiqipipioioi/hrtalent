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


def cal_gxtp_score(df_base, df_jiating, df_jianzhi):
    #家庭成员得分
    df_jiating_g = df_jiating[df_jiating.notnull().all(axis=1)].groupby('a0188').count()

    def cal_num_score(x):
        score = 0
        if x == 1:
            score = 90
        else:
            score = 90 + (x - 1) * 5
        return score
    
    df_jiating_g = df_jiating_g[['name']]
    df_jiating_g.rename(columns={'name': '完整条数'}, inplace=True)

    df_jiating_g['base_jtcy_score'] = df_jiating_g['完整条数'].apply(cal_num_score)


    #社会兼职
    df_jianzhi_g = df_jianzhi.groupby('a0188').count()
    df_jianzhi_g['base_shgx_score'] = df_jianzhi_g['recordid'] * 50



    #合并结果
    df_result = pd.merge(df_base[['a0188']], df_jiating_g[['base_jtcy_score']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_jianzhi_g[['base_shgx_score']], on='a0188', how='left')
    df_result.fillna(0, inplace=True)

    return df_result

