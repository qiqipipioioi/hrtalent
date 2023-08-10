'''
学习提升得分
'''
# !/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time


def cal_xxts_score(now_year, df_base, df_code_education_type, df_code_is_or_not, df_code_xueli, df_code_xuewei, df_peixun,\
                                  df_pingtai, df_lunxun, df_jiaoyu, df_gaoxiao):
    # 内训师
    df_peixun = df_peixun[df_peixun['years'] == now_year]
    # df_peixun.rename(columns={'a0190': 'a0188'}, inplace=True)
    df_peixun['考核得分'] = df_peixun['a81884'].apply(lambda x: 0 if x == '无' else int(x))

    def cal_neixunshi_score(x):
        lvl_score = 0
        if x['a81882'] == '初级内训师':
            lvl_score = 20
        elif x['a81882'] == '中级内训师':
            lvl_score = 30
        elif x['a81882'] == '高级内训师':
            lvl_score = 40
        elif x['a81882'] == '专家内训师':
            lvl_score = 50
        jifen_score = 0
        if x['a81884'] < 80:
            jifen_score = 0
        elif 80 <= x['a81884'] <= 85:
            jifen_score = 30
        elif 80 < x['a81884'] <= 90:
            jifen_score = 35
        elif 90 < x['a81884'] <= 95:
            jifen_score = 40
        elif 95 < x['a81884'] <= 100:
            jifen_score = 45
        elif x['a81884'] > 100:
            jifen_score = 50
        final_score = lvl_score + jifen_score
        return final_score

    df_peixun['内训师资格得分'] = df_peixun.apply(cal_neixunshi_score, axis=1)

    # 学习平台
    df_pingtai = df_pingtai[df_pingtai['years'] == now_year]
    # df_pingtai.rename(columns={'a0190': 'a0188'}, inplace=True)  # 工号 姓名

    df_pingtai['学习平台得分情况得分'] = df_pingtai['empat181'].astype(float)

    # 全员轮训
    df_lunxun = df_lunxun[df_lunxun['years'] == now_year]
    # df_lunxun.rename(columns={'a0188': 'a0188'}, inplace=True)

    def cal_lunxun_score(x):
        final_score = 0
        bixiuke_score = float(x['ReqCourses'])
        if x['OpenCourses'] == '无需参加':
            final_score = bixiuke_score
        else:
            final_score = (float(x['OpenCourses']) + bixiuke_score) / 2
        return final_score

    df_lunxun['全员轮训情况得分'] = df_lunxun.apply(cal_lunxun_score, axis=1)
    df_lunxun = df_lunxun[['a0188', '全员轮训情况得分']].groupby('a0188').max()

    # 在职教育得分
    school_shuangyiliu = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfsyl'] == 1]['mc0000'].to_list()])
    school_211 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sf'] == 1]['mc0000'].to_list()])
    school_985 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['sfjbw'] == 1]['mc0000'].to_list()])
    school_qs100 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['qs100'] == 1]['mc0000'].to_list()])
    school_qs100_200 = set([i.split('（')[0] for i in df_gaoxiao[(df_gaoxiao['sfqs2'] == 1) & (df_gaoxiao['qs100'] == 1)]['mc0000'].to_list()])

    df_jiaoyu_zaizhi = df_jiaoyu[df_jiaoyu['a0447'] == df_code_education_type[df_code_education_type['mc0000'] == '在职']['bm0000'].values[0]]
    df_jiaoyu_zaizhi = df_jiaoyu[df_jiaoyu['endtime'].notnull()]

    print(df_jiaoyu_zaizhi)


    def cal_zaizhi_score(x):
        before_2001 = x['endtime'] < datetime.datetime.strptime(
            '2001-01-01', '%Y-%m-%d')
        has_fujian = not (pd.isna(x['fjo']) and pd.isna(x['fjt']) and pd.isna(x['fj3']))

        final_score = 0
        if x is None:
            final_score = 0
        else:
            base_score = 0
            school_coe = 1.1
            zhengshu_coe = 1
            if x['a0429'] == df_code_xueli.loc[df_code_xueli['mc0000'] == '博士研究生', 'bm0000'].values[0] or x['a0440'] == df_code_xuewei.loc[
                df_code_xuewei['mc0000'] == '博士学位', 'bm0000'].values[0]:
                base_score = 100
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3

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
                    base_score = 100
                else:
                    base_score = 90
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3

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
                    base_score = 90
                else:
                    base_score = 80
                if x['a0431'] in school_qs100 or x['a0431'] in school_985:
                    school_coe = 1.5
                elif x['a0431'] in school_211 or x['a0431'] in school_shuangyiliu or x['a0431'] in school_qs100_200:
                    school_coe = 1.3

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
                    base_score = 80
                else:
                    base_score = 70

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
                base_score = 0

            final_score = base_score * school_coe * zhengshu_coe

        return final_score

    df_jiaoyu_zaizhi['学校得分'] = df_jiaoyu_zaizhi.apply(cal_zaizhi_score, axis=1)

    df_jiaoyu_zaizhi_group = df_jiaoyu_zaizhi.groupby(['a0188']).apply(lambda x: x['学校得分'].max())

    df_jiaoyu_zaizhi_group.rename('在职教育得分', inplace=True)


    df_result = pd.merge(df_base[['a0188']], df_peixun[['a0188', '内训师资格得分']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_pingtai[['a0188', '学习平台得分情况得分']], on='a0188', how='left')
    df_result = pd.merge(df_result, df_lunxun, on='a0188', how='left')
    df_result = pd.merge(df_result, df_jiaoyu_zaizhi_group, on='a0188', how='left')

    df_result.rename(columns={'内训师资格得分': 'base_nxzg_score', '学习平台得分情况得分': 'base_xxpt_score',\
                              '全员轮训情况得分': 'base_qylx_score', '在职教育得分': 'base_zzjy_score'}, inplace=True)

    df_result.fillna(0, inplace=True)

    df_result = df_result[['a0188', 'base_nxzg_score', 'base_xxpt_score', 'base_qylx_score', 'base_zzjy_score']]

    return df_result
