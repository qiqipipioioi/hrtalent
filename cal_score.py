'''
计算员工积分和专业序列分
'''
#coding=utf-8

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from processes.layer1.dimn_gxtp_score import cal_gxtp_score
from processes.layer1.dimn_gzcz_score import cal_gzcz_score
from processes.layer1.dimn_gzlc_score import cal_gzlc_score
from processes.layer1.dimn_gzqk_score import cal_gzqk_score
from processes.layer1.dimn_hwjl_score import cal_hwjl_score
from processes.layer1.dimn_rybz_score import cal_rybz_score
from processes.layer1.dimn_wgcc_score import cal_wgcc_score
from processes.layer1.dimn_xxts_score import cal_xxts_score
from processes.layer1.dimn_zhpc_score import cal_zhpc_score
from processes.layer1.dimn_zynl_score import cal_zynl_score
from utils.read_configs import read_relations, read_ranges, read_mysql_configs, init_log
from models.layer1_model import *
from models.layer2_model import EmployeeBaseScoreModel

#建立mysql链接
mysql_info = read_mysql_configs()
engine = create_engine(mysql_info, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

#读取配置参数
LANG_BASE_DICT, DIMN_LANG_DICT, BASE_DICT, LANG_DICT, DIMN_DICT, SEQC_DICT, BASE_WITH_SEC_LABEL_DICT = read_relations()
COMMON_LEVEL_RANGE, SEQC1_LEVEL_RANGE, SEQC2_LEVEL_RANGE = read_ranges()

hrlog = init_log()

class EmployeeScoreModel(object):
    def __init__(self, now_year):
        self.now_year = now_year

    def get_source_data(self):
        hrlog.info("1.1 开始读取数据")
        now_year = '2022'
        #0.员工基本信息数据
        df_base = pd.read_sql(session.query(A01).statement, session.bind)
        df_dept = pd.read_sql(session.query(B01).statement, session.bind)
        df_base = df_base[df_base['dept_code'] != df_dept.loc[df_dept['content']=='高管','dept_code'].values[0]]
        self.df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x if x else True)]
        hrlog.info("1.1 数据读取: 员工基本信息读取完成")
        #1.读取关系拓扑数据
        #家庭数据
        self.df_jiating = pd.read_sql(session.query(A864).statement, session.bind)
        hrlog.info("1.1 数据读取: 家庭成员读取完成")
        #社会兼职
        self.df_jianzhi = pd.read_sql(session.query(A865).statement, session.bind)
        hrlog.info("1.1 数据读取: 社会兼职读取完成")
        #2.读取工作成长数据
        #年度考核数据
        self.df_kaohe = pd.read_sql(session.query(A875).statement, session.bind)
        #龙虎榜数据
        self.df_longhu = pd.read_sql(session.query(Gxlygydjx).statement, session.bind)
        self.df_xulie = pd.read_sql(session.query(EmployeeProfessionalSequenceModel).statement, session.bind)
        hrlog.info("1.1 数据读取: 工作成长数据读取完成")
        #3.读取工作经历数据
        #工作经历数据
        self.df_working = pd.read_sql(session.query(A866).statement, session.bind)
        hrlog.info("1.1 数据读取: 工作经历数据读取完成")
        #4.读取工作情况数据
        #KOL
        self.df_kol = pd.read_sql(session.query(Kol).statement,session.bind)
        #工作日志
        self.df_journal = pd.read_sql(session.query(A8187).statement,session.bind)
        #考勤
        self.df_kaoqin = pd.read_sql(session.query(K_month).statement, session.bind)
        #考核
        self.df_kaohe = pd.read_sql(session.query(A875).statement, session.bind)
        #龙虎榜
        self.df_longhu = pd.read_sql(session.query(Gxlygydjx).statement, session.bind)
        hrlog.info("1.1 数据读取: 工作情况数据读取完成")
        #5.读取行外经历数据
        #6.读取荣誉表彰数据
        self.df_honor = pd.read_sql(session.query(A815).statement, session.bind)
        hrlog.info("1.1 数据读取: 荣誉表彰数据读取完成")
        #7.读取违规处分数据
        self.df_weigui = pd.read_sql(session.query(A8145).statement, session.bind)
        self.df_chengchu = pd.read_sql(session.query(A8192).statement, session.bind)
        hrlog.info("1.1 数据读取: 违规处分数据读取完成")
        #8.读取学习提升数据
        #教育类型码表
        self.df_code_education_type = pd.read_sql(session.query(Bm_jylx).statement, session.bind)
        #是否最高码表
        self.df_code_is_or_not = pd.read_sql(session.query(Bm_sf0).statement, session.bind)
        #学历编码
        self.df_code_xueli = pd.read_sql(session.query(Bmyh_xl).statement, session.bind)
        #学位编码
        self.df_code_xuewei = pd.read_sql(session.query(Bmyh_xw).statement, session.bind)
        #内训师数据
        self.df_peixun = pd.read_sql(session.query(Empat17).statement, session.bind)
        #学习平台数据
        self.df_pingtai = pd.read_sql(session.query(Empat18).statement, session.bind)
        #全员轮训数据
        self.df_lunxun = pd.read_sql(session.query(Empat19).statement,session.bind)
        #教育数据
        self.df_jiaoyu = pd.read_sql(session.query(A04).statement, session.bind)
        #高校数据
        self.df_gaoxiao = pd.read_sql(session.query(Bm_gxsjb).statement, session.bind)
        hrlog.info("1.1 数据读取: 学习提升数据读取完成")
        #9.读取综合评测数据
        self.df_nengli = pd.read_sql(session.query(Tability).statement, session.bind) 
        self.df_xingge = pd.read_sql(session.query(Tpersonality).statement, session.bind)
        hrlog.info("1.1 数据读取: 综合评测数据读取完成")
        #10.读取专业能力数据
        self.df_zhengshu = pd.read_sql(session.query(A832).statement, session.bind)
        self.df_zhengshu_score = pd.read_sql(session.query(ZYXLJFB).statement, session.bind)
        hrlog.info("1.1 数据读取: 专业能力数据读取完成")
        hrlog.info("1.1 数据读取完成")


    def get_common_score(self):
        #计算宽表
        #计算各个指标得分
        df_dimn_gxtp_score = cal_gxtp_score(self.df_base, self.df_jiating, self.df_jianzhi)
        df_dimn_gzcz_score = cal_gzcz_score(self.now_year, self.df_base, self.df_kaohe, self.df_longhu, self.df_xulie)
        df_dimn_gzlc_score = cal_gzlc_score(self.df_base, self.df_xulie, self.df_working)
        df_dimn_gzqk_score = cal_gzqk_score(self.now_year, self.df_base, self.df_xulie, self.df_kol, self.df_journal, self.df_kaoqin,\
                                            self.df_kaohe, self.df_longhu)
        df_dimn_hwjl_score = cal_hwjl_score(self.now_year, self.df_base, self.df_working)
        df_dimn_rybz_score = cal_rybz_score(self.now_year, self.df_honor, self.df_base)
        df_dimn_wgcc_score = cal_wgcc_score(self.now_year, self.df_weigui, self.df_base, self.df_chengchu)
        df_dimn_xxts_score = cal_xxts_score(self.now_year, self.df_base, self.df_code_education_type, self.df_code_is_or_not,\
                                            self.df_code_xueli, self.df_code_xuewei, self.df_peixun, self.df_pingtai, self.df_lunxun,\
                                            self.df_jiaoyu, self.df_gaoxiao)
        df_dimn_zhpc_score = cal_zhpc_score(self.df_nengli, self.df_xingge, self.df_base)
        df_dimn_zynl_score = cal_zynl_score(self.df_base, self.df_code_education_type, self.df_code_is_or_not, self.df_code_xueli,\
                                            self.df_code_xuewei, self.df_jiaoyu, self.df_gaoxiao, self.df_zhengshu, self.df_zhengshu_score)
        #合并各个指标得分
        df_result = pd.merge(self.df_base[['a0188', 'a0190', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101']], df_dimn_gxtp_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_gzcz_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_gzlc_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_gzqk_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_hwjl_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_rybz_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_wgcc_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_xxts_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_zhpc_score, on='a0188', how='left')
        df_result = pd.merge(df_result, df_dimn_zynl_score, on='a0188', how='left')
        
        return df_result


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
                    # if col_name not in ['base_dqxl', '']
                
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

    def cal_score_main(self):
        #1.1从数据库读取数据
        self.get_source_data()
        print(self.get_common_score())
        # df_employee_seqc = pd.read_sql(session.query(EmployeeProfessionalSequenceModel).statement, session.bind)
        # df_base_score = pd.merge(df_base_score, df_employee_seqc[['user_id', 'lvl2_professional_sequence']], on = 'user_id', how='left')
        # #计算员工序列得分
        # df_seqc_score = cal_score(df_base_score, df_weights)
        # print(df_seqc_score.columns)
        # cal_rank(df_seqc_score, df_employee_seqc)
        # print(df_score)


if __name__ == '__main__':
    employeeScore = EmployeeScoreModel(now_year='2022')
    employeeScore.cal_score_main()











