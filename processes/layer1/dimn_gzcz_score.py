'''
工作成长得分
'''

#!/usr/bin/env python
# coding: utf-8

import pandas as pd

def cal_gzcz_score(now_year, df_base, df_kaohe, df_longhu, df_xulie):

    now_year = int(now_year)

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


    #年度考核
    df_kaohe['a8759'] = df_kaohe['a8759'].astype(int)
    df_kaohe = df_kaohe[df_kaohe['khqk'].notnull()]
    df_kaohe['年度考核得分'] = df_kaohe.apply(cal_kaohe_score, axis=1)
    df_kaohe_past = df_kaohe[df_kaohe['a8759'].apply(lambda x:x>=now_year - 5 and x<=now_year-1)]
    df_kaohe_past.drop('a8759',axis=1,inplace=True)
    df_kaohe_past = df_kaohe_past.groupby(['a0188']).mean()
    df_kaohe_past.rename(columns={'年度考核得分':'考核评分成长'},inplace=True)

    #过往绩效
    def cal_longhu_score(x):
        a, b = x['龙虎榜排名'].split('/')
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


    def cal_longhu_5year_score(x):
        score = 0
        if x['year'].min() <= now_year - 5:
            score = x['龙虎榜得分'].mean()
        else:
            score = 0
        return score

    def cal_longhu_3year_score(x):
        score = 0
        if x['year'].min() <= now_year - 3:
            score = x['龙虎榜得分'].mean()
        else:
            score = 0
        return score


    df_longhu['year'] = df_longhu['year'].astype(int)
    df_longhu= pd.merge(df_longhu, df_xulie[['a0188', 'lvl2_professional_sequence']], on = 'a0188', how='left')
    df_longhu['lvl2_professional_sequence'].fillna('未知分类', inplace=True)
    df_longhu['yjjxje'].fillna(0, inplace=True)
    df_longhu['yjjxje'] = df_longhu['yjjxje'].astype(float)
    df_longhu['rank'] = df_longhu.groupby(['year','lvl2_professional_sequence'])['yjjxje'].rank(ascending=False)
    total_counts = df_longhu.groupby(['year', 'lvl2_professional_sequence'])['a0188'].count()
    df_longhu['龙虎榜排名'] = df_longhu.apply(lambda x: str(int(x['rank'])) + '/' + str(total_counts[x['year'], x['lvl2_professional_sequence']]), axis=1 )


    df_longhu['龙虎榜得分'] = df_longhu.apply(cal_longhu_score, axis=1)
    df_longhu_past = df_longhu[df_longhu['year'].apply(lambda x: x >= now_year - 5 and x <= now_year - 1)]
    df_longhu_past.drop('year', axis=1, inplace=True)
    df_longhu_past = df_longhu_past.groupby(['a0188']).mean()
    df_longhu_past.rename(columns={'龙虎榜得分': '龙虎榜成长'}, inplace=True)

    df_result = pd.merge(df_base[['a0188']],df_kaohe_past[['考核评分成长']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_longhu_past[['龙虎榜成长']], on='a0188', how='left')

    df_result['base_jxcz_score'] = 0.5 * df_result['考核评分成长'] + 0.5 * df_result['龙虎榜成长']
    df_result = df_result[['a0188', 'base_jxcz_score']]

    return df_result





