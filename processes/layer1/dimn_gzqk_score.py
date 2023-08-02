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


def calculate_working_status_score(now_year):
    #计算工作状态得分

    #读取KOL数据    
    kol_names = os.listdir('seqdata/KOL')
    df_kol_list = []
    for kol_name in kol_names:
        kol_file = 'seqdata/KOL/' + kol_name
        df_temp = pd.read_csv(kol_file, dtype=str)
        df_temp['统计年份'] = kol_name.replace('.csv', '')
        df_kol_list.append(df_temp)
    df_kol = pd.concat(df_kol_list, axis=0)
    df_kol.rename(columns = {'USERID': '员工号', 'USERNAME': '姓名', '(EXPR)': 'KOL积分'}, inplace=True)

    #KOL得分统计
    df_kol_now = df_kol[df_kol['统计年份'] == now_year]
    kol_now_max_score = df_kol_now['KOL积分'].astype(int).max()

    df_kol_now['KOL得分'] = df_kol_now['KOL积分'].astype(int) / kol_now_max_score * 100

    #日志数据读取
    journal_names = os.listdir('seqdata/日志')
    df_journal_list = []
    for journal_name in journal_names:
        journal_file = 'seqdata/日志/' + journal_name
        df_temp = pd.read_excel(journal_file, dtype=str)
        df_temp['统计年月'] = journal_name.replace('.xls', '')
        df_journal_list.append(df_temp)
    df_journal = pd.concat(df_journal_list, axis=0)
    df_journal.rename(columns={'用户CODE': '员工号'}, inplace=True)
    df_journal_now = df_journal[df_journal['统计年月'].apply(lambda x: now_year in x)]

    #日志得分统计
    df_journal_now['发布量'] = df_journal_now['发布量'].astype(float)
    df_journal_now['点赞量'] = df_journal_now['点赞量'].astype(float)
    df_journal_now['浏览量'] = df_journal_now['浏览量'].astype(float)
    df_journal_now['回复量'] = df_journal_now['回复量'].astype(float)
    df_journal_now['转发量'] = df_journal_now['转发量'].astype(float)
    df_journal_now['互动总量'] = df_journal_now['互动总量'].astype(float)
    df_journal_now['总字数'] = df_journal_now['总字数'].astype(float)
    df_journal_now['上榜次数'] = df_journal_now['上榜次数'].astype(float)
    df_journal_now_by_month = df_journal_now.groupby('员工号').mean().reset_index()

    df_journal_now_by_month['发布数量得分'] = df_journal_now_by_month['发布量'] / df_journal_now_by_month['发布量'].max() * 20
    df_journal_now_by_month['发布字数得分'] = df_journal_now_by_month['总字数'] / df_journal_now_by_month['总字数'].max() * 20
    df_journal_now_by_month['上榜次数得分'] = df_journal_now_by_month['上榜次数'] / df_journal_now_by_month['上榜次数'].max() * 20
    df_journal_now_by_month['互动总量得分'] = df_journal_now_by_month['互动总量'] / df_journal_now_by_month['互动总量'].max() * 20
    df_journal_now_by_month['日志得分'] = df_journal_now_by_month['发布数量得分'] + df_journal_now_by_month['发布字数得分'] + df_journal_now_by_month['上榜次数得分'] + df_journal_now_by_month['互动总量得分']


    #员工统计
    # 部门表：b01，'一级机构', '二级机构', '中心'
    # e01，岗位
    # bm_zwtx，职务
    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base = df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '入行时间', '任现岗位时间','行员等级']]
    
    
    #筛选出非高管和首席的员工
    # status，任职形式
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]


    #工具使用情况得分
    df_result = pd.merge(df_base[['员工号']], df_kol_now[['员工号', 'KOL得分']], on='员工号', how='left')
    df_result = pd.merge(df_result, df_journal_now_by_month[['员工号', '日志得分']], on='员工号', how='left')
    df_result.fillna(0, inplace=True)
    df_result['工具使用情况得分'] = df_result['KOL得分'] * 0.5 + df_result['日志得分'] * 0.5

    #考勤数据
    df_kaoqin = pd.read_excel('seqdata\月结果_20230627160707.xlsx', dtype=str)
    
    # k_month
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
    df_kaoqin_now = df_kaoqin[df_kaoqin['年月'].apply(lambda x: now_year in x)]
    df_kaoqin_now['出勤情况得分'] = df_kaoqin_now['事假天数'].astype(int) + df_kaoqin_now['病假天数'].astype(int)
    df_kaoqin_now_sum_month = df_kaoqin_now[['员工号', '事病假天数']].groupby(['员工号']).sum().reset_index()
    df_kaoqin_now_sum_month['出勤情况得分'] = df_kaoqin_now_sum_month.apply(cal_kaoqin_score, axis=1)
    df_kaoqin_now_sum_month['出勤情况得分'].fillna(100, inplace=True)

    df_result = pd.merge(df_result, df_kaoqin_now_sum_month[['员工号', '出勤情况得分']], on='员工号', how='left')

    #考核数据读取
    df_kaohe = pd.read_excel('seqdata\年度考核子集_20230504141856.xlsx', dtype=str)
    df_kaohe_now = df_kaohe[df_kaohe['年度'] == now_year]
    df_kaohe_now = df_kaohe_now[df_kaohe_now['任职形式'] == '担任']

    #考核得分计算
    # 
    def cal_kaohe_score(x):
        if x['考核情况'] == '优秀':
            return 100
        elif x['考核情况'] == '称职':
            return 80
        elif x['考核情况'] == '基本称职':
            return 60
        elif x['考核情况'] == '不称职':
            return 40

    df_kaohe_now['考核得分'] = df_kaohe_now.apply(cal_kaohe_score, axis=1)

    #龙虎榜数据读取
    df_longhu = pd.read_excel('seqdata\龙虎榜排名_20230509153725.xlsx', dtype=str)
    df_longhu_now = df_longhu[df_longhu['年度'] == now_year]

    #读取员工序列表
    df_xulie = pd.read_excel('seqdata\员工序列表.xlsx', dtype=str)

    #龙虎榜序列重新计算
    df_longhu_now = pd.merge(df_longhu_now, df_xulie[['员工号', '二级序列']], on = '员工号', how='left')

    df_longhu_now['二级序列'].fillna('未知分类', inplace=True)
    df_longhu_now['月均绩效金额'].fillna(0, inplace=True)
    df_longhu_now['月均绩效金额'] = df_longhu_now['月均绩效金额'].astype(float)
    df_longhu_now['rank'] = df_longhu_now.groupby('二级序列')['月均绩效金额'].rank(ascending=False)
    total_counts = df_longhu_now.groupby('二级序列')['员工号'].count()
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
    df_longhu_now = df_longhu_now[['员工号', '龙虎榜得分']].groupby('员工号').max()

    #得分数据合并

    df_result = pd.merge(df_result, df_kaohe_now[['员工号', '考核得分']], on='员工号', how='left')
    df_result = pd.merge(df_result, df_longhu_now, on='员工号', how='left')
    df_result['当年工作业绩评价得分'] = 0.5 * df_result['考核得分'] + 0.5 * df_result['龙虎榜得分']

    df_result.fillna(0, inplace=True)



    return df_result







