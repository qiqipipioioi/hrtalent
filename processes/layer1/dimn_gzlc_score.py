'''
在行工作经历得分计算
'''
#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np
import datetime
import time
from models.layer1_model import A01,A866,Bm_jp_a01,E01



def calculate_in_bank_working_experience_score(session):

    # 行员等级编码
    hydj_code = pd.read_sql(session.query(Bm_jp_a01).statement,session.bind)

    # 岗位编码
    position_code = pd.read_sql(session.query(E01).statement,session.bind)

    #读取员工基本信息
    df_base = pd.read_sql(session.query(A01).statement, session.bind)

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任'] # TODO 没有任职形式字段
    df_base = df_base[df_base['dept_code'] != position_code.loc[position_code['mc0000']=='高管','dept_code']]
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)] # code error
    df_base = df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a0141', 'a01145','a01686']]

    #计算入行年限得分
    def cal_inworking_score(x):
        if x < 1:
            return 5
        elif 1 <= x and x < 5:
            return 15
        elif 5<= x and x < 10:
            return 25
        elif 10 <= x and x < 15:
            return 45
        elif 15 <= x and x <= 25:
            return 70
        elif 20 <= x:
            return 100

    # df_base['入行年限'] = df_base['a0141'].apply(lambda x: (datetime.datetime.now() - datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')).days / 365)
    df_base['入行年限'] = df_base['a0141'].apply(lambda x: (datetime.datetime.now() - x).days / 365)
    # df_base['当期岗位工作年限'] = df_base['a01145'].apply(lambda x: (datetime.datetime.now() - datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')).days / 365)
    df_base['当期岗位工作年限'] = df_base['a01145'].apply(lambda x: (datetime.datetime.now() - x).days / 365)
    #计算入行年限得分
    df_base['在行持续服务年限得分'] = df_base['入行年限'].apply(cal_inworking_score)

    #计算当前岗位序列得分
    def cal_now_position_seq_score(x):
        #计算当前岗位序列得分

        #计算基础分
        base_score = 0
        if x['二级序列'] in ['工勤', '柜员']:
            base_score = 40
        else:
            base_score = 50

        #计算行员等级系数
        emp_lv_factor = 1
        if x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='十二级','bm0000']]:
            emp_lv_factor = 1.1
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='十一级','bm0000']]:
            emp_lv_factor = 1.15
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='十级','bm0000']]:
            emp_lv_factor = 1.2
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='九级','bm0000']]:
            emp_lv_factor = 1.3
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='八级','bm0000']]:
            emp_lv_factor = 1.4
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='七级','bm0000']]:
            emp_lv_factor = 1.5
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='六级','bm0000']]:
            emp_lv_factor = 1.6
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='五级','bm0000']]:
            emp_lv_factor = 1.7
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='四级','bm0000']]:
            emp_lv_factor = 1.8
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='三级','bm0000']]:
            emp_lv_factor = 1.9
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='二级','bm0000']]:
            emp_lv_factor = 2.0
        elif x['a01686'] in [hydj_code.loc[hydj_code['mc0000']=='一级','bm0000']]:
            emp_lv_factor = 2.0
        else:
            emp_lv_factor = 1.0

        #职业序列等级系数
        seq_lv_factor = 1
    #     if x['职业序列等级'] == '初级':
    #         seq_lv_factor = 1
    #     elif x['职业序列等级'] == '中级':
    #         seq_lv_factor = 1.05
    #     elif x['职业序列等级'] == '高级':
    #         seq_lv_factor = 1.1
    #     elif x['职业序列等级'] == '资深':
    #         seq_lv_factor = 1.2
    #     elif x['职业序列等级'] == '高级资深':
    #         seq_lv_factor = 1.25
    #     elif x['职业序列等级'] == '专家':
    #         seq_lv_factor = 1.3
    #     elif x['职业序列等级'] == '高级专家':
    #         seq_lv_factor = 1.4
    #     elif x['职业序列等级'] == '高级资深专家':
    #         seq_lv_factor = 1.5

        #当前岗位工作年限系数
        now_position_factor = np.log10(x['当期岗位工作年限'] * 10 + 1)

        #计算现任岗位得分
        now_position_score = base_score * max([emp_lv_factor, seq_lv_factor]) * now_position_factor

        return now_position_score



    # 读取员工序列表
    df_seq = pd.read_excel('seqdata\员工序列表.xlsx', dtype=str) # TODO 没有员工序列表

    # 将员工序列表与基础信息表合并
    df_base_merge_seq = pd.merge(df_base, df_seq[['a0188', '一级序列', '二级序列']], on='a0188', how='left')

    # 计算当前岗位序列得分
    df_base_merge_seq['当前岗位序列得分'] = df_base_merge_seq.apply(cal_now_position_seq_score, axis=1)

    # 读取工作经历子集
    df_working = pd.read_sql(session.query(A866).statement, session.bind)

    # 将工作经历子集与基础信息表合并
    df_working_merge_base = pd.merge(df_working, df_base[['a0188', 'a0141', 'a01145']], on='a0188', how='left')

    # 筛选出起始时间晚于入行时间，终止时间早于任现岗位时间的工作经历
    df_working_merge_base = df_working_merge_base[df_working_merge_base['a8661'] >= df_working_merge_base['a0141']]
    df_working_merge_base = df_working_merge_base[df_working_merge_base['a8662'] <= df_working_merge_base['a01145']]

    # 将“职务/岗位”列重命名为“岗位”
    df_working_merge_base.rename(columns={'职务/岗位': '岗位'}, inplace=True)

    # 从员工序列表中提取岗位和二级序列信息
    df_seq_simple = df_seq[['e0101', '二级序列']].drop_duplicates()

    # 将工作经历子集与岗位和二级序列信息合并
    df_working_merge_base_seq = pd.merge(df_working_merge_base, df_seq_simple, on='岗位', how='left')

    # 计算每个员工在每个二级序列下的工作年限
    df_working_merge_base_seq['岗位工作时间'] = df_working_merge_base_seq.apply(lambda x: (x['a8662'] - x['a8661']).days / 365, axis=1)
    df_working_merge_base_seq_group = df_working_merge_base_seq[['a0188', '岗位工作时间', '二级序列']].groupby(['a0188', '二级序列']).sum().reset_index()

    # 计算单一序列得分
    def cal_single_past_seq_score(x):
        #计算基础分
        base_score = 0
        if x['二级序列'] in ['工勤', '柜员']:
            base_score = 40
        else:
            base_score = 50

        #当前岗位工作年限系数
        now_position_factor = np.log10(x['岗位工作时间'] * 10 + 1)
        #计算现任岗位得分
        single_position_score = base_score * now_position_factor
        return single_position_score


    df_working_merge_base_seq_group['单一序列年限'] = df_working_merge_base_seq_group['岗位工作时间']
    # df_working_merge_base_seq_group['单一序列得分'] = df_working_merge_base_seq_group.apply(cal_single_past_seq_score, axis=1)
    df_base_merge_seq_hist = pd.merge(df_working_merge_base_seq_group, df_base_merge_seq[['a0188', '二级序列','当前岗位序列得分']], on='a0188', how='left')

    # #计算当前序列得分
    # def cal_now_seq_score(x):
    #     if x['二级序列_x'] == x['二级序列_y']:
    #         return x['单一序列得分'] + x['当前岗位序列得分']
    #     else:
    #         return x['当前岗位序列得分']

    # df_base_merge_seq_hist['当前序列得分'] = df_base_merge_seq_hist.apply(cal_now_seq_score, axis=1)

    df_base_merge_seq_now = df_base_merge_seq_hist[df_base_merge_seq_hist['二级序列_x'] == df_base_merge_seq_hist['二级序列_y']]
    df_base_merge_seq_now.rename(columns={'二级序列_y':'二级序列'},inplace=True)
    df_base_merge_seq_now = df_base_merge_seq_now[['a0188', '二级序列', '单一序列年限']].drop_duplicates()

    # 合并当期序列得分
    df_base_merge_seq_now.rename(columns={'单一序列年限':'当前序列年限'},inplace=True)
    df_base_merge_seq.rename(columns={'当前岗位序列年限':'当前序列年限'},inplace=True)
    df_base_merge_seq_now = pd.concat([df_base_merge_seq[['a0188','二级序列','单一序列年限']],df_base_merge_seq_now[['a0188','二级序列','单一序列年限']]],axis=0)
    df_base_merge_seq_now_g = df_base_merge_seq_now.groupby(['a0188','二级序列']).sum()
    df_base_merge_seq_now_g.reset_index(inplace=True)

    def cal_now_seq_score(x):
        # 计算基础分
        base_score=0
        if x['二级序列'] in ['工勤','柜员','村镇银行']:
            base_score = 40
        elif x['二级序列'] in ['不适用']:
            base_score=20
        else:
            base_score=60

        #当前岗位工作年限系数
        now_position_factor = np.log10(x['当前序列年限']*10+1)

        # 计算现任岗位得分
        single_position_score = base_score * now_position_factor

        return single_position_score

    def cal_past_seq_score(x):
        # 计算基础分
        base_score = 40
        # 当前岗位工作年限系数
        now_position_factor = np.log10(x['过去序列年限']*10+1)
        # 计算现任岗位得分
        single_position_score = base_score * now_position_factor
        return single_position_score

    #计算其他序列得分
    df_base_merge_seq_other = df_base_merge_seq_hist[df_base_merge_seq_hist['二级序列_x'] != df_base_merge_seq_hist['二级序列_y']][['a0188', '单一序列得分']].groupby(['a0188']).sum().reset_index()

    df_base_merge_seq_other.rename(columns={'单一序列得分': '过去序列得分'}, inplace=True)

    df_base_merge_seq_now_g['当前序列得分'] = df_base_merge_seq_now_g.apply(cal_now_seq_score,axis=1)
    df_base_merge_seq_other['过去序列得分'] = df_base_merge_seq_other.apply(cal_past_seq_score,axis=1)
    #对所有得分进行汇总
    df_result = df_base[['a0188', '在行持续服务年限得分']]
    df_result = pd.merge(df_result, df_base_merge_seq_now, on='a0188', how='left')
    df_result = pd.merge(df_result, df_base_merge_seq_other, on='a0188', how='left')
    df_result.fillna(0, inplace=True)

    return df_result



