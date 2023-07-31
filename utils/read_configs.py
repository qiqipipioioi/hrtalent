#coding=utf-8
'''
读取配置文件
'''
import pandas as pd
import numpy as np
import json 


def read_lang():
    #读取语义模版
    lang_templates = json.load(open('config/lang_templates.json', 'r', encoding='utf-8'))
    lang_models = lang_templates['语义模版']
    return lang_models

def read_variables():
    #读取变量名
    variable_names = json.load(open('config/variable_names.json', 'r', encoding='utf-8'))
    return variable_names

def read_ranges():
    #读取各层级分数范围
    score_ranges = json.load(open('config/level_range.json', 'r', encoding='utf-8'))
    common_level_range = score_ranges['综合评分']
    seqc1_level_range = score_ranges['专业序列1']
    seqc2_level_range = score_ranges['专业序列2']
    return common_level_range, seqc1_level_range, seqc2_level_range


def read_relations():
    #读取各层级标签映射关系
    label_relations = json.load(open('config/label_relations.json', 'r', encoding='utf-8'))
    variable_names = json.load(open('config/variable_names.json', 'r', encoding='utf-8'))
    base_label_dict = variable_names['基础标签']
    lang_label_dict = variable_names['语义标签']
    dimn_label_dict = variable_names['维度标签']
    seqc_label_dict = variable_names['专业序列']
    base_with_sec_label_dict = variable_names['序列相关基础标签']

    lang_base_mapping = label_relations['语义标签-基础标签映射']
    dimn_lang_mapping = label_relations['维度标签-语义标签映射']
    #转化为英文字段
    lang_base_mapping = {lang_label_names[k]: [base_label_names[i] for i in v] for k, v in lang_base_mapping.items()}
    dimn_lang_mapping = {dimn_label_names[k]: [lang_label_names[i] for i in v] for k, v in dimn_lang_mapping.items()}

    return lang_base_mapping, dimn_lang_mapping, base_label_dict, lang_label_dict, dimn_label_dict, seqc_label_dict, base_with_sec_label_dict

if __name__ == '__main__':
    lang_base_mapping, dimn_lang_mapping, base_label_names, lang_label_names, dimn_label_names, seqc_label_names = read_relations()
    print(lang_base_mapping)
    print(dimn_lang_mapping)
    print(base_label_names)
    print(lang_label_names)
    print(dimn_label_names)
    print(seqc_label_names)



