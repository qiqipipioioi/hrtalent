'''
工作状态得分
'''

#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
import datetime
import time
import os
from models.layer1_model import A01,K_month,A875,Gxlygydjx,E01,Kol,A8187


def calculate_working_status_score(now_year,session):
    #计算工作状态得分

    # 岗位编码
    position_code = pd.read_sql(session.query(E01).statement, session.bind)

    # kol
    df_kol = pd.read_sql(session.query(Kol).statement,session.bind)

    #读取KOL数据    
    # kol_names = os.listdir('seqdata/KOL')
    # df_kol_list = []
    # for kol_name in kol_names:
    #     kol_file = 'seqdata/KOL/' + kol_name
    #     df_temp = pd.read_csv(kol_file, dtype=str)
    #     df_temp['统计年份'] = kol_name.replace('.csv', '')
    #     df_kol_list.append(df_temp)
    # df_kol = pd.concat(df_kol_list, axis=0)
    df_kol.rename(columns = {'a0190': '员工号', 'a0188': '姓名', 'jf': 'KOL积分'}, inplace=True)

    #KOL得分统计
    df_kol_now = df_kol[df_kol['gz_ym'] == now_year]
    kol_now_max_score = df_kol_now['KOL积分'].astype(int).max()

    df_kol_now['KOL得分'] = df_kol_now['KOL积分'].astype(int) / kol_now_max_score * 100

    #日志数据读取
    df_journal = pd.read_sql(session.query(A8187).statement,session.bind)
    # journal_names = os.listdir('seqdata/日志')
    # df_journal_list = []
    # for journal_name in journal_names:
    #     journal_file = 'seqdata/日志/' + journal_name
    #     df_temp = pd.read_excel(journal_file, dtype=str)
    #     df_temp['统计年月'] = journal_name.replace('.xls', '')
    #     df_journal_list.append(df_temp)
    # df_journal = pd.concat(df_journal_list, axis=0)
    # df_journal.rename(columns={'用户CODE': 'a0188'}, inplace=True)
    df_journal_now = df_journal[df_journal['gz_ym'].apply(lambda x: now_year in x)]

    #日志得分统计
    df_journal_now['a81872'] = df_journal_now['a81872'].astype(float)
    df_journal_now['a81873'] = df_journal_now['a81873'].astype(float)
    df_journal_now['a81874'] = df_journal_now['a81874'].astype(float)
    df_journal_now['a81875'] = df_journal_now['a81875'].astype(float)
    df_journal_now['a81876'] = df_journal_now['a81876'].astype(float)
    df_journal_now['a81877'] = df_journal_now['a81877'].astype(float)
    df_journal_now['a81878'] = df_journal_now['a81878'].astype(float)
    df_journal_now['a81879'] = df_journal_now['a81879'].astype(float)
    df_journal_now_by_month = df_journal_now.groupby('a0188').mean().reset_index()

    df_journal_now_by_month['发布数量得分'] = df_journal_now_by_month['a81872'] / df_journal_now_by_month['a81872'].max() * 20
    df_journal_now_by_month['发布字数得分'] = df_journal_now_by_month['a81878'] / df_journal_now_by_month['a81878'].max() * 20
    df_journal_now_by_month['上榜次数得分'] = df_journal_now_by_month['a81879'] / df_journal_now_by_month['a81879'].max() * 20
    df_journal_now_by_month['互动总量得分'] = df_journal_now_by_month['a81877'] / df_journal_now_by_month['a81877'].max() * 20
    df_journal_now_by_month['日志得分'] = df_journal_now_by_month['发布数量得分'] + df_journal_now_by_month['发布字数得分'] + df_journal_now_by_month['上榜次数得分'] + df_journal_now_by_month['互动总量得分']


    #员工统计
    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base = df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a0141', 'a01145','a01686']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['dept_code'] != position_code.loc[position_code['mc0000']=='高管','dept_code']]
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]


    #工具使用情况得分
    df_result = pd.merge(df_base[['a0188']], df_kol_now[['a0188', 'KOL得分']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_journal_now_by_month[['a0188', '日志得分']], on='a0188', how='left')
    df_result.fillna(0, inplace=True)
    df_result['工具使用情况得分'] = df_result['KOL得分'] * 0.5 + df_result['日志得分'] * 0.5

    #考勤数据
    df_kaoqin = pd.read_sql(session.query(K_month).statement, session.bind)

    def cal_kaoqin_score(x):
        if x['事病假天数'] == 0:
            return 100
        elif 0 < x['事病假天数'] and x['事病假天数'] <= 5:
            return 90
        elif 5 < x['事病假天数'] and x['事病假天数'] <= 15:
            return 80
        elif 15 < x['事病假天数'] and x['事病假天数'] <= 30:
            return 70
        elif 30 < x['事病假天数'] and x['事病假天数'] <= 45:
            return 60
        elif 45 < x['事病假天数'] and x['事病假天数'] <= 60:
            return 50
        elif 60 < x['事病假天数']:
            return 40

    #考勤得分统计
    df_kaoqin_now = df_kaoqin[df_kaoqin['gz_ym'].apply(lambda x: now_year in x)]
    df_kaoqin_now['事病假天数'] = df_kaoqin_now['leave_time_11'].astype(int) + df_kaoqin_now['leave_time_12'].astype(int)
    df_kaoqin_now_sum_month = df_kaoqin_now[['a0188', '事病假天数']].groupby(['a0188']).sum().reset_index()
    df_kaoqin_now_sum_month['出勤情况得分'] = df_kaoqin_now_sum_month.apply(cal_kaoqin_score, axis=1)
    df_kaoqin_now_sum_month['出勤情况得分'].fillna(100, inplace=True)

    df_result = pd.merge(df_result, df_kaoqin_now_sum_month[['a0188', '出勤情况得分']], on='a0188', how='left')

    #考核数据读取
    df_kaohe = pd.read_sql(session.query(A875).statement, session.bind)
    df_kaohe_now = df_kaohe[df_kaohe['gz_ym'] == now_year]
    df_kaohe_now = df_kaohe_now[df_kaohe_now['任职形式'] == '担任']

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

    df_kaohe_now['考核得分'] = df_kaohe_now.apply(cal_kaohe_score, axis=1)

    #龙虎榜数据读取
    df_longhu = pd.read_sql(session.query(Gxlygydjx).statement, session.bind)
    df_longhu_now = df_longhu[df_longhu['year'] == now_year]

    #读取员工序列表
    df_xulie = pd.read_excel('seqdata\员工序列表.xlsx', dtype=str)

    #龙虎榜序列重新计算
    df_longhu_now = pd.merge(df_longhu_now, df_xulie[['a0188', '二级序列']], on = 'a0188', how='left')

    df_longhu_now['二级序列'].fillna('未知分类', inplace=True)
    df_longhu_now['yjjxje'].fillna(0, inplace=True)
    df_longhu_now['yjjxje'] = df_longhu_now['yjjxje'].astype(float)
    df_longhu_now['rank'] = df_longhu_now.groupby('二级序列')['yjjxje'].rank(ascending=False)
    total_counts = df_longhu_now.groupby('二级序列')['a0188'].count()
    df_longhu_now['龙虎榜排名1'] = df_longhu_now.apply(lambda x: str(int(x['rank'])) + '/' + str(total_counts[x['二级序列']]), axis=1 )

    #计算龙虎榜得分
    def cal_longhu_score(x):
        a, b = x['龙虎榜排名1'].split('/')
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


    df_longhu_now['龙虎榜得分'] = df_longhu_now.apply(cal_longhu_score, axis=1)
    df_longhu_now = df_longhu_now[['a0188', '龙虎榜得分']].groupby('a0188').max()

    #得分数据合并

    df_result = pd.merge(df_result, df_kaohe_now[['a0188', '考核得分']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_longhu_now, on='a0188', how='left')
    df_result['当年工作业绩评价得分'] = 0.5 * df_result['考核得分'] + 0.5 * df_result['龙虎榜得分']

    df_result.fillna(0, inplace=True)



    return df_result







