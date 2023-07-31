'''
计算推荐建议
'''
#coding=utf-8

import pandas as pd
import numpy as np
from utils.read_configs import read_relations
from processes.layer2.advise_components import cal_guanxituopu_advise, cal_xuexitisheng_advise,\
                                               cal_hangwaijingli_advise, cal_zhuanyenengli_advise,\
                                               cal_weiguichengchu_advise, cal_rongyubiaozhang_advise,\
                                               cal_gongzuochengzhang_advise, cal_gongzuolicheng_advise,\
                                               cal_gongzuoqingkuang_advise

XULIE_SET, BIAOQIAN_SET, YUYI_BIAOQIAN_DICT, WEIDU_YUYI_DICT = read_relations()


def cal_xulie_score_range(df_all):
    #计算每个序列的每个等级的分数的最大值、最小值、平均值
    
    # df_all_1 = df_all[['二级序列', '员工积分序列等级', '所在序列得分'] + list(BIAOQIAN_SET)]
    df_xuelie_lvl = df_all[['二级序列', '员工积分序列等级', '所在序列得分']]

    df_xulie_mean = df_xuelie_lvl.groupby(['二级序列', '员工积分序列等级']).mean()
    df_xulie_mean.rename(columns={'所在序列得分':'所在序列得分平均分'}, inplace=True)
    df_xulie_max = df_xuelie_lvl.groupby(['二级序列', '员工积分序列等级']).max()
    df_xulie_max.rename(columns={'所在序列得分':'所在序列得分最高分'}, inplace=True)
    df_xulie_min = df_xuelie_lvl.groupby(['二级序列', '员工积分序列等级']).min()
    df_xulie_min.rename(columns={'所在序列得分':'所在序列得分最低分'}, inplace=True)

    df_xulie_lvl_score = pd.merge(df_xulie_mean, df_xulie_max, on=['二级序列', '员工积分序列等级'], how='left')
    df_xulie_lvl_score = pd.merge(df_xulie_lvl_score, df_xulie_min, on=['二级序列', '员工积分序列等级'], how='left')
    df_xulie_lvl_score.reset_index(inplace=True)
    return df_xulie_lvl_score


def cal_weidu_yuyi_mean_score(df_all):
    #计算各序列的语义和维度的平均分
    #把基础标签合并为语义
    for yuyi in YUYI_BIAOQIAN_DICT:
        for biaoqian_pair in YUYI_BIAOQIAN_DICT[yuyi]:
            if biaoqian_pair[0] not in df_all.columns:
                df_all[yuyi] = df_all[biaoqian_pair[0]].apply(lambda x: 100 if x> 100 else x) * biaoqian_pair[1] / 100
            else:
                df_all[yuyi] += df_all[biaoqian_pair[0]].apply(lambda x: 100 if x> 100 else x) * biaoqian_pair[1] / 100
    df_all_yuyi = df_all[['No.', '二级序列', '员工积分序列等级'] + list(YUYI_BIAOQIAN_DICT.keys())]
    #把语义合并为维度
    for weidu in WEIDU_YUYI_DICT:
        df_all_yuyi[weidu] = df_all_yuyi[WEIDU_YUYI_DICT[weidu]].sum(axis=1)

    #计算语义在各个序列不同等级上的平均值
    df_yuyi_mean = df_all_yuyi.groupby(['二级序列', '员工积分序列等级']).mean()
    df_yuyi_mean.reset_index(inplace=True)
    return df_yuyi_mean, df_all_yuyi


