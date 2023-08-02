'''
行外工作经历得分计算
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
from models.layer1_model import BaseInfo,WorkingExperience

def calculate_in_bank_working_experience_score(session):
    
    def cal_working_time(x):
        #计算行外工作时间
        x['起始时间'] = pd.to_datetime(x['起始时间'])
        x['终止时间'] = pd.to_datetime(x['终止时间'])
        merged_intervals = []
        for _, row in x.iterrows():
            start_time = row['起始时间']
            end_time = row['终止时间']
            print(start_time, end_time)
            mark = 0
            for i, interval in enumerate(merged_intervals):
                if (interval[0] <= start_time <= interval[1]) or (interval[0] <= end_time <= interval[1]):
                    print(merged_intervals[i])
                    if mark == 0:
                        merged_intervals[i] = (min(start_time, interval[0]), max(end_time, interval[1]))
                        mark = 1
                    else:
                        merged_intervals[i] = (max(start_time, interval[0]), min(end_time, interval[1]))
            if mark == 0:
                merged_intervals.append((start_time, end_time))

        total_work_time = sum((end_time - start_time).days / 365 for start_time, end_time in merged_intervals)
        return total_work_time * 10


    # df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base = pd.read_sql(session.query(BaseInfo).statement, session.bind)

    # df_base = df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '入行时间', '任现岗位时间','行员等级']]
    df_base = df_base[
        ['user_id', 'name', 'lv1_org', 'lv2_org', 'center', 'position', 'join_time', 'position_time', 'emp_lvl']
    ]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['emp_lvl'] == '担任'] # TODO unclear
    df_base = df_base[df_base['center'] != '高管']
    df_base = df_base[df_base['position'].apply(lambda x: '首席' not in x)]

    df_working = pd.read_sql(session.query(WorkingExperience).statement, session.bind)

    df_working_merge_base = pd.merge(df_working, df_base[['user_id', 'join_time', 'position_time']], on='user_id', how='left')

    df_working_merge_base = df_working_merge_base[df_working_merge_base['end_time'] < df_working_merge_base['start_time']]

    df_working_merge_base_g = df_working_merge_base.groupby('user_id').apply(cal_working_time)
    # df_working_merge_base_g.rename('过去工作经验得分',inplace=True)
    df_working_merge_base_g.rename('pro_seq_years',inplace=True)

    df_result = pd.merge(df_base[['user_id']], df_working_merge_base_g, on='user_id', how='left')
    df_result.fillna(0, inplace=True)


    return df_result

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
if __name__ == '__main__':
    # test
    engine = create_engine('mysql+pymysql://hruser:12345@110.40.154.26:3306/talents', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()

    print(calculate_in_bank_working_experience_score(session=session))
