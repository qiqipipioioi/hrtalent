'''
能力评测得分
'''
#!/usr/bin/env python
# coding: utf-8

import pandas as pd


def cal_zhpc_score(df_nengli, df_xingge, df_base):
    #能力评测得分
    df_nengli['base_zhnl_score'] = df_nengli['totalscore'].astype(float) / 8 * 100
    df_nengli = df_nengli[['a0188', 'base_zhnl_score']].groupby('a0188').max()

    #性格评测得分
    df_xingge['base_xgpc_score'] = df_xingge['dominance'].astype(int) + df_xingge['compliance'].astype(int) + df_xingge['influence'].astype(int) + df_xingge['steadiness'].astype(int)
    df_xingge = df_xingge[['a0188', 'base_xgpc_score']].groupby('a0188').max()


    df_result = pd.merge(df_base[['a0188']], df_nengli, on='a0188', how='left')
    df_result = pd.merge(df_result, df_xingge, on='a0188', how='left')
    df_result.fillna(0, inplace=True)

    df_result = df_result[['a0188', 'base_zhnl_score', 'base_xgpc_score']]

    return df_result