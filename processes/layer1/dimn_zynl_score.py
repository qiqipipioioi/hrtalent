'''
计算专业能力得分
'''
# !/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime


def cal_zynl_score(df_base, df_code_education_type, df_code_is_or_not, df_code_xueli, df_code_xuewei,\
                                    df_jiaoyu, df_gaoxiao, df_zhengshu, df_zhengshu_score):
    # 全日制得分
    school_shuangyiliu = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfsyl'] == 1]['mc0000'].to_list()])
    school_211 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sf'] == 1]['mc0000'].to_list()])
    school_985 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfjbw'] == 1]['mc0000'].to_list()])
    school_qs100 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['qs100'] == 1]['mc0000'].to_list()])
    school_qs100_200 = set([i.split('（')[0] for i in df_gaoxiao[(df_gaoxiao['sfqs2'] == 1) & (df_gaoxiao['qs100'] == 1)]['mc0000'].to_list()])

    df_jiaoyu_quanrizhi = df_jiaoyu[df_jiaoyu['a0447'] == df_code_education_type[df_code_education_type['mc0000'] == '全日制']['bm0000'].values[0]]
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
            if x['a0429'] == df_code_xueli.loc[df_code_xueli['mc0000'] == '博士研究生', 'bm0000'].values[0] or x['a0440'] == df_code_xuewei.loc[
                df_code_xuewei['mc0000'] == '博士学位', 'bm0000'].values[0]:
                base_score = 100
                if before_2001:
                    base_score = 200
                else:
                    base_score = 180

                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.3
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.2
                if x['a0429'] == df_code_xueli.loc[df_code_xueli['mc0000'] == '博士研究生', 'bm0000'].values[0] and x['a0440'] == df_code_xuewei.loc[
                    df_code_xuewei['mc0000'] == '博士学位', 'bm0000'].values[0]:
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

            elif x['a0429'] in [df_code_xueli.loc[df_code_xueli['mc0000'] == '硕士研究生', 'bm0000'].values[0],
                                df_code_xueli.loc[df_code_xueli['mc0000'] == '硕士', 'bm0000'].values[0],
                                df_code_xueli.loc[df_code_xueli['mc0000'] == '双硕士', 'bm0000'].values[0]] or x['a0440'] == df_code_xuewei.loc[
                df_code_xuewei['mc0000'] == '硕士学位', 'bm0000'].values[0]:
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
            elif x['a0429'] in [df_code_xueli.loc[df_code_xueli['mc0000'] == '大学本科', 'bm0000'].values[0],
                                df_code_xueli.loc[df_code_xueli['mc0000'] == '双本科', 'bm0000'].values[0]] or x['a0440'] == df_code_xuewei.loc[
                df_code_xuewei['mc0000'] == '学士学位', 'bm0000'].values[0]:
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
            elif x['a0429'] in [df_code_xueli.loc[df_code_xueli['mc0000'] == '大学专科', 'bm0000'].values[0],
                                df_code_xueli.loc[df_code_xueli['mc0000'] == '双大专', 'bm0000'].values[0]]:
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
            elif x['a0429'] in [df_code_xueli.loc[df_code_xueli['mc0000'] == '中等专科', 'bm0000'].values[0],
                                df_code_xueli.loc[df_code_xueli['mc0000'] == '高中', 'bm0000'].values[0]]:
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


    print(df_jiaoyu_quanrizhi)
    df_jiaoyu_quanrizhi['学校得分'] = df_jiaoyu_quanrizhi.apply(cal_quanrizhi_score, axis=1)

    df_jiaoyu_quanrizhi_group = df_jiaoyu_quanrizhi.groupby(['a0188']).apply(lambda x: x['学校得分'].max())
    df_jiaoyu_quanrizhi_group.rename('全日制教育得分', inplace=True)

    # 职称情况得分

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
    df_zhengshu_score.rename(columns={'mc': 'a83211'}, inplace=True)
    df_zhengshu_defen = pd.merge(df_zhengshu[['a0188', 'a83211']], df_zhengshu_score[['a83211', 'type', 'grade', 'fz']],
                                 on='a83211', how='left')

    def cal_zhengshu_score(x):
        final_score = 0
        zhengshu_dict = {}
        for _, row in x.iterrows():
            if not pd.isna(row['fz']):
                if not pd.isna(row['type']):
                    if row['type'] in zhengshu_dict:
                        zhengshu_dict[row['type']] = max(row['fz'], zhengshu_dict[row['type']])
                    else:
                        zhengshu_dict[row['type']] = row['fz']
                else:
                    final_score += row['fz']
        for k in zhengshu_dict:
            final_score += zhengshu_dict[k]

        return final_score

    df_zhengshu_defen_g = df_zhengshu_defen.groupby(['a0188']).apply(cal_zhengshu_score)
    df_zhengshu_defen_g.rename('技术资格情况得分', inplace=True)

    df_result = df_base[['a0188', '职称情况得分']]
    df_result = pd.merge(df_result, df_jiaoyu_quanrizhi_group, on='a0188', how='left')
    df_result = pd.merge(df_result, df_zhengshu_defen_g, on='a0188', how='left')

    df_result.rename(columns={'全日制教育得分': 'base_qrjy_score', '职称情况得分': 'base_zcqk_score',\
                               '技术资格情况得分': 'base_jszg_score'}, inplace=True)
    
    df_result = df_result.fillna(0)
    df_result = df_result[['a0188', 'base_qrjy_score', 'base_zcqk_score', 'base_jszg_score']]

    return df_result
