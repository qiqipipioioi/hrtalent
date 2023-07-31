'''
计算荣誉表彰得分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time


def cal_honor_score(now_year):
    now_year = int(now_year)

    df_honor = pd.read_excel('seqdata\奖励子集_20230628140513.xlsx', dtype=str)

    #行内奖励
    df_honor_past_in = df_honor[df_honor['表彰奖励级别'] == '总行级']
    df_honor_past_in = df_honor_past_in[df_honor_past_in['表彰奖励年度'] != str(now_year)]


    def cal_in_honor_score(x, now_year):
        def year_map(y):
            if y == 0:
                return 1
            elif y == 1:
                return 0.8
            elif y == 2:
                return 0.6
            elif 3 <= y and y <= 5:
                return 0.4
            else:
                return 0.2

        def cum_years_map(y):
            if y < 5:
                return 1
            elif 5 <= y and y < 10:
                return 1.2
            elif 10 <= y:
                return 1.4

        cum_years = 0
        pair_list = []
        last_y = None
        last_pair = None
        for y in x:
            if y != last_y:
                if last_y:
                    pair_list.append(last_pair)
                    cum_years += 1
                last_pair = [y, 1]
                last_y = y
            else:
                last_pair[1] += 1
        pair_list.append(last_pair)
        cum_years += 1

        final_score = 0
        if pair_list != []:
            final_score = sum([min(p[1] * 50, 100) * year_map(now_year - int(p[0])) for p in pair_list]) / cum_years * cum_years_map(cum_years)

        return final_score


    #计算过往荣誉得分
    df_honor_past_in_group = df_honor_past_in[['员工号', '表彰奖励年度']].groupby(['员工号']).apply(lambda x: cal_in_honor_score(x['表彰奖励年度'].to_list(), now_year))
    df_honor_past_in_group.rename('过往行内表彰得分',inplace=True)

    #行外奖励
    df_honor_past_out = df_honor[df_honor['表彰奖励级别'] != '总行级']
    df_honor_past_out = df_honor_past_out[df_honor_past_out['表彰奖励级别'].notnull()]
    df_honor_past_out = df_honor_past_out[df_honor_past_out['表彰奖励年度'] != str(now_year)]

    #计算行外荣誉得分
    def cal_out_honor_score(x, now_year):
        def year_map(x):
            if x[0] == '国家级':
                if x[1] == 0:
                    return 1
                elif x[1] == 1:
                    return 0.9
                elif x[1] == 2:
                    return 0.8
                elif 3 <= x[1] and x[1] <= 5:
                    return 0.6
                else:
                    return 0.4
            elif x[0] in ['厅局级', '省部级']:
                if x[1] == 0:
                    return 1
                elif x[1] == 1:
                    return 0.8
                elif x[1] == 2:
                    return 0.6
                elif 3 <= x[1] and x[1] <= 5:
                    return 0.4
                else:
                    return 0.2
            elif x[0] == '地市级':
                if x[1] == 0:
                    return 1
                elif x[1] == 1:
                    return 0.7
                elif x[1] == 2:
                    return 0.5
                elif 3 <= x[1] and x[1] <= 5:
                    return 0.4
                else:
                    return 0.2
            elif x[0] == '县区级':
                if x[1] == 0:
                    return 1
                elif x[1] == 1:
                    return 0.6
                elif x[1] == 2:
                    return 0.4
                else:
                    return 0.2
            else:
                return 1

        def cum_years_guojia_map(y):
            if y <= 1:
                return 1
            elif y == 2:
                return 1.1
            elif 3 <= y and y<=4:
                return 1.2
            elif 5 <= y < 8:
                return 1.3
            elif 8 <= y and y < 10:
                return 1.4
            elif 10 <= y:
                return 1.5

        def cum_years_map(y):
            if y < 5:
                return 1
            elif 5 <= y and y < 10:
                return 1.2
            elif 10 <= y:
                return 1.4

        def base_map(y):
            if y == '国家级':
                return 100
            elif y in ['厅局级', '省部级']:
                return 75
            elif y == '地市级':
                return 50
            elif y == '县区级':
                return 25

        cum_years = 0
        cum_guojia_years = 0
        last_guojia_y = None
        pair_list = []
        last_y = None
        last_pair = None
        for p in x:
            if p[1] != last_y:
                if last_y:
                    pair_list.append(last_pair)
                    cum_years += 1
                last_pair = [[year_map([p[0], now_year - int(p[1])])], base_map(p[0])]
                last_y = p[1]
                if p[0] == '国家级':
                    cum_guojia_years += 1
                    last_guojia_y = p[1]

            else:
                last_pair[0].append(year_map([p[0], now_year - int(p[1])]))
                last_pair[1] += base_map(p[0])
                if p[0] == '国家级' and p[1] != last_guojia_y:
                    cum_guojia_years += 1
                    last_guojia_y = p[1]

        pair_list.append(last_pair)
        cum_years += 1 

        final_score = 0
        if pair_list != []:
            final_score = sum([max(p[0]) * min(p[1], 100) for p in pair_list]) / cum_years * max(cum_years_guojia_map(cum_guojia_years), cum_years_map(cum_years))

        return final_score


    df_honor_past_out_group = df_honor_past_out[['员工号', '表彰奖励级别', '表彰奖励年度']].groupby(['员工号']).apply(lambda x: cal_out_honor_score(x[['表彰奖励级别', '表彰奖励年度']].values.tolist(), now_year))
    df_honor_past_out_group.rename('过往行外表彰得分',inplace=True)


    #当年内部奖励得分
    df_honor_now_in = df_honor[df_honor['表彰奖励级别'] == '总行级']
    df_honor_now_in = df_honor_now_in[df_honor_now_in['表彰奖励年度'] == str(now_year)]


    def cal_now_in_honor_score(x):
        return min(100, 50 * len(x))


    df_honor_now_in_group = df_honor_now_in[['员工号', '表彰奖励年度']].groupby(['员工号']).apply(lambda x: cal_now_in_honor_score(x['表彰奖励年度'].to_list()))
    df_honor_now_in_group.rename('当年行内表彰得分',inplace=True)


    #当年行外奖励
    df_honor_now_out = df_honor[df_honor['表彰奖励级别'] != '总行级']
    df_honor_now_out = df_honor_now_out[df_honor_now_out['表彰奖励级别'].notnull()]
    df_honor_now_out = df_honor_now_out[df_honor_now_out['表彰奖励年度'] == str(now_year)]


    def cal_now_out_honor_score(x):
        score = 0
        for y in x:
            if y == '国家级':
                score += 100
            elif y in ['厅局级', '省部级']:
                score += 75
            elif y == '地市级':
                score += 50
            elif y == '县区级':
                score += 25
        return min(100, score)


    df_honor_now_out_group = df_honor_now_out[['员工号', '表彰奖励级别']].groupby(['员工号']).apply(lambda x: cal_now_out_honor_score(x['表彰奖励级别'].to_list()))
    df_honor_now_out_group.rename('当年行外表彰得分',inplace=True)


    #员工统计
    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '入行时间', '任现岗位时间','行员等级']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]


    df_result = pd.merge(df_base[['员工号']], df_honor_past_in_group, on='员工号', how='left')
    df_result = pd.merge(df_result, df_honor_past_out_group, on='员工号', how='left')
    df_result = pd.merge(df_result, df_honor_now_in_group, on='员工号', how='left')
    df_result = pd.merge(df_result, df_honor_now_out_group, on='员工号', how='left')
    df_result.fillna(0, inplace=True)
    df_result['在行累积工作荣誉得分'] = df_result['过往行内表彰得分'] * 0.5 + df_result['过往行内表彰得分'] * 0.5
    df_result['当年工作荣誉得分'] = df_result['当年行内表彰得分'] * 0.5 + df_result['当年行内表彰得分'] * 0.5


    return df_result






