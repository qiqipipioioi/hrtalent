'''
行外工作经历得分计算
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time

def cal_hwjl_score(now_year, df_base, df_working):
    now_year=int(now_year)

    def cal_working_time(x):
        #计算行外工作时间
        x['a8661'] = pd.to_datetime(x['a8661'])
        x['a8662'] = pd.to_datetime(x['a8662'])
        merged_intervals = []
        for _, row in x.iterrows():
            start_time = row['a8661']
            end_time = row['a8662']
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


    df_working_merge_base = pd.merge(df_working, df_base[['a0188', 'a0141', 'a01145']], on='a0188', how='left')

    df_working_merge_base = df_working_merge_base[df_working_merge_base['a8662'] < df_working_merge_base['a0141']]

    df_working_merge_base_g = df_working_merge_base.groupby('a0188').apply(cal_working_time)
    df_working_merge_base_g.rename('过去工作经验得分',inplace=True)

    def cal_hire_type_score(x):
        years = now_year - x['a0141'].year
        past_work_year = x['过去工作经验得分'] / 10
        if past_work_year > 10:
            past_work_year = 10
        coe = past_work_year / 10 * 0.5 + 1
        base_score = 0
        if x['a01679'] in ['熟练用工','人才引进']:
            if years <= 1:
                base_score = 100
            elif 1 <years<=2:
                base_score = 70
            elif 2<years<=3:
                base_score = 40
            else:
                base_score = 0
        else:
            base_score = 0
        return base_score * coe

    df_result = pd.merge(df_base[['a0188','a01679', 'a0141']], df_working_merge_base_g, on='a0188', how='left')
    df_result['base_lylx_score'] = df_result.apply(cal_hire_type_score, axis=1)
    df_result.rename(columns={'过去工作经验得分': 'base_gqgz_score'}, inplace=True)
    df_result.fillna(0, inplace=True)

    df_result = df_result[['a0188', 'base_lylx_score', 'base_gqgz_score']]

    return df_result
