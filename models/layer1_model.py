'''
该模型为数据源表
涂迅
2023/6/21
'''
from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

# 创建一个基类
Base = declarative_base()



class BaseInfo(Base):
    #基本信息表
    __tablename__ = 'baseInfo'
    uid = Column(Integer, primary_key=True, autoincrement=True)    #主键
    user_id = Column(String(10), index=True)                       #工号
    name = Column(String(10), index=True)                          #姓名
    id_no = Column(String(18))                                     #身份证号
    lv1_org = Column(String(20))                                   #一级组织
    lv2_org = Column(String(20))                                   #二级组织
    center = Column(String(20))                                    #中心
    position = Column(String(20))                                  #职位
    duty = Column(String(20))                                      #职务
    emp_type = Column(String(20))                                  #人员类别
    emp_status = Column(String(20))                                #人员状态
    join_time = Column(DateTime)                                   #入行时间
    join_part_time = Column(DateTime)                              #入本机构时间
    part_working_years = Column(Float)                             #本机构工作年限
    position_time = Column(DateTime)                               #任现岗位时间
    emp_lvl = Column(String(20))                                   #行员等级
    highest_edu = Column(String(20))                               #最高学历
    tech_lvl = Column(String(20))                                  #聘任职业技术等级


class WorkingExperience(Base):
    #工作经历子集表
    __tablename__ = 'workingExperience'
    uid = Column(Integer, primary_key=True, autoincrement=True)    #主键
    user_id = Column(String(10), index=True)                       #工号
    name = Column(String(10), index=True)                          #姓名  
    start_time = Column(DateTime)                                  #开始时间
    end_time = Column(DateTime)                                    #结束时间
    company = Column(String(50))                                   #所在单位
    department = Column(String(20))                                #所在部门
    position = Column(String(20))                                  #职位
    professional_sequence = Column(String(20))                     #专业序列
    working_years = Column(Float)                                  #任岗时间
    pro_seq_years = Column(Float)                                  #专业序列折算年限

    def __repr__(self):
        return f"<WorkingExperience(uid='{self.uid}',user_id='{self.user_id}', name={self.name}, \
            start_time={self.start_time}, end_time={self.end_time}, company={self.company}, \
            department={self.department}, position={self.position}, professional_sequence={self.professional_sequence}, \
            working_years={self.working_years}, pro_seq_years={self.pro_seq_years})>"
    

class EmployeeProfessionalSequenceModel(Base):
    #员工专业序列表
    __tablename__ = 'employeeProfessionalSequence'
    uid = Column(Integer, primary_key=True, autoincrement=True)    #主键
    user_id = Column(String(10), index=True)                       #工号
    name = Column(String(10), index=True)                          #姓名
    lvl1_org = Column(String(20), nullable=True)                                   #一级机构
    lvl2_org = Column(String(20), nullable=True)                                   #二级机构
    center = Column(String(20), nullable=True)                                    #中心
    position = Column(String(20), nullable=True)                                  #岗位
    duty = Column(String(20), nullable=True)                                      #职务
    lvl1_professional_sequence = Column(String(20), nullable=True)                #一级序列
    lvl2_professional_sequence = Column(String(20), nullable=True)                #二级序列
    update_datetime = Column(DateTime)                             #更新时间

    def __repr__(self):
        return f"<employee_professional_sequence(uid='{self.uid}',user_id='{self.user_id}', name={self.name}, \
            lv1_org={self.lvl1_org}, lv2_org={self.lvl2_org}, center={self.center}, \
            position={self.position}, duty={self.duty}, lvl1_professional_sequence={self.lvl1_professional_sequence}, \
            lvl2_professional_sequence={self.lvl2_professional_sequence}, update_datetime={self.update_datetime})>"
    


