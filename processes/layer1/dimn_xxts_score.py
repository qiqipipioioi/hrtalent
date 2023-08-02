'''
学习提升得分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import datetime
import time


def cal_learning_growing_up_score():

    #内训师
    df_peixun= pd.read_excel('seqdata\内训师、学习平台、全员轮训数据.xls', dtype=str, sheet_name='内训师')
    df_peixun.rename(columns={'工号':'员工号'}, inplace=True)

    df_peixun['考核得分'] = df_peixun['2022年末考核得分'].apply(lambda x: 0 if x == '无' else int(x))

    def cal_neixunshi_score(x):
        lvl_score = 0
        if x['内训师现等级'] == '初级内训师':
            lvl_score = 20
        elif x['内训师现等级'] == '中级内训师':
            lvl_score = 30
        elif x['内训师现等级'] == '高级内训师':
            lvl_score = 40
        elif x['内训师现等级'] == '专家内训师':
            lvl_score = 50
        jifen_score = 0
        if x['考核得分'] < 80:
            jifen_score = 0
        elif 80 <= x['考核得分'] <= 85:
            jifen_score = 30
        elif 80 < x['考核得分'] <= 90:
            jifen_score = 35
        elif 90 < x['考核得分'] <= 95:
            jifen_score = 40
        elif 95 < x['考核得分'] <= 100:
            jifen_score = 45
        elif x['考核得分'] > 100:
            jifen_score = 50
        final_score = lvl_score + jifen_score
        return final_score


    df_peixun['内训师资格得分'] = df_peixun.apply(cal_neixunshi_score, axis=1)


    #学习平台
    df_pingtai= pd.read_excel('seqdata\内训师、学习平台、全员轮训数据.xls', dtype=str, sheet_name='学习平台')
    df_pingtai.rename(columns={'工号':'员工号'}, inplace=True)

    df_pingtai['学习平台得分情况得分'] = df_pingtai['2022年学习平台总学分'].astype(float)

    #全员轮训
    df_lunxun= pd.read_excel('seqdata\内训师、学习平台、全员轮训数据.xls', dtype=str, sheet_name='2022年全员轮训')
    now_year = 2022
    df_lunxun = df_lunxun[df_lunxun['归属年份'].astype(int) == now_year]
    df_lunxun.rename(columns={'工号':'员工号'}, inplace=True)


    def cal_lunxun_score(x):
        final_score = 0
        bixiuke_score = float(x['必修课'])
        if x['公开课'] == '无需参加':
            final_score = bixiuke_score
        else:
            final_score = (float(x['公开课']) + bixiuke_score) / 2
        return final_score

    df_lunxun['全员轮训情况得分'] = df_lunxun.apply(cal_lunxun_score, axis=1)
    df_lunxun = df_lunxun[['员工号', '全员轮训情况得分']].groupby('员工号').max()


    #在职教育得分
    # bm_jylx，教育类型
    # bmyh_xl,学历
    # bmyh_xw,学位
    # bm_sf0,是否最高
    # 
    df_jiaoyu = pd.read_excel('seqdata\jiaoyubeijing.xlsx', dtype=str)
    df_gaoxiao = pd.read_excel('seqdata\高校数据库v5.xlsx', dtype=str)
    school_shuangyiliu = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否双一流'] == '是']['学校名称'].to_list()])
    school_211 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否211'] == '是']['学校名称'].to_list()])
    school_985 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否985'] == '是']['学校名称'].to_list()])
    school_qs100 = set([i.split('（')[0] for i in df_gaoxiao[df_gaoxiao['是否QS100'] == '是']['学校名称'].to_list()])
    school_qs100_200 = set([i.split('（')[0] for i in df_gaoxiao[(df_gaoxiao['是否QS200'] == '是') & (df_gaoxiao['是否QS100'] == '否')]['学校名称'].to_list()])


    df_jiaoyu_zaizhi = df_jiaoyu[df_jiaoyu['教育类型'] == '在职']
    df_jiaoyu_zaizhi = df_jiaoyu[df_jiaoyu['终止时间'].notnull()]


    def cal_zaizhi_score(x):
        before_2001 = datetime.datetime.strptime(x['终止时间'], '%Y-%m-%d %H:%M:%S') < datetime.datetime.strptime('2001-01-01', '%Y-%m-%d')
        has_fujian = not(pd.isna(x['学历附件']) and pd.isna(x['学位附件']) and pd.isna(x['学信网在线验证报告']))

        final_score = 0
        if x is None:
            final_score = 0
        else:
            base_score = 0
            school_coe = 1.1
            zhengshu_coe = 1
            if x['学历'] == '博士研究生' or x['学位'] == '博士学位':
                base_score = 100
                if x['学校'] in school_qs100 or x['学校'] in school_985:
                    school_coe = 1.5
                elif x['学校'] in school_211 or x['学校'] in school_shuangyiliu or x['学校'] in school_qs100_200:
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

            elif x['学历'] in ['硕士研究生', '硕士', '双硕士'] or x['学位'] == '硕士学位':
                if before_2001:
                    base_score = 100
                else:
                    base_score = 90
                if x['学校'] in school_qs100 or x['学校'] in school_985:
                    school_coe = 1.5
                elif x['学校'] in school_211 or x['学校'] in school_shuangyiliu or x['学校'] in school_qs100_200:
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
            elif x['学历'] in ['大学本科', '双本科'] or x['学位'] == '学士学位':
                if before_2001:
                    base_score = 90
                else:
                    base_score = 80
                if x['学校'] in school_qs100 or x['学校'] in school_985:
                    school_coe = 1.5
                elif x['学校'] in school_211 or x['学校'] in school_shuangyiliu or x['学校'] in school_qs100_200:
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
            elif x['学历'] in ['大学专科', '双大专'] :
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
            elif x['学历'] in ['中等专科', '高中'] :
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

    df_jiaoyu_zaizhi_group = df_jiaoyu_zaizhi.groupby(['员工号']).apply(lambda x: x['学校得分'].max())

    df_jiaoyu_zaizhi_group.rename('在职教育得分', inplace=True)

    df_base = pd.read_excel('seqdata\基本信息_20230620170630.xlsx', dtype=str)
    df_base[['员工号', '姓名', '一级机构', '二级机构', '中心', '岗位', '入行时间', '任现岗位时间','行员等级']]

    #筛选出非高管和首席的员工
    df_base = df_base[df_base['任职形式'] == '担任']
    df_base = df_base[df_base['中心'] != '高管']
    df_base = df_base[df_base['岗位'].apply(lambda x: '首席' not in x)]

    df_result = pd.merge(df_base[['员工号']], df_peixun[['员工号', '内训师资格得分']], on='员工号', how='left')
    df_result = pd.merge(df_result, df_pingtai[['员工号', '学习平台得分情况得分']], on='员工号', how='left')
    df_result = pd.merge(df_result, df_lunxun, on='员工号', how='left')
    df_result = pd.merge(df_result, df_jiaoyu_zaizhi_group, on='员工号', how='left')

    df_result.fillna(0, inplace=True)


    return df_result




