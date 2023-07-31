'''
计算专业能力得分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
import re


def cal_professional_ability_score():

    #教育情况
    df_jiaoyu = pd.read_excel('seqdata\jiaoyubeijing.xlsx', dtype=str)

    df_gaoxiao = pd.read_excel('seqdata\高校数据库v5.xlsx', dtype=str)

    school_shuangyiliu = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否双一流'] == '是']['学校名称'].to_list()])
    school_211 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否211'] == '是']['学校名称'].to_list()])
    school_985 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否985'] == '是']['学校名称'].to_list()])
    school_qs100 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否QS100'] == '是']['学校名称'].to_list()])
    school_qs100_200 = set([i.split('（')[0] for i in df_gaoxiao[(df_gaoxiao['是否QS200'] == '是') & (df_gaoxiao['是否QS100'] == '否')]['学校名称'].to_list()])

    df_jiaoyu_quanrizhi = df_jiaoyu[df_jiaoyu['教育类型'] == '全日制']


    def cal_quanrizhi_score(x):
        final_score = 0
        if x is None:
            final_score = 40
        else:
            base_score = 40
            school_coe = 1
            zhengshu_coe = 0.8
            if x['学历'] == '博士研究生' or x['学位'] == '博士学位':
                base_score = 100
                if x['学校'] in school_qs100 or x['学校'] in school_985:
                    school_coe = 1.5
                elif x['学校'] in school_211 or x['学校'] in school_shuangyiliu or x['学校'] in school_qs100_200:
                    school_coe = 1.3
                if x['学历'] == '博士研究生' and x['学位'] == '博士学位':
                    zhengshu_coe = 1
                else:
                    zhengshu_coe = 0.8
            elif x['学历'] in ['硕士研究生', '硕士', '双硕士'] or x['学位'] == '硕士学位':
                base_score = 90
                if x['学校'] in school_qs100 or x['学校'] in school_985:
                    school_coe = 1.5
                elif x['学校'] in school_211 or x['学校'] in school_shuangyiliu or x['学校'] in school_qs100_200:
                    school_coe = 1.3
                if x['学历'] in ['硕士研究生', '硕士', '双硕士'] and x['学位'] == '硕士学位':
                    zhengshu_coe = 1
                else:
                    zhengshu_coe = 0.8           
            elif x['学历'] in ['大学本科', '双本科'] or x['学位'] == '学士学位':
                base_score = 80
                if x['学校'] in school_qs100 or x['学校'] in school_985:
                    school_coe = 1.5
                elif x['学校'] in school_211 or x['学校'] in school_shuangyiliu or x['学校'] in school_qs100_200:
                    school_coe = 1.3
                if x['学历'] in ['大学本科', '双本科'] and x['学位'] == '学士学位':
                    zhengshu_coe = 1
                else:
                    zhengshu_coe = 0.8 
            elif x['学历'] in ['大学专科', '双大专'] :
                base_score = 60
            elif x['学历'] in ['中等专科', '高中'] :
                base_score = 50
            else:
                base_score = 40

            final_score = base_score * school_coe * zhengshu_coe

        return final_score


    df_jiaoyu_quanrizhi['学校得分'] = df_jiaoyu_quanrizhi.apply(cal_quanrizhi_score, axis=1)

    df_jiaoyu_quanrizhi_group = df_jiaoyu_quanrizhi.groupby(['员工号']).apply(lambda x: x['学校得分'].max())
    df_jiaoyu_quanrizhi_group.rename('全日制教育得分', inplace=True)

    #职称情况得分
    #员工统计
    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '聘任职业技术等级']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]


    def cal_zhicheng_score(x):
        final_score = 20
        if x == '高级':
            final_score = 100
        elif x == '中级':
            final_score = 60
        elif x == '初级':
            final_score = 20
        return final_score
    

    df_base['职称情况得分'] = df_base['聘任职业技术等级'].apply(cal_zhicheng_score)
    
    
    #技术资格得分
    df_zhengshu_score = pd.read_excel('seqdata\江南农商银行_专业序列资质标签加分表 v5 20230713.xlsx', sheet_name='Sheet3')
    df_zhengshu = pd.read_excel('seqdata\zhiyezhengshu.xlsx', dtype=str)
    df_zhengshu_defen = pd.merge(df_zhengshu[['员工号', '证书名称']], df_zhengshu_score[['证书名称', '名称', '等级', '标签得分']], on='证书名称', how='left')
    
    def cal_zhengshu_score(x):
        final_score = 0
        zhengshu_dict = {}
        for _, row in x.iterrows():
            if not pd.isna(row['标签得分']):
                if not pd.isna(row['名称']):
                    if row['名称'] in zhengshu_dict:
                        zhengshu_dict[row['名称']] = max(row['标签得分'], zhengshu_dict[row['名称']])
                    else:
                        zhengshu_dict[row['名称']] = row['标签得分']
                else:
                    final_score += row['标签得分']
        for k in zhengshu_dict:
            final_score += zhengshu_dict[k]
        
        return final_score


    df_zhengshu_defen_g = df_zhengshu_defen.groupby(['员工号']).apply(cal_zhengshu_score)
    df_zhengshu_defen_g.rename('技术资格情况得分', inplace=True)


    df_result = df_base[['员工号', '职称情况得分']]
    df_result = pd.merge(df_result, df_jiaoyu_quanrizhi_group, on='员工号', how='left')
    df_result = pd.merge(df_result, df_zhengshu_defen_g, on='员工号', how='left')

    return df_result