class ProfessionalSequenceLabelWeightsModel(Base):
    # 序列标签权重表
    __tablename__ = 'professionalSequenceLabelWeights'
    uid = Column(Integer, primary_key=True, autoincrement=True)     #主键
    sequence_name = Column(String(50))                              #序列名称
    base_zhnx_weight = Column(Float)                                #在行持续服务年限权重
    base_dqxl_weight = Column(Float)                                #当前序列权重
    base_gqxl_weight = Column(Float)                                #过去序列权重
    base_dqgw_weight = Column(Float)                                #当前岗位权重
    base_gqgw_weight = Column(Float)                                #过去岗位权重
    base_dnhd_weight = Column(Float)                                #当年参与行内活动情况权重
    base_gqhd_weight = Column(Float)                                #过往参与行内活动情况权重
    base_cqqk_weight = Column(Float)                                #出勤情况权重
    base_gjsy_weight = Column(Float)                                #工具使用情况权重
    base_dnpg_weight = Column(Float)                                #当年工作立体评估权重
    base_dnyj_weight = Column(Float)                                #当年工作业绩评价权重
    base_dnry_weight = Column(Float)                                #当年工作荣誉权重
    base_ljry_weight = Column(Float)                                #在行累积工作荣誉权重
    base_dnwg_weight = Column(Float)                                #当年违规行为权重
    base_gqwg_weight = Column(Float)                                #过去违规行为权重
    base_dncf_weight = Column(Float)                                #当年纪律处分权重
    base_gqcf_weight = Column(Float)                                #过去纪律处分权重
    base_qrjy_weight = Column(Float)                                #全日制教育权重
    base_zcqk_weight = Column(Float)                                #职称情况权重
    base_jszg_weight = Column(Float)                                #技术资格情况权重
    base_jxcz_weight = Column(Float)                                #绩效考核成长权重
    base_pgcz_weight = Column(Float)                                #工作立体评估成长权重
    base_gqgz_weight = Column(Float)                                #过去工作经验权重
    base_hwhd_weight = Column(Float)                                #参与行外活动情况权重
    base_qylx_weight = Column(Float)                                #全员轮训情况权重
    base_nxzg_weight = Column(Float)                                #内训师资格权重
    base_xxpt_weight = Column(Float)                                #学习平台得分情况权重
    base_zzjy_weight = Column(Float)                                #在职教育权重
    base_zhnl_weight = Column(Float)                                #综合能力权重
    base_xgpc_weight = Column(Float)                                #性格评测权重
    base_jtcy_weight = Column(Float)                                #家庭成员关系权重
    base_shgx_weight = Column(Float)                                #社会关系权重
    update_datetime = Column(DateTime)                              #更新时间


    def __repr__(self):
        return f"<ProfessionalSequenceLabelWeightsModel(uid='{self.uid}',\
                sequence_name='{self.sequence_name}',base_zhnx_weight={self.base_zhnx_weight}, \
                base_dqxl_weight={self.base_dqxl_weight}, base_gqxl_weight={self.base_gqxl_weight}, \
                base_dqgw_weight={self.base_dqgw_weight}, base_gqgw_weight={self.base_gqgw_weight}, \
                base_dnhd_weight={self.base_dnhd_weight}, base_gqhd_weight={self.base_gqhd_weight}, \
                base_cqqk_weight={self.base_cqqk_weight}, base_gjsy_weight={self.base_gjsy_weight}, \
                base_dnpg_weight={self.base_dnpg_weight}, base_dnyj_weight={self.base_dnyj_weight}, \
                base_dnry_weight={self.base_dnry_weight}, base_ljry_weight={self.base_ljry_weight}, \
                base_dnwg_weight={self.base_dnwg_weight}, base_gqwg_weight={self.base_gqwg_weight}, \
                base_dncf_weight={self.base_dncf_weight}, base_gqcf_weight={self.base_gqcf_weight}, \
                base_qrjy_weight={self.base_qrjy_weight}, base_zcqk_weight={self.base_zcqk_weight}, \
                base_jszg_weight={self.base_jszg_weight}, base_jxcz_weight={self.base_jxcz_weight}, \
                base_pgcz_weight={self.base_pgcz_weight}, base_gqgz_weight={self.base_gqgz_weight}, \
                base_hwhd_weight={self.base_hwhd_weight}, base_qylx_weight={self.base_qylx_weight}, \
                base_nxzg_weight={self.base_nxzg_weight}, base_xxpt_weight={self.base_xxpt_weight}, \
                base_zzjy_weight={self.base_zzjy_weight}, base_zhnl_weight={self.base_zhnl_weight}, \
                base_xgpc_weight={self.base_xgpc_weight}, base_jtcy_weight={self.base_jtcy_weight}, \
                base_shgx_weight={self.base_shgx_weight}, update_datetime={self.update_datetime})>"
    