def cal_target_lvl(df_all, df_xulie_lvl_score):
    #计算目标序列等级
    def get_xulie_lvl(xulie, score):
        #已知序列和分数，求等级
        xulie_zishen_min = df_xulie_lvl_score[(df_xulie_lvl_score['二级序列'] == xulie) & (df_xulie_lvl_score['员工积分序列等级'] == '资深')]['所在序列得分最低分'].values[0]
        xulie_gaoji_max = df_xulie_lvl_score[(df_xulie_lvl_score['二级序列'] == xulie) & (df_xulie_lvl_score['员工积分序列等级'] == '高级')]['所在序列得分最高分'].values[0]
        xulie_gaoji_min = df_xulie_lvl_score[(df_xulie_lvl_score['二级序列'] == xulie) & (df_xulie_lvl_score['员工积分序列等级'] == '高级')]['所在序列得分最低分'].values[0]
        xulie_zhongji_max = df_xulie_lvl_score[(df_xulie_lvl_score['二级序列'] == xulie) & (df_xulie_lvl_score['员工积分序列等级'] == '中级')]['所在序列得分最高分'].values[0]
        xulie_zhongji_min = df_xulie_lvl_score[(df_xulie_lvl_score['二级序列'] == xulie) & (df_xulie_lvl_score['员工积分序列等级'] == '中级')]['所在序列得分最低分'].values[0]
        xulie_chuji_max = df_xulie_lvl_score[(df_xulie_lvl_score['二级序列'] == xulie) & (df_xulie_lvl_score['员工积分序列等级'] == '初级')]['所在序列得分最高分'].values[0]

        now_lvl = '未知'
        if score >= xulie_zishen_min:
            now_lvl = '资深'
        elif score >= xulie_gaoji_min and score < xulie_gaoji_max:
            now_lvl = '高级'
        elif score >= xulie_zhongji_min and score < xulie_zhongji_max:
            now_lvl = '中级'
        elif score < xulie_chuji_max:
            now_lvl = '初级'

        result = None 
        if now_lvl == '资深':
            result = now_lvl + '||' + '已经最高'
        elif now_lvl == '高级':
            fencha = (xulie_zishen_min - score) / xulie_zishen_min
            if fencha <= 0.2:
                result = now_lvl + '|' + '资深' + '|' + '稍有差距'
            elif 0.4 >= fencha and fencha > 0.2:
                result = now_lvl + '|' + '资深' + '|' + '存在差距'
            elif fencha > 0.4:
                result = now_lvl + '|' + '资深' + '|' + '差距较远'
        elif now_lvl == '中级':
            fencha = (xulie_gaoji_min - score) / xulie_gaoji_min
            if fencha <= 0.2:
                result = now_lvl + '|' + '高级' + '|' + '稍有差距'
            elif 0.4 >= fencha and fencha > 0.2:
                result = now_lvl + '|' + '高级' + '|' + '存在差距'
            elif fencha > 0.4:
                result = now_lvl + '|' + '高级' + '|' + '差距较远'
        elif now_lvl == '初级':
            fencha = (xulie_zhongji_min - score) / xulie_zhongji_min
            if fencha <= 0.2:
                result = now_lvl + '|' + '中级' + '|' + '稍有差距'
            elif 0.4 >= fencha and fencha > 0.2:
                result = now_lvl + '|' + '中级' + '|' + '存在差距'
            elif fencha > 0.4:
                result = now_lvl + '|' + '中级' + '|' + '差距较远'
        else:
            result = now_lvl + '|' + '未知' + '|' + '未知'
        if result is None:
            print(xulie, score, now_lvl, fencha)
        return result
    
    #判断每个员工在每个序列里应该处于什么等级
    df_all_every_xulie = df_all[['No.'] + [ i + '总分' for i in list(XULIE_SET)]]
    #判断df_all_every_xulie的每个序列分在df_xulie_lvl_score处于哪个等级的最小值和最大值范围内
    for xulie in list(XULIE_SET):
        if xulie in df_xulie_lvl_score['二级序列'].drop_duplicates().values:
            df_all_every_xulie[xulie + '文本'] = df_all_every_xulie[xulie + '总分'].apply(lambda x: get_xulie_lvl(xulie, x))
            df_all_every_xulie[xulie + '等级'] = df_all_every_xulie[xulie + '文本'].apply(lambda x: x.split('|')[0])
            df_all_every_xulie[xulie + '目标等级'] = df_all_every_xulie[xulie + '文本'].apply(lambda x: x.split('|')[1])
            df_all_every_xulie[xulie + '目标等级差距'] = df_all_every_xulie[xulie + '文本'].apply(lambda x: x.split('|')[2])
            df_all_every_xulie.drop(xulie+'文本', axis=1, inplace=True)
        else:
            print(xulie)
    return df_all_every_xulie
    

def cal_every_advise(df_all_every_xulie, df_all_yuyi, df_yuyi_mean):
    #计算每个序列每个维度的推荐建议
    target_list =  [i + '目标等级' for i in list(XULIE_SET) if (i+ '目标等级') in df_all_every_xulie.columns.to_list()]
    df_all_merge = pd.merge(df_all_yuyi, df_all_every_xulie[['No.'] + target_list], on = 'No.', how='inner')
    df_advise = df_all_merge[['No.'] + target_list]
    for xulie in XULIE_SET:
        if xulie + '目标等级' in df_all_merge.columns.to_list():
            # print(df_all_merge.apply(lambda x: print(x[xulie+'目标等级']), axis=1))
            df_advise[xulie + '关系拓扑建议'] = df_all_merge.apply(lambda x: cal_guanxituopu_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '学习提升建议'] = df_all_merge.apply(lambda x: cal_xuexitisheng_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '行外经历建议'] = df_all_merge.apply(lambda x: cal_hangwaijingli_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '工作成长建议'] = df_all_merge.apply(lambda x: cal_gongzuochengzhang_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '专业能力建议'] = df_all_merge.apply(lambda x: cal_zhuanyenengli_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '违规惩处建议'] = df_all_merge.apply(lambda x: cal_weiguichengchu_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '荣誉表彰建议'] = df_all_merge.apply(lambda x: cal_rongyubiaozhang_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '工作情况建议'] = df_all_merge.apply(lambda x: cal_gongzuoqingkuang_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
            df_advise[xulie + '工作历程建议'] = df_all_merge.apply(lambda x: cal_gongzuolicheng_advise(x, df_yuyi_mean, xulie, x[xulie+'目标等级']), axis=1)
    return df_advise


def advise_main():
    #主函数
    df_rank = pd.read_excel('data/员工序列评价得分_排名.xlsx')
    df_score = pd.read_excel('data/员工原始积分.xlsx')
    df_all = pd.merge(df_rank, df_score[['No.'] + list(BIAOQIAN_SET)], on='No.', how='left')
    df_xulie_lvl_score = cal_xulie_score_range(df_all)
    df_yuyi_mean, df_all_yuyi = cal_weidu_yuyi_mean_score(df_all)
    df_all_every_xulie = cal_target_lvl(df_all, df_xulie_lvl_score)
    df_advise = cal_every_advise(df_all_every_xulie, df_all_yuyi, df_yuyi_mean)

            
