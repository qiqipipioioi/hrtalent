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
from models.layer1_model import Tability,A01,Tpersonality,E01

def cal_ability_evaluation_score(session):
    # 岗位编码
    position_code = pd.read_sql(session.query(E01).statement, session.bind)

    #综合能力测评得分
    df_nengli = pd.read_sql(session.query(Tability).statement, session.bind)

    df_nengli['综合能力得分'] = df_nengli['totalscore'].astype(float) / 8 * 100
    df_nengli = df_nengli[['a0188', '综合能力得分']].groupby('a0188').max()

    #性格评测得分
    df_xingge = pd.read_sql(session.query(Tpersonality).statement, session.bind)
    df_xingge['性格测试得分'] = df_xingge['dominance'].astype(int) + df_xingge['compliance'].astype(int) + df_xingge['influence'].astype(int) + df_xingge['steadiness'].astype(int)
    df_xingge = df_xingge[['a0188', '性格测试得分']].groupby('a0188').max()

    #员工统计
    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a01687']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['dept_code'] != position_code.loc[position_code['mc0000']=='高管','dept_code']]
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['a0188']], df_nengli, on='a0188', how='left')
    df_result = pd.merge(df_result, df_xingge, on='a0188', how='left')
    df_result.fillna(0, inplace=True)

    return df_result