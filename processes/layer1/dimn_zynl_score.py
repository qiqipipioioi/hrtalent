'''
能力评测得分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
import re


def cal_ability_evaluation_score():
    #综合能力测评得分
    # bm_starlevel,胜任力星级
    df_nengli = pd.read_excel('seqdata\综合能力测评_20230706091438.xlsx', dtype=str)

    df_nengli['综合能力得分'] = df_nengli['总分'].astype(float) / 8 * 100
    df_nengli = df_nengli[['员工号', '综合能力得分']].groupby('员工号').max()

    #性格评测得分
    df_xingge = pd.read_excel('seqdata\性格评测_20230509133432.xlsx', dtype=str)
    df_xingge['性格测试得分'] = df_xingge['支配型'].astype(int) + df_xingge['思考型'].astype(int) + df_xingge['影响型'].astype(int) + df_xingge['支持型'].astype(int)
    df_xingge = df_xingge[['员工号', '性格测试得分']].groupby('员工号').max()

    #员工统计
    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '聘任职业技术等级']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['员工号']], df_nengli, on='员工号', how='left')
    df_result = pd.merge(df_result, df_xingge, on='员工号', how='left')
    df_result.fillna(0, inplace=True)

    return df_result