'''
在行工作经历得分计算
'''
#!/usr/bin/env python
# coding: utf-8



import pandas as pd
import numpy as np
import datetime
import time



def calculate_in_bank_working_experience_score():
    #读取员工基本信息
    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]
    df_base = df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '入行时间', '任现岗位时间','行员等级']]

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

    df_base['入行年限'] = df_base['入行时间'].apply(lambda x: (datetime.datetime.now() - datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')).days / 365)
    df_base['当期岗位工作年限'] = df_base['任现岗位时间'].apply(lambda x: (datetime.datetime.now() - datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')).days / 365)
    #计算入行年限得分
    df_base['在行持续服务年限得分'] = df_base['入行年限'].apply(cal_inworking_score)

    #计算当前岗位序列得分
    def cal_now_position_seq_score(x):
        #计算当前岗位序列得分

        #计算基础分
        # 序列：bm_gwseq
        base_score = 0
        if x['二级序列'] in ['工勤', '柜员']:
            base_score = 40
        else:
            base_score = 50

        #计算行员等级系数
        # 行员等级：bm_jp_a01
        emp_lv_factor = 1
        if x['行员等级'] in ['十二级', '十一级']:
            emp_lv_factor = 1
        elif x['行员等级'] in ['十级', '九级', '八级']:
            emp_lv_factor = 1.1
        elif x['行员等级'] in ['七级', '六级', '五级']:
            emp_lv_factor = 1.2
        elif x['行员等级'] in ['四级', '三级', '二级']:
            emp_lv_factor = 1.3
        elif x['行员等级'] in ['一级']:
            emp_lv_factor = 1.5

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
    df_seq = pd.read_excel('seqdata\员工序列表.xlsx', dtype=str)

    # 将员工序列表与基础信息表合并
    df_base_merge_seq = pd.merge(df_base, df_seq[['员工号', '一级序列', '二级序列']], on='员工号', how='left')

    # 计算当前岗位序列得分
    df_base_merge_seq['当前岗位序列得分'] = df_base_merge_seq.apply(cal_now_position_seq_score, axis=1)

    # 读取工作经历子集
    df_working = pd.read_excel('seqdata\工作经历子集_20230504133753.xlsx', dtype=str)

    # 将工作经历子集与基础信息表合并
    df_working_merge_base = pd.merge(df_working, df_base[['员工号', '入行时间', '任现岗位时间']], on='员工号', how='left')

    # 筛选出起始时间晚于入行时间，终止时间早于任现岗位时间的工作经历
    df_working_merge_base = df_working_merge_base[df_working_merge_base['起始时间'] >= df_working_merge_base['入行时间']]
    df_working_merge_base = df_working_merge_base[df_working_merge_base['终止时间'] <= df_working_merge_base['任现岗位时间']]

    # 将“职务/岗位”列重命名为“岗位”
    df_working_merge_base.rename(columns={'职务/岗位': '岗位'}, inplace=True)

    # 从员工序列表中提取岗位和二级序列信息
    df_seq_simple = df_seq[['岗位', '二级序列']].drop_duplicates()

    # 将工作经历子集与岗位和二级序列信息合并
    df_working_merge_base_seq = pd.merge(df_working_merge_base, df_seq_simple, on='岗位', how='left')

    # 计算每个员工在每个二级序列下的工作年限
    df_working_merge_base_seq['岗位工作时间'] = df_working_merge_base_seq.apply(lambda x: (datetime.datetime.strptime(x['终止时间'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(x['起始时间'], '%Y-%m-%d %H:%M:%S')).days / 365, axis=1)
    df_working_merge_base_seq_group = df_working_merge_base_seq[['员工号', '岗位工作时间', '二级序列']].groupby(['员工号', '二级序列']).sum().reset_index()

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


    df_working_merge_base_seq_group['单一序列得分'] = df_working_merge_base_seq_group.apply(cal_single_past_seq_score, axis=1)

    df_base_merge_seq_hist = pd.merge(df_working_merge_base_seq_group, df_base_merge_seq[['员工号', '二级序列','当前岗位序列得分']], on='员工号', how='left')

    #计算当前序列得分
    def cal_now_seq_score(x):
        if x['二级序列_x'] == x['二级序列_y']:
            return x['单一序列得分'] + x['当前岗位序列得分']
        else:
            return x['当前岗位序列得分']

    df_base_merge_seq_hist['当前序列得分'] = df_base_merge_seq_hist.apply(cal_now_seq_score, axis=1)

    df_base_merge_seq_now = df_base_merge_seq_hist[df_base_merge_seq_hist['二级序列_x'] == df_base_merge_seq_hist['二级序列_y']]
    df_base_merge_seq_now = df_base_merge_seq_now[['员工号', '当前序列得分']].drop_duplicates()

    #计算其他序列得分
    df_base_merge_seq_other = df_base_merge_seq_hist[df_base_merge_seq_hist['二级序列_x'] != df_base_merge_seq_hist['二级序列_y']][['员工号', '单一序列得分']].groupby(['员工号']).sum().reset_index()

    df_base_merge_seq_other.rename(columns={'单一序列得分': '过去序列得分'}, inplace=True)

    #对所有得分进行汇总
    df_result = df_base[['员工号', '在行持续服务年限得分']]
    df_result = pd.merge(df_result, df_base_merge_seq_now, on='员工号', how='left')
    df_result = pd.merge(df_result, df_base_merge_seq_other, on='员工号', how='left')
    df_result.fillna(0, inplace=True)

    return df_result



