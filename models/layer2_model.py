'''
该模型为加工后的表格
涂迅
2023/6/21
'''
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

# 创建一个基类
Base = declarative_base()


class EmployeeBaseScoreModel(Base):
    # 员工基础标签得分表
    __tablename__ = 'employeeBaseScore'
    uid = Column(Integer, primary_key=True, autoincrement=True)    #主键
    user_id = Column(String(20))                                   #员工号
    lvl1_org = Column(String(20), nullable=True)                   #一级机构
    lvl2_org = Column(String(20), nullable=True)                   #二级机构
    center = Column(String(20), nullable=True)                     #中心
    position = Column(String(20), nullable=True)                   #岗位
    base_zhnx_score = Column(Float)                                #在行持续服务年限得分
    base_dqxl_score = Column(Float)                                #当前序列得分
    base_gqxl_score = Column(Float)                                #过去序列得分
    base_dqgw_score = Column(Float)                                #当前岗位得分
    base_gqgw_score = Column(Float)                                #过去岗位得分
    base_dnhd_score = Column(Float)                                #当年参与行内活动情况得分
    base_gqhd_score = Column(Float)                                #过往参与行内活动情况得分
    base_cqqk_score = Column(Float)                                #出勤情况得分
    base_gjsy_score = Column(Float)                                #工具使用情况得分
    base_dnpg_score = Column(Float)                                #当年工作立体评估得分
    base_dnyj_score = Column(Float)                                #当年工作业绩评价得分
    base_dnry_score = Column(Float)                                #当年工作荣誉得分
    base_ljry_score = Column(Float)                                #在行累积工作荣誉得分
    base_dnwg_score = Column(Float)                                #当年违规行为扣分
    base_gqwg_score = Column(Float)                                #过去违规行为扣分
    base_dncf_score = Column(Float)                                #当年纪律处分扣分
    base_gqcf_score = Column(Float)                                #过去纪律处分扣分
    base_qrjy_score = Column(Float)                                #全日制教育得分
    base_zcqk_score = Column(Float)                                #职称情况得分
    base_jszg_score = Column(Float)                                #技术资格情况得分
    base_jxcz_score = Column(Float)                                #绩效考核成长得分
    base_pgcz_score = Column(Float)                                #工作立体评估成长得分
    base_gqgz_score = Column(Float)                                #过去工作经验得分
    base_hwhd_score = Column(Float)                                #参与行外活动情况得分
    base_qylx_score = Column(Float)                                #全员轮训情况得分
    base_nxzg_score = Column(Float)                                #内训师资格得分
    base_xxpt_score = Column(Float)                                #学习平台得分情况得分
    base_zzjy_score = Column(Float)                                #在职教育得分
    base_zhnl_score = Column(Float)                                #综合能力得分
    base_xgpc_score = Column(Float)                                #性格评测得分
    base_jtcy_score = Column(Float)                                #家庭成员关系得分
    base_shgx_score = Column(Float)                                #社会关系得分
    update_datetime = Column(DateTime)                             #更新时间

    def __repr__(self):
        return f"<EmployeeBaseScoreModel(uid='{self.uid}',user_id='{self.user_id}', \
                lvl1_org={self.lvl1_org}, lvl2_org={self.lvl2_org}, center={self.center}, \
                position={self.position}, base_zhnx_score={self.base_zhnx_score}, \
                base_dqxl_score={self.base_dqxl_score}, base_gqxl_score={self.base_gqxl_score}, \
                base_dqgw_score={self.base_dqgw_score}, base_gqgw_score={self.base_gqgw_score}, \
                base_dnhd_score={self.base_dnhd_score}, base_gqhd_score={self.base_gqhd_score}, \
                base_cqqk_score={self.base_cqqk_score}, base_gjsy_score={self.base_gjsy_score}, \
                base_dnpg_score={self.base_dnpg_score}, base_dnyj_score={self.base_dnyj_score}, \
                base_dnry_score={self.base_dnry_score}, base_ljry_score={self.base_ljry_score}, \
                base_dnwg_score={self.base_dnwg_score}, base_gqwg_score={self.base_gqwg_score}, \
                base_dncf_score={self.base_dncf_score}, base_gqcf_score={self.base_gqcf_score}, \
                base_qrjy_score={self.base_qrjy_score}, base_zcqk_score={self.base_zcqk_score}, \
                base_jszg_score={self.base_jszg_score}, base_jxcz_score={self.base_jxcz_score}, \
                base_pgcz_score={self.base_pgcz_score}, base_gqgz_score={self.base_gqgz_score}, \
                base_hwhd_score={self.base_hwhd_score}, base_qylx_score={self.base_qylx_score}, \
                base_nxzg_score={self.base_nxzg_score}, base_xxpt_score={self.base_xxpt_score}, \
                base_zzjy_score={self.base_zzjy_score}, base_zhnl_score={self.base_zhnl_score}, \
                base_xgpc_score={self.base_xgpc_score}, base_jtcy_score={self.base_jtcy_score}, \
                base_shgx_score={self.base_shgx_score}, update_datetime={self.update_datetime})>"
    