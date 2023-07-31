'''
计算员工积分和专业序列分
'''
#coding=utf-8

import pandas as pd
import numpy as np
import json
import hashlib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from processes.layer1.ability_evaluation import cal_ability_evaluation_score
from processes.layer1.honor import cal_honor_score
from processes.layer1.in_bank_working_experience import calculate_in_bank_working_experience_score
from processes.layer1.learning_growing_up import cal_learning_growing_up_score
from processes.layer1.out_bank_working_experience import calculate_in_bank_working_experience_score
from processes.layer1.professional_ability import cal_professional_ability_score
from processes.layer1.punish import cal_punish_score
from processes.layer1.relation_score import cal_relation_score
from processes.layer1.working_growing_up import cal_working_growing_up_score
from processes.layer1.working_status import calculate_working_status_score
from utils.read_configs import read_relations, read_ranges
from models.layer1_model import ProfessionalSequenceLabelWeightsModel, EmployeeProfessionalSequenceModel
from models.layer2_model import EmployeeBaseScoreModel

#建立mysql链接
engine = create_engine('', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#读取配置参数
LANG_BASE_DICT, DIMN_LANG_DICT, BASE_DICT, LANG_DICT, DIMN_DICT, SEQC_DICT, BASE_WITH_SEC_LABEL_DICT = read_relations()
COMMON_LEVEL_RANGE, SEQC1_LEVEL_RANGE, SEQC2_LEVEL_RANGE = read_ranges()



def get_common_score():
    #计算宽表
    #计算各个指标得分
    df_ability_evaluation_score = cal_ability_evaluation_score()
    df_honor_score = cal_honor_score()
    df_in_bank_working_experience_score = calculate_in_bank_working_experience_score()
    df_learning_growing_up_score = cal_learning_growing_up_score()
    df_out_bank_working_experience_score = calculate_in_bank_working_experience_score()
    df_professional_ability_score = cal_professional_ability_score()
    df_punish_score = cal_punish_score()
    df_relation_score = cal_relation_score()
    df_working_growing_up_score = cal_working_growing_up_score()
    df_working_status_score = calculate_working_status_score()


    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '聘任职业技术等级']], df_ability_evaluation_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_honor_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_in_bank_working_experience_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_learning_growing_up_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_out_bank_working_experience_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_professional_ability_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_punish_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_relation_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_working_growing_up_score, on='员工号', how='left')
    df_result = pd.merge(df_result, df_working_status_score, on='员工号', how='left')


def cal_score(df_base_score, df_weights):
    #计算员工积分
    df_seqc_score = df_base_score[['user_id', 'lvl1_org', 'lvl2_org', 'center', 'position']]
    #基础标签最大值
    df_max_val = df_weights.iloc[0,:]
    #计算序列分
    for _, row in df_weights.iloc[1:, :].iterrows():
        seqc_name = SEQC_DICT[row.values[1]] + '_score'
        if row.values[1] == '综合评分':
            #带绩效的综合评分
            df_seqc_score[seqc_name] = 0
            #不带绩效的综合评分
            zhpf_nojx_name = SEQC_DICT[row.values[1]] + '_nojx_score'
            df_seqc_score[zhpf_nojx_name] = 0
            for col in BASE_DICT:
                col_name = BASE_DICT[col]
                label_max_val = df_max_val[col_name+'_weight']
                df_seqc_score[seqc_name] += df_base_score[col_name+'_score'].apply(lambda x: label_max_val if x > label_max_val else x) * row[col_name+'_weight']
                if col_name not in ['base_dqxl', '']
            
    return df_seqc_score


def cal_rank(df_seqc_score, df_employee_seqc):
    #合并序列数据
    df_seqc_score_all = pd.merge(df_seqc_score, df_employee_seqc[['user_id', 'lvl2_professional_sequence']], on = 'user_id', how='left')
    #计算每个No.在他所在二级序列的排名
    #取二级序列的值，然后找到对应的列

    for seqc in SEQC_DICT.values():
        if seqc != 'seqc_zhpf':
            seqc_total_name = seqc + '_total_score'
            df_seqc_score_all[seqc_total_name] = df_seqc_score_all.apply(lambda x: x[seqc + '_score'] + x['seqc_zhpf_score'], axis=1)
    
    def self_seqc_score(x):
        if x['lvl2_professional_sequence'] in SEQC_DICT:
            return x[SEQC_DICT[x['lvl2_professional_sequence']] + '_score'] + x['seqc_zhpf_score']
        else:
            return x['seqc_zhpf_score']
    #计算本序列得分
    df_seqc_score_all['self_seqc_total_score'] = df_seqc_score_all.apply(self_seqc_score, axis=1)
    #计算每个No.在他所在二级序列的所在序列得分的排名,并且处以所在序列总人数，得到排名的百分比
    
    def cal_zhpf_lvl(score):
        #根据COMMON_LEVEL_RANGE计算综合评分等级
        for rating, range in COMMON_LEVEL_RANGE.items():
            if range[0] <= score < range[1]:
                return rating
        return None 

        
    def cal_seqc_lvl(score, seqc):
        #根据SEQC_LEVEL_RANGE计算序列评分等级
        if seqc in ['柜员', '工勤']:
            for rating, range in SEQC2_LEVEL_RANGE.items():
                if range[0] <= score < range[1]:
                    return rating
        else:
            for rating, range in SEQC1_LEVEL_RANGE.items():
                if range[0] <= score < range[1]:
                    return rating
        return None

    df_seqc_score_all['self_seqc_rank'] = df_seqc_score_all.groupby('lvl2_professional_sequence')['self_seqc_total_score'].rank(ascending=False)
    df_seqc_score_all['self_seqc_rank_pct'] = df_seqc_score_all.groupby('lvl2_professional_sequence')['self_seqc_total_score'].rank(ascending=False, pct=True)
    df_seqc_score_all['zhpf_rank'] = df_seqc_score_all['seqc_zhpf_score'].rank(ascending=False)
    df_seqc_score_all['zhpf_rank_pct'] = df_seqc_score_all['seqc_zhpf_score'].rank(ascending=False, pct=True)
    df_seqc_score_all['zhpf_level'] = df_seqc_score_all['zhpf_rank_pct'].apply(lambda x: cal_zhpf_lvl(x))
    df_seqc_score_all['self_seqc_level'] = df_seqc_score_all[['self_seqc_rank_pct', 'lvl2_professional_sequence']].apply(lambda x: cal_seqc_lvl(x['self_seqc_rank_pct'], x['lvl2_professional_sequence']), axis=1)
    print(df_seqc_score_all.columns)
    df_seqc_score_all.to_excel('data/员工序列评价得分_排名1.xlsx')
    return df_seqc_score_all

def cal_score_main():
    #读取权重，基础得分，员工序列表，并且合并序列到基础得分表
    df_weights = pd.read_sql(session.query(ProfessionalSequenceLabelWeightsModel).statement, session.bind)
    df_base_score = pd.read_sql(session.query(EmployeeBaseScoreModel).statement, session.bind)
    df_employee_seqc = pd.read_sql(session.query(EmployeeProfessionalSequenceModel).statement, session.bind)
    df_base_score = pd.merge(df_base_score, df_employee_seqc[['user_id', 'lvl2_professional_sequence']], on = 'user_id', how='left')
    #计算员工序列得分
    df_seqc_score = cal_score(df_base_score, df_weights)
    print(df_seqc_score.columns)
    cal_rank(df_seqc_score, df_employee_seqc)
    # print(df_score)


if __name__ == '__main__':
    cal_score_main()











