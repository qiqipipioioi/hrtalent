'''
分别计算十个维度的建议语
'''
#coding=utf-8
import pandas as pd
import numpy as np
from utils.read_configs import read_lang


YUYI_MODELS = read_lang()


#关系拓扑维度
def cal_guanxituopu_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '关系拓扑'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['关系拓扑得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['关系拓展得分'].values[0]
    weidu_fencha =  (x['关系拓扑得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['关系拓展得分'] - yuyi1_target_score) / yuyi1_target_score
    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    elif weidu_fencha < 0 and weidu_fencha >= -0.2:
        lang1 = '稍有差距'
        lang2 = '提高关系拓展能力'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
        lang1 = '有差距'
        lang2 = '提高关系拓展能力'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    else:
        lang1 = '差距较远'
        lang2 = '提高关系拓展能力'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    return advise



#学习提升维度
def cal_xuexitisheng_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '学习提升'
    guanlian_weidu = '专业能力'
    guanlian_yuyi1 = '基础学历'

    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['学习提升得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['学历提升得分'].values[0]
    yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['行内培训得分'].values[0]
    guanlian_weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['专业能力得分'].values[0]
    guanlian_yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['基础学历得分'].values[0]
    weidu_fencha = (x['学习提升得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['学历提升得分'] - yuyi1_target_score) / yuyi1_target_score
    yuyi2_fencha = (x['行内培训得分'] - yuyi2_target_score) / yuyi2_target_score
    guanlian_weidu_fencha = (x['专业能力得分'] - guanlian_weidu_target_score) / guanlian_weidu_target_score
    guanlian_yuyi1_fencha = (x['基础学历得分'] - guanlian_yuyi1_target_score) / guanlian_yuyi1_target_score

    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -0.2:
            return '稍有差距'
        elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
            return '仍有差距'
        else:
            return '差距较远'
    
    def lang_guanlian(guanlian_fencha):
        if guanlian_fencha > 0.2:
            return '全面领先'
        elif guanlian_fencha > 0 and guanlian_fencha <= 0.2:
            return '有所领先'
    
    def lang_yuyi1(yuyi1_fencha, guanlian1_fencha):
        if guanlian1_fencha >= 0:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '保持学历提升的热情，胜利就在前方'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '继续保持学习的热情，我们能看到您的学历提升努力'
            else:
                return '保持对知识的好奇，您的学历提升努力不会白费'
        else:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '关注学历提升，迈向知识的下一步台阶'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '多关注学历提升，现在就是正当年'
            else:
                return '着重关注学历提升，用知识重燃热血和激情'
    
    def lang_yuyi2(yuyi2_fencha):
        if yuyi2_fencha >= 0:
            return '无需关注'
        elif yuyi2_fencha < 0 and yuyi2_fencha >= -0.2:
            return '再提高一些行内培训参与的积极性，保持求知热情'
        elif yuyi2_fencha < -0.2 and yuyi2_fencha >= -0.4:
            return '持续提高行内培训的参与积极性，多留下您奋斗的背影'
        else:
            return '多多参与行内培训，期待您的出现'

    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    else:
        if yuyi1_fencha < 0 and yuyi2_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang4 = lang_yuyi2(yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod3'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, weidu_name=weidu_name, 
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang3 = lang_yuyi2(yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
        elif yuyi1_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name, 
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
        elif yuyi2_fencha < 0:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_yuyi2(yuyi2_fencha)
            advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    return advise



#行外经历维度
def cal_hangwaijingli_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '行外经历'
    guanlian_weidu = '工作历程'
    guanlian_yuyi1 = '行内经验'
    guanlian_yuyi2 = '行内活动'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['行外经历得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['其他经验得分'].values[0]
    yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['其他活动得分'].values[0]
    guanlian_weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['工作历程得分'].values[0]
    guanlian_yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['行内经验得分'].values[0]
    guanlian_yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['行内活动得分'].values[0]
    weidu_fencha =  (x['行外经历得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['其他经验得分'] - yuyi1_target_score) / yuyi1_target_score
    yuyi2_fencha = (x['其他活动得分'] - yuyi2_target_score) / yuyi2_target_score
    guanlian_weidu_fencha = (x['工作历程得分'] - guanlian_weidu_target_score) / guanlian_weidu_target_score
    guanlian_yuyi1_fencha = (x['行内经验得分'] - guanlian_yuyi1_target_score) / guanlian_yuyi1_target_score
    guanlian_yuyi2_fencha = (x['行内活动得分'] - guanlian_yuyi2_target_score) / guanlian_yuyi2_target_score

    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -0.2:
            return '稍有差距'
        elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
            return '仍有差距'
        else:
            return '差距较远'
    
    def lang_guanlian(guanlian_fencha):
        if guanlian_fencha > 0.2:
            return '全面领先'
        elif guanlian_fencha > 0 and guanlian_fencha <= 0.2:
            return '有所领先'
    
    def lang_yuyi1(yuyi1_fencha, guanlian1_fencha):
        if guanlian1_fencha >= 0:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '保持一贯的工作热情，继续丰富行内工作经验'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '保持专注，持续积累行内经验，机会和成功会随之而来'
            else:
                return'坚持信念，逐步积累行内经验，追求下一个事业高峰'
        else:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '再加把劲，继续丰富行内经验'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '撸起袖子加油干，持续积累行内经验'
            else:
                return '千里之行始于足下，逐步积累行内经验，为自己铺就成功的道路'
    
    def lang_yuyi2(yuyi2_fencha, guanlian2_fencha):
        if guanlian2_fencha >= 0:
            if yuyi2_fencha >= 0:
                return '无需关注'
            elif yuyi2_fencha < 0 and yuyi2_fencha >= -0.2:
                return '稍稍关注行外其他活动，继续展现您在行内活动中的热情与活力'
            elif yuyi2_fencha < -0.2 and yuyi2_fencha >= -0.4:
                return '增加对行外其他活动的关注，用您在行内活动的热情感染更多人'
            else:
                return '多多关注行外其他活动，将您在行内的快乐轨迹再延伸'
        else:
            if yuyi2_fencha >= 0:
                return '无需关注'
            elif yuyi2_fencha < 0 and yuyi2_fencha >= -0.2:
                return '保持参加行外其他各项活动的热情'
            elif yuyi2_fencha < -0.2 and yuyi2_fencha >= -0.4:
                return '持续积极参与行外其他各项活动'
            else:
                return '多参与行外其他各项活动，期待您释放的光彩'

    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    else:
        if yuyi1_fencha < 0 and yuyi2_fencha < 0:
            if guanlian_yuyi1_fencha >= 0 and guanlian_yuyi2_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_guanlian(guanlian_yuyi2_fencha)
                lang4 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang5 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod4'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, yuyi5=lang5, weidu_name=weidu_name, 
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1, guanlian_yuyi2=guanlian_yuyi2)
            elif guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang4 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod3'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            elif guanlian_yuyi2_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi2_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang4 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod3'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi2)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang3 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
        elif yuyi1_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
        elif yuyi2_fencha < 0:
            if guanlian_yuyi2_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi2_fencha)
                lang3 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi2)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    return advise



#工作成长维度
def cal_gongzuochengzhang_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '工作成长'
    guanlian_weidu = '工作情况'
    guanlian_yuyi1 = '当年表现'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['工作成长得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['持续表现得分'].values[0]
    guanlian_weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['工作情况得分'].values[0]
    guanlian_yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['当年表现得分'].values[0]
    weidu_fencha =  (x['工作成长得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['持续表现得分'] - yuyi1_target_score) / yuyi1_target_score
    guanlian_weidu_fencha = (x['工作情况得分'] - guanlian_weidu_target_score) / guanlian_weidu_target_score
    guanlian_yuyi1_fencha = (x['当年表现得分'] - guanlian_yuyi1_target_score) / guanlian_yuyi1_target_score

    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -0.2:
            return '稍有差距'
        elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
            return '仍有差距'
        else:
            return '差距较远'
    
    def lang_guanlian(guanlian_fencha):
        if guanlian_fencha > 0.2:
            return '全面领先'
        elif guanlian_fencha > 0 and guanlian_fencha <= 0.2:
            return '有所领先'
    
    def lang_yuyi1(yuyi1_fencha, guanlian1_fencha):
        if guanlian1_fencha >= 0:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '保持当前的工作表现，继续发光发热'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '始终保持当前优秀的工作表现，未来再接再厉'
            else:
                return '当前的工作表现展现出您的实力，未来一定要继续保持'
        else:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '再提升些工作表现，您已经开始展露锋芒'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '多加强工作中的表现，并持之以恒'
            else:
                return '着重开始提高工作表现，您的潜力不可估量'

    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    else:
        if guanlian_yuyi1_fencha >= 0:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_guanlian(guanlian_yuyi1_fencha)
            lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
            advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name,
                                                     guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
        else:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
            advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)

    return advise
                


                
#专业能力维度
def cal_zhuanyenengli_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '专业能力'
    guanlian_weidu = '学习提升'
    guanlian_yuyi1 = '学历提升'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['专业能力得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['基础学历得分'].values[0]
    yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['专业技术得分'].values[0]
    guanlian_weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['学习提升得分'].values[0]
    guanlian_yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['学历提升得分'].values[0]
    weidu_fencha =  (x['专业能力得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['基础学历得分'] - yuyi1_target_score) / yuyi1_target_score
    yuyi2_fencha = (x['专业技术得分'] - yuyi2_target_score) / yuyi2_target_score
    guanlian_weidu_fencha = (x['学习提升得分'] - guanlian_weidu_target_score) / guanlian_weidu_target_score
    guanlian_yuyi1_fencha = (x['学历提升得分'] - guanlian_yuyi1_target_score) / guanlian_yuyi1_target_score

    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -0.2:
            return '稍有差距'
        elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
            return '仍有差距'
        else:
            return '差距较远'
    
    def lang_guanlian(guanlian_fencha):
        if guanlian_fencha > 0.2:
            return '全面领先'
        elif guanlian_fencha > 0 and guanlian_fencha <= 0.2:
            return '有所领先'
    
    def lang_yuyi1(yuyi1_fencha, guanlian1_fencha):
        if guanlian1_fencha >= 0:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '保持学历提升的热情，胜利就在前方'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '继续保持学习的热情，我们能看到您的学历提升努力'
            else:
                return '保持对知识的好奇，您的学历提升努力不会白费'
        else:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '关注学历提升，迈向知识的下一步台阶'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '多关注学历提升，现在就是正当年'
            else:
                return '着重关注学历提升，用知识重燃热血和激情'
    
    def lang_yuyi2(yuyi2_fencha):
        if yuyi2_fencha >= 0:
            return '无需关注'
        elif yuyi2_fencha < 0 and yuyi2_fencha >= -0.2:
            return '再提高些专业技术能力，争当六边形战士'
        elif yuyi2_fencha < -0.2 and yuyi2_fencha >= -0.4:
            return '多提高对专业技术能力的关注，丰满自己专业的羽翼'
        else:
            return '着重提高专业技术能力，开始打造自己的专业护城河'

    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    else:
        if yuyi1_fencha < 0 and yuyi2_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang4 = lang_yuyi2(yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod3'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang3 = lang_yuyi2(yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
        elif yuyi1_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
        elif yuyi2_fencha < 0:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_yuyi2(yuyi2_fencha)
            advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    return advise
                
                


#违规惩处维度
def cal_weiguichengchu_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '违规惩处'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['违规惩处扣分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['违规行为扣分'].values[0]
    yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['纪律处分扣分'].values[0]

    weidu_fencha = -(x['违规惩处扣分'] - weidu_target_score)
    yuyi1_fencha = -(x['违规行为扣分'] - yuyi1_target_score)
    yuyi2_fencha = -(x['纪律处分扣分'] - yuyi2_target_score)


    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -20:
            return '稍有差距'
        elif weidu_fencha < -20 and weidu_fencha >= -40:
            return '仍有差距'
        else:
            return '差距较远'

    
    def lang_yuyi1(yuyi1_fencha):
        if yuyi1_fencha >= 0:
            return '无需关注'
        elif yuyi1_fencha < 0 and yuyi1_fencha >= -20:
            return '保持合规意识，继续保持遵规守法行为'
        elif yuyi1_fencha < -20 and yuyi1_fencha >= -40:
            return '保持合规意识，努力保持遵规守法行为'
        else:
            return '保持合规意识，未来可以做的更好'
        
    def lang_yuyi2(yuyi2_fencha):
        if yuyi2_fencha >= 0:
            return '无需关注'
        elif yuyi2_fencha < 0 and yuyi2_fencha >= -20:
            return '保持法律意识，继续做守法的好市民好员工'
        elif yuyi2_fencha < -20 and yuyi2_fencha >= -40:
            return '保持法律意识，努力保持守法行为'
        else:
            return '保持法律意识，未来可以做的更好'


    advise = ''
    if weidu_fencha >= 0:
        lang1 = '做的很好'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    else:
        if yuyi1_fencha < 0 and yuyi2_fencha < 0:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_yuyi1(yuyi1_fencha)
            lang3 = lang_yuyi2(yuyi2_fencha)
            advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
        elif yuyi1_fencha < 0:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_yuyi1(yuyi1_fencha)
            advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
        elif yuyi2_fencha < 0:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_yuyi2(yuyi2_fencha)
            advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)

    return advise
                


                
#荣誉表彰维度
def cal_rongyubiaozhang_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '荣誉表彰'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['荣誉表彰得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['荣誉情况得分'].values[0]

    weidu_fencha = (x['荣誉表彰得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['荣誉情况得分'] - yuyi1_target_score) / yuyi1_target_score


    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -0.2:
            return '稍有差距'
        elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
            return '仍有差距'
        else:
            return '差距较远'

    
    def lang_yuyi1(yuyi1_fencha):
        if yuyi1_fencha >= 0:
            return '无需关注'
        elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
            return '再积极些争取各项荣誉，真正树立模范形象'
        elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
            return '持续争取行内外各项荣誉表彰，争当行内模范'
        else:
            return '提高荣誉表彰争取的积极性，获得属于自己的荣誉'


    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    else:
        lang1 = lang_weidu(weidu_fencha)
        lang2 = lang_yuyi1(yuyi1_fencha)
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)

    return advise
                


                

 #工作情况维度
def cal_gongzuoqingkuang_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '工作情况'
    guanlian_weidu = '工作成长'
    guanlian_yuyi1 = '持续表现'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['工作情况得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['当年表现得分'].values[0]
    yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['当年行为得分'].values[0]
    guanlian_weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['工作成长得分'].values[0]
    guanlian_yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['持续表现得分'].values[0]
    weidu_fencha =  (x['工作情况得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['当年表现得分'] - yuyi1_target_score) / yuyi1_target_score
    yuyi2_fencha = (x['当年行为得分'] - yuyi2_target_score) / yuyi2_target_score
    guanlian_weidu_fencha = (x['工作成长得分'] - guanlian_weidu_target_score) / guanlian_weidu_target_score
    guanlian_yuyi1_fencha = (x['持续表现得分'] - guanlian_yuyi1_target_score) / guanlian_yuyi1_target_score

    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -0.2:
            return '稍有差距'
        elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
            return '仍有差距'
        else:
            return '差距较远'
    
    def lang_guanlian(guanlian_fencha):
        if guanlian_fencha > 0.2:
            return '全面领先'
        elif guanlian_fencha > 0 and guanlian_fencha <= 0.2:
            return '有所领先'
    
    def lang_yuyi1(yuyi1_fencha, guanlian1_fencha):
        if guanlian1_fencha >= 0:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '保持一贯的卓越工作表现，今年继续发光发热'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '始终保持优秀的工作表现，今年再接再厉'
            else:
                return '展现出您应有的实力，今年加油提升工作表现'
        else:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '继续提升当年表现，曙光快要出现'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '持续关注当年表现，让事业更进一步'
            else:
                return '着重关注当年表现，脚踏实地做出成就'
    
    def lang_yuyi2(yuyi2_fencha):
        if yuyi2_fencha >= 0:
            return '无需关注'
        elif yuyi2_fencha < 0 and yuyi2_fencha >= -0.2:
            return '出勤再守时些，日常的工具使用再积极些'
        elif yuyi2_fencha < -0.2 and yuyi2_fencha >= -0.4:
            return '出勤情况还需加强，日常的工具使用还要更积极'
        else:
            return '格外关注出勤表现和日常工具使用情况'

    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    else:
        if yuyi1_fencha < 0 and yuyi2_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang4 = lang_yuyi2(yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod3'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang3 = lang_yuyi2(yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
        elif yuyi1_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
        elif yuyi2_fencha < 0:
            lang1 = lang_weidu(weidu_fencha)
            lang2 = lang_yuyi2(yuyi2_fencha)
            advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    return advise               
                



#工作历程维度
def cal_gongzuolicheng_advise(x, df_yuyi_mean, xulie,lvl):
    if lvl == None or lvl == '' or lvl == '未知':
        return ''
    weidu_name = '工作历程'
    guanlian_weidu = '行外经历'
    guanlian_yuyi1 = '其他经验'
    guanlian_yuyi2 = '其他活动'
    weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['工作历程得分'].values[0]
    yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['行内经验得分'].values[0]
    yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['行内活动得分'].values[0]
    guanlian_weidu_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['行外经历得分'].values[0]
    guanlian_yuyi1_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['其他经验得分'].values[0]
    guanlian_yuyi2_target_score = df_yuyi_mean[(df_yuyi_mean['二级序列'] == xulie) & (df_yuyi_mean['员工积分序列等级'] == lvl)]['其他活动得分'].values[0]
    weidu_fencha =  (x['工作历程得分'] - weidu_target_score) / weidu_target_score
    yuyi1_fencha = (x['行内经验得分'] - yuyi1_target_score) / yuyi1_target_score
    yuyi2_fencha = (x['行内活动得分'] - yuyi2_target_score) / yuyi2_target_score
    guanlian_weidu_fencha = (x['行外经历得分'] - guanlian_weidu_target_score) / guanlian_weidu_target_score
    guanlian_yuyi1_fencha = (x['其他经验得分'] - guanlian_yuyi1_target_score) / guanlian_yuyi1_target_score
    guanlian_yuyi2_fencha = (x['其他活动得分'] - guanlian_yuyi2_target_score) / guanlian_yuyi2_target_score

    def lang_weidu(weidu_fencha):
        if weidu_fencha < 0 and weidu_fencha >= -0.2:
            return '稍有差距'
        elif weidu_fencha < -0.2 and weidu_fencha >= -0.4:
            return '仍有差距'
        else:
            return '差距较远'
    
    def lang_guanlian(guanlian_fencha):
        if guanlian_fencha > 0.2:
            return '全面领先'
        elif guanlian_fencha > 0 and guanlian_fencha <= 0.2:
            return '有所领先'
    
    def lang_yuyi1(yuyi1_fencha, guanlian1_fencha):
        if guanlian1_fencha >= 0:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '保持一贯的工作热情，继续丰富行内工作经验'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '保持专注，持续积累行内经验，机会和成功会随之而来'
            else:
                return'坚持信念，逐步积累行内经验，追求下一个事业高峰'
        else:
            if yuyi1_fencha >= 0:
                return '无需关注'
            elif yuyi1_fencha < 0 and yuyi1_fencha >= -0.2:
                return '再加把劲，继续丰富行内经验'
            elif yuyi1_fencha < -0.2 and yuyi1_fencha >= -0.4:
                return '撸起袖子加油干，持续积累行内经验'
            else:
                return '千里之行始于足下，逐步积累行内经验，为自己铺就成功的道路'
    
    def lang_yuyi2(yuyi2_fencha, guanlian2_fencha):
        if guanlian2_fencha >= 0:
            if yuyi2_fencha >= 0:
                return '无需关注'
            elif yuyi2_fencha < 0 and yuyi2_fencha >= -0.2:
                return '稍稍关注行内活动动态，继续展现您在行外其他活动中的热情与活力'
            elif yuyi2_fencha < -0.2 and yuyi2_fencha >= -0.4:
                return '增加对行内活动动态的关注，用您在行外其他活动的热情感染更多人'
            else:
                return '多多关注行内活动动态，将您在行外其他活动的快乐轨迹再延伸'
        else:
            if yuyi2_fencha >= 0:
                return '无需关注'
            elif yuyi2_fencha < 0 and yuyi2_fencha >= -0.2:
                return '保持参加行内各项活动的热情'
            elif yuyi2_fencha < -0.2 and yuyi2_fencha >= -0.4:
                return '持续积极参与行内各项活动'
            else:
                return '多参与行内各项活动，期待您的光彩'

    advise = ''
    if weidu_fencha >= 0.2:
        lang1 = '全面领先'
        lang2 = '重点关注其他得分差距较大的维度'
        advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    elif weidu_fencha >=0 and weidu_fencha < 0.2:
        lang1 = '有所领先'
        lang2 = '优先关注其他得分差距较大的维度'
        lang3 = '对本维度得分情况继续保持关注'
        advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
    else:
        if yuyi1_fencha < 0 and yuyi2_fencha < 0:
            if guanlian_yuyi1_fencha >= 0 and guanlian_yuyi2_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_guanlian(guanlian_yuyi2_fencha)
                lang4 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang5 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod4'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, yuyi5=lang5, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1, guanlian_yuyi2=guanlian_yuyi2)
            elif guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang4 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod3'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            elif guanlian_yuyi2_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi2_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang4 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod3'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, yuyi4=lang4, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi2)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                lang3 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod2'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name)
        elif yuyi1_fencha < 0:
            if guanlian_yuyi1_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi1_fencha)
                lang3 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi1)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi1(yuyi1_fencha, guanlian_yuyi1_fencha)
                advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
        elif yuyi2_fencha < 0:
            if guanlian_yuyi2_fencha >= 0:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_guanlian(guanlian_yuyi2_fencha)
                lang3 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod5'].format(yuyi1=lang1, yuyi2=lang2, yuyi3=lang3, weidu_name=weidu_name,
                                                         guanlian_weidu=guanlian_weidu, guanlian_yuyi1=guanlian_yuyi2)
            else:
                lang1 = lang_weidu(weidu_fencha)
                lang2 = lang_yuyi2(yuyi2_fencha, guanlian_yuyi2_fencha)
                advise = YUYI_MODELS['yuyi_mod1'].format(yuyi1=lang1, yuyi2=lang2, weidu_name=weidu_name)
    return advise




                


