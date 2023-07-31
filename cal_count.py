'''
员工信息统计
'''
#coding=utf-8

import pandas as pd
import numpy as np
import json


df_employee = pd.read_excel('data/员工序列评价得分_排名.xlsx', dtype=str)

def calculate_department_common_count(df_employee):
    #统计各个部门员工综合积分各个等级的人数, 以及占比

    df_department_lvl_common = df_employee[['一级机构', '员工积分综合等级', 'No.']].groupby(['一级机构', '员工积分综合等级']).count()
    df_department_lvl_common.rename(columns={'No.': '各级人数'}, inplace=True)
    df_department_lvl_common.reset_index(inplace=True)
    df_department_common = df_employee[['一级机构', 'No.']].groupby(['一级机构']).count()
    df_department_common.rename(columns={'No.': '机构人数'}, inplace=True)
    df_department_common.reset_index(inplace=True)
    df_department_lvl_common = pd.merge(df_department_lvl_common, df_department_common, on='一级机构', how='left')
    df_department_lvl_common['占比'] = df_department_lvl_common['各级人数'] / df_department_lvl_common['机构人数']
    print(df_department_lvl_common)


def calculate_department_xulie_count(df_employee):
    #统计各部门各序列各等级人数以及占比
    df_department_xulie_lvl = df_employee[['一级机构', '二级序列', '员工积分序列等级', 'No.']].groupby(['一级机构',  '二级序列', '员工积分序列等级']).count()
    df_department_xulie_lvl.rename(columns={'No.': '各级人数'}, inplace=True)
    df_department_xulie_lvl.reset_index(inplace=True)
    df_department_xulie = df_employee[['一级机构', '二级序列', 'No.']].groupby(['一级机构', '二级序列']).count()
    df_department_xulie.rename(columns={'No.': '序列人数'}, inplace=True)
    df_department_xulie.reset_index(inplace=True)
    df_department_xulie_lvl = pd.merge(df_department_xulie_lvl, df_department_xulie, on=['一级机构', '二级序列'], how='left')
    df_department_xulie_lvl['占比'] = df_department_xulie_lvl['各级人数'] / df_department_xulie_lvl['序列人数']
    print(df_department_xulie_lvl)

def calculate_department_xulie_total_count(df_employee):
    #统计各部门序列等级人数以及占比
    df_department_xulie_total_lvl = df_employee[['一级机构', '员工积分序列等级', 'No.']].groupby(['一级机构', '员工积分序列等级']).count()
    df_department_xulie_total_lvl.rename(columns={'No.': '各级人数'}, inplace=True)
    df_department_xulie_total_lvl.reset_index(inplace=True)
    df_department_xulie_total = df_employee[['一级机构', 'No.']].groupby(['一级机构']).count()
    df_department_xulie_total.rename(columns={'No.': '序列人数'}, inplace=True)
    df_department_xulie_total.reset_index(inplace=True)
    df_department_xulie_total_lvl = pd.merge(df_department_xulie_total_lvl, df_department_xulie_total, on=['一级机构'], how='left')
    df_department_xulie_total_lvl['占比'] = df_department_xulie_total_lvl['各级人数'] / df_department_xulie_total_lvl['序列人数']
    print(df_department_xulie_total_lvl)


def calculate_common_count(df_employee):
    #统计全行员工综合积分各个等级的人数, 以及占比

    df_lvl_common = df_employee[['员工积分综合等级', 'No.']].groupby(['员工积分综合等级']).count()
    df_lvl_common.rename(columns={'No.': '各级人数'}, inplace=True)
    df_lvl_common['占比'] = df_lvl_common['各级人数'] / df_lvl_common['No.'].count()

    print(df_lvl_common)

def calculate_xulie_count(df_employee):
    #统计全行各序列各等级人数以及占比
    df_xulie_lvl = df_employee[['二级序列', '员工积分序列等级', 'No.']].groupby(['二级序列', '员工积分序列等级']).count()
    df_xulie_lvl.rename(columns={'No.': '各级人数'}, inplace=True)
    df_xulie_lvl.reset_index(inplace=True)
    df_xulie = df_employee[['二级序列', 'No.']].groupby(['二级序列']).count()
    df_xulie_lvl.rename(columns={'No.': '序列人数'}, inplace=True)
    df_xulie_lvl.reset_index(inplace=True)
    df_xulie_lvl = pd.merge(df_xulie_lvl, df_xulie, on=['二级序列'], how='left')
    df_xulie_lvl['占比'] = df_xulie_lvl['各级人数'] / df_xulie_lvl['序列人数']
    print(df_xulie_lvl)


def calculate_common_count(df_employee):
    #统计所有序列等级的人数以及占比

    df_xulie_total = df_employee[['员工积分序列等级', 'No.']].groupby(['员工积分序列等级']).count()
    df_xulie_total.rename(columns={'No.': '各级人数'}, inplace=True)
    df_xulie_total['占比'] = df_xulie_total['各级人数'] / df_xulie_total['No.'].count()

    print(df_xulie_total)


