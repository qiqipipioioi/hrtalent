'''
计算专业能力得分
'''
# !/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time
import re
from models.layer1_model import A01, A04, Bm_gxsjb, A832, Bm_jylx, Bm_sf0, E01, Bmyh_xl, Bmyh_xw


def cal_professional_ability_score(session):
    # 岗位编码
    position_code = pd.read_sql(session.query(E01).statement, session.bind)

    # 教育类型码表
    code_education_type = pd.read_sql(session.query(Bm_jylx).statement, session.bind)

    # 是否最高码表
    code_is_or_not = pd.read_sql(session.query(Bm_sf0).statement, session.bind)

    # 学历编码
    code_xueli = pd.read_sql(session.query(Bmyh_xl).statement, session.bind)

    # 学位编码
    code_xuewei = pd.read_sql(session.query(Bmyh_xw).statement, session.bind)

    # 教育情况，教育背景
    df_jiaoyu = pd.read_sql(session.query(A04).statement, session.bind)

    # 高校数据
    df_gaoxiao = pd.read_sql(session.query(Bm_gxsjb).statement, session.bind)

    school_shuangyiliu = set([i.split('（')[0] for i in df_gaoxiao[
        df_gaoxiao['sfsyl'] == code_is_or_not.loc[code_is_or_not['mc0000'] == '是', 'bm0000']]['mc0000'].to_list()])
    school_211 = set([i.split('（')[0] for i in
                      df_gaoxiao[df_gaoxiao['sf'] == code_is_or_not.loc[code_is_or_not['mc0000'] == '是', 'bm0000']][
                          'mc0000'].to_list()])
    school_985 = set([i.split('（')[0] for i in
                      df_gaoxiao[df_gaoxiao['sfjbw'] == code_is_or_not.loc[code_is_or_not['mc0000'] == '是', 'bm0000']][
                          'mc0000'].to_list()])
    school_qs100 = set([i.split('（')[0] for i in
                        df_gaoxiao[df_gaoxiao['qs100'] == code_is_or_not.loc[code_is_or_not['mc0000'] == '是', 'bm0000']][
                            'mc0000'].to_list()])
    school_qs100_200 = set([i.split('（')[0] for i in df_gaoxiao[
        (df_gaoxiao['sfqs2'] == code_is_or_not.loc[code_is_or_not['mc0000'] == '是', 'bm0000']) & (
                    df_gaoxiao['qs100'] == code_is_or_not.loc[code_is_or_not['mc0000'] == '否', 'bm0000'])][
        'mc0000'].to_list()])

    df_jiaoyu_quanrizhi = df_jiaoyu[
        df_jiaoyu['a0447'] == code_education_type[code_education_type['mc0000'] == '全日制', 'bm0000']]
    df_jiaoyu_quanrizhi = df_jiaoyu_quanrizhi[df_jiaoyu_quanrizhi['endtime'].notnull()]

    def cal_quanrizhi_score(x):
        before_2001 = x['endtime'] < datetime.datetime.strptime('2001-01-01','%Y-%m-%d')
        has_fujian = not(pd.isna(x['fjo']) and pd.isna(x['fjt']) and pd.isna(x['fj3']))
        final_score = 0
        if x is None:
            final_score = 40
        else:
            base_score = 50
            school_coe = 1
            zhengshu_coe = 0.9
            if x['a0429'] == code_xueli.loc[code_xueli['mc0000'] == '博士研究生', 'bm0000'] or x['a0440'] == code_xuewei.loc[
                code_xuewei['mc0000'] == '博士学位', 'bm0000']:
                base_score = 100
                if before_2001:
                    base_score = 200
                else:
                    base_score = 180

                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.3
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.2
                if x['a0429'] == code_xueli.loc[code_xueli['mc0000'] == '博士研究生', 'bm0000'] and x['a0440'] == code_xuewei[
                    code_xuewei['mc0000'] == '博士学位', 'bm0000']:
                    zhengshu_coe = 1
                else:
                    zhengshu_coe = 0.8

                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0

            elif x['a0429'] in [code_xueli.loc[code_xueli['mc0000'] == '硕士研究生', 'bm0000'],
                                code_xueli.loc[code_xueli['mc0000'] == '硕士', 'bm0000'],
                                code_xueli.loc[code_xueli['mc0000'] == '双硕士', 'bm0000']] or x['a0440'] == code_xuewei.loc[
                code_xuewei['mc0000'] == '硕士学位', 'bm0000']:
                if before_2001:
                    base_score = 150
                else:
                    base_score = 140

                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.3
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.2
                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0
            elif x['a0429'] in [code_xueli.loc[code_xueli['mc0000'] == '大学本科', 'bm0000'],
                                code_xueli.loc[code_xueli['mc0000'] == '双本科', 'bm0000']] or x['a0440'] == code_xuewei.loc[
                code_xuewei['mc0000'] == '学士学位', 'bm0000']:
                if before_2001:
                    base_score = 120
                else:
                    base_score = 100
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.3
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.2
                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0
            elif x['a0429'] in [code_xueli.loc[code_xueli['mc0000'] == '大学专科', 'bm0000'],
                                code_xueli.loc[code_xueli['mc0000'] == '双大专', 'bm0000']]:
                if before_2001:
                    base_score = 90
                else:
                    base_score = 80
                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0
            elif x['a0429'] in [code_xueli.loc[code_xueli['mc0000'] == '中等专科', 'bm0000'],
                                code_xueli.loc[code_xueli['mc0000'] == '高中', 'bm0000']]:
                if before_2001:
                    base_score = 70
                else:
                    base_score = 60
                if before_2001:
                    if has_fujian:
                        zhengshu_coe = 1.3
                    else:
                        zhengshu_coe = 1.1
                else:
                    if has_fujian:
                        zhengshu_coe = 1
                    else:
                        zhengshu_coe = 0
            else:
                base_score = 50

            final_score = base_score * school_coe * zhengshu_coe

        return final_score

    df_jiaoyu_quanrizhi['学校得分'] = df_jiaoyu_quanrizhi.apply(cal_quanrizhi_score, axis=1)

    df_jiaoyu_quanrizhi_group = df_jiaoyu_quanrizhi.groupby(['a0188']).apply(lambda x: x['学校得分'].max())
    df_jiaoyu_quanrizhi_group.rename('全日制教育得分', inplace=True)

    # 职称情况得分
    # 员工统计
    df_base = pd.read_sql(session.query(A01).statement, session.bind)
    df_base[['a0188', 'a0101', 'dept_1', 'dept_2', 'dept_code', 'e0101', 'a01687']]

    # 筛选出非高管和首席的员工
    # df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['dept_code'] != position_code.loc[position_code['mc0000'] == '高管', 'dept_code']]
    df_base = df_base[df_base['e0101'].apply(lambda x: '首席' not in x)]

    def cal_zhicheng_score(x):
        final_score = 20
        if x == '高级':
            final_score = 100
        elif x == '中级':
            final_score = 60
        elif x == '初级':
            final_score = 20
        return final_score

    df_base['职称情况得分'] = df_base['a01687'].apply(cal_zhicheng_score)

    # 技术资格得分
    df_zhengshu_score = pd.read_excel('seqdata\江南农商银行_专业序列资质标签加分表 v5 20230713.xlsx', sheet_name='Sheet3')
    df_zhengshu = pd.read_sql(session.query(A832).statement, session.bind)
    df_zhengshu_defen = pd.merge(df_zhengshu[['a0188', 'a83213']], df_zhengshu_score[['a83213', '名称', '等级', '标签得分']],
                                 on='a83213', how='left')

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

    df_zhengshu_defen_g = df_zhengshu_defen.groupby(['a0188']).apply(cal_zhengshu_score)
    df_zhengshu_defen_g.rename('技术资格情况得分', inplace=True)

    df_result = df_base[['a0188', '职称情况得分']]
    df_result = pd.merge(df_result, df_jiaoyu_quanrizhi_group, on='a0188', how='left')
    df_result = pd.merge(df_result, df_zhengshu_defen_g, on='a0188', how='left')

    return df_result
