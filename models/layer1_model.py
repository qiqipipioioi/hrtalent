'''
该模型为数据源表
涂迅
2023/6/21
'''
from sqlalchemy import Column, Integer, String, DateTime, Float, Numeric, LargeBinary
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
    

class AnnualExaminationSubset(Base):
    # 年度考核子集
    __tablename__ = 'annualExaminationSubset'
    name = Column(Integer,nullable=False)                               # 姓名
    order = Column(String(20),nullable=True)                            # 格次
    score = Column(Numeric(19,2),nullable=True)                         # 分数
    assessment_category = Column(String(20),nullable=True)              #考核类别
    assessment_date = Column(String(20),nullable=True)                  #考核时间

    def __repr__(self):
        return f"<annualExaminationSubset(name='{self.name}', \
                order='{self.order},score='{self.score}', \
                assessment_category='{self.assessment_category}', \
                assessment_data='{self.assessment_date}')>"


class MonthlyResult(Base):
    # 月结果
    __tablename__ = 'monthlyResult'
    name = Column(Integer,nullable=False)                               # 姓名
    joined_date = Column(DateTime(6),nullable=True)                     # 入职日期
    resignation_time = Column(DateTime(6),nullable=True)                # 离职时间
    absent_freq = Column(Integer,nullable=True)                         # 未打卡旷工次数
    absent_days = Column(Numeric(10,2),nullable=True)                   # 未打卡旷工天数
    actual_attend_days = Column(Numeric(19,2),nullable=True)            # 实际出勤天数
    audit_time = Column(DateTime,nullable=True)                         # 审核时间
    reviewer = Column(String(100),nullable=True)                        # 审核人
    signiture_monthly_result = Column(LargeBinary,nullable=True)        # 月结果签字
    confirm_time = Column(DateTime,nullable=True)                       # 确认时间
    create_time = Column(DateTime(6),nullable=True)                     # 创建时间
    early_count = Column(Integer,nullable=True)                         # 早退次数
    early_min = Column(Integer,nullable=True)                           # 早退分钟数
    year_month = Column(String(6),nullable=True)                        # 年月
    is_confirm = Column(Integer,nullable=True)                          # 是否确认
    is_fullwork = Column(Integer,nullable=True)                         # 是否全勤
    issue = Column(Integer,nullable=True)                               # 是否发布
    attend_days = Column(Numeric(19,2),nullable=True)                   # 出勤天数
    month_dept_name = Column(String(60),nullable=True)                  # 本月部门名称
    month_dept_code = Column(String(60),nullable=True)                  # 本月部门编码
    month_result_id = Column(Integer,nullable=False,primary_key=True)   # 月结果ID
    birth_control_leave = Column(String(20),nullable=True)              # 节育假天数
    late_count = Column(Integer,nullable=True)                          # 迟到次数
    late_min = Column(Integer,nullable=True)                            # 迟到分钟数
    leakage_card = Column(Integer,nullable=True)                        # 漏刷卡次数
    leave_count = Column(Integer,nullable=True)                         # 事假次数
    sick_leave_count = Column(Integer,nullable=True)                    # 病假次数
    injury_leave_count = Column(Integer,nullable=True)                  # 工伤假次数
    maternity_leave_count = Column(Integer,nullable=True)               # 产假次数
    nursing_leave_count = Column(Integer,nullable=True)                 # 护理假次数
    breastfeed_leave_count = Column(Integer,nullable=True)              # 哺乳假次数
    maternal_examine_leave_count = Column(Integer,nullable=True)        # 产检假次数
    prenatal_leave_count = Column(Integer,nullable=True)                # 产前假次数
    home_leave_count = Column(Integer,nullable=True)                    # 探亲假次数
    marriage_leave_count = Column(Integer,nullable=True)                # 婚假次数
    bereavement_leave_count = Column(Integer,nullable=True)             # 丧假次数
    compensatory_leave_count = Column(Integer,nullable=True)            # 调休次数
    annual_leave_count = Column(Integer,nullable=True)                  # 年休假次数
    train_leave_count = Column(Integer,nullable=True)                   # 培训加次数
    secondments_leave_count = Column(Integer,nullable=True)             # 借调次数
    abortion_leave_count = Column(Integer,nullable=True)                # 流产假次数
    leave_days = Column(Numeric(19,2),nullable=True)                    # 事假天数
    sick_leave_days = Column(Numeric(19,2),nullable=True)               # 病假天数
    injury_leave_days = Column(Numeric(19,2),nullable=True)             # 工伤假天数
    maternity_leave_days = Column(Numeric(19,2),nullable=True)          # 产假天数
    nursing_leave_days = Column(Numeric(19,2),nullable=True)            # 护理假天数
    breastfeed_leave_days = Column(Numeric(19,2),nullable=True)         # 哺乳假天数
    maternal_examin_leave_days = Column(Numeric(19,2),nullable=True)    # 产检假天数
    home_leave_days = Column(Numeric(19,2),nullable=True)               # 探亲假天数
    official_bussiness_leave = Column(Numeric(19,2),nullable=True)      # 公出
    marriage_leave_days = Column(Numeric(19,2),nullable=True)           # 婚假天数
    bereavement_leave_days = Column(Numeric(19,2),nullable=True)        # 丧假天数
    compensatory_leave_days = Column(Numeric(19,2),nullable=True)       # 调休天数
    annual_leave_days = Column(Numeric(19,2),nullable=True)             # 年休假天数
    train_leave_days = Column(Numeric(19,2),nullable=True)              # 培训假天数
    secondments_leave_days = Column(Numeric(19,2),nullable=True)        # 借调天数
    minor_maternity_leave_days = Column(Numeric(19,2),nullable=True)    # 小产假天数
    leave_time_sum = Column(Numeric(19,2),nullable=True)                # 总请假时数
    lack_check = Column(Integer,nullable=True)                          # 缺卡次数
    month_day = Column(Integer,nullable=True)                           # 本月天数
    notpost_day = Column(Numeric(19,2),nullable=True)                   # 未到岗天数
    out_count = Column(Integer,nullable=True)                           # 外出次数
    business_count = Column(Integer,nullable=True)                      # 出差次数
    out_time = Column(Numeric(19,2),nullable=True)                      # 外出时数
    out_days = Column(Numeric(19,2),nullable=True)                      # 外出天数
    over_count = Column(Integer,nullable=True)                          # 平时加班次数
    over_count_weekend = Column(Integer,nullable=True)                  # 周末加班次数
    over_count_legal = Column(Integer, nullable=True)                   # 法定加班次数
    over_time_common = Column(Numeric(19,2),nullable=True)              # 平时加班时数
    over_time_weekend = Column(Numeric(19,2),nullable=True)             # 周末加班时数
    over_time_legal = Column(Numeric(19,2),nullable=True)               # 法定加班时数
    end_time = Column(Numeric(19,2),nullable=True)                      # 结束时间
    over_time_sum = Column(Numeric(19,2),nullable=True)                 # 总加班天数
    shift_count = Column(Integer,nullable=True)                         # 排班天数
    should_days = Column(Numeric(19,2),nullable=True)                   # 应出勤天数
    signed = Column(String(10),nullable=True)                           # 审批标记
    work_days = Column(Numeric(10,2),nullable=True)                     # 工作日天数

    def __repr__(self):
        return f"<MonthlyResult(name='{self.name}', joined_date='{self.joined_date}', resignation_time='{self.resignation_time}', " \
               f"absent_freq='{self.absent_freq}', absent_days='{self.absent_days}', actual_attend_days='{self.actual_attend_days}', " \
               f"audit_time='{self.audit_time}', reviewer='{self.reviewer}', signiture_monthly_result='{self.signiture_monthly_result}', " \
               f"confirm_time='{self.confirm_time}', create_time='{self.create_time}', early_count='{self.early_count}', " \
               f"early_min='{self.early_min}', year_month='{self.year_month}', is_confirm='{self.is_confirm}', is_fullwork='{self.is_fullwork}', " \
               f"issue='{self.issue}', attend_days='{self.attend_days}', month_dept_name='{self.month_dept_name}', month_dept_code='{self.month_dept_code}', " \
               f"month_result_id='{self.month_result_id}', birth_control_leave='{self.birth_control_leave}', late_count='{self.late_count}', " \
               f"late_min='{self.late_min}', leakage_card='{self.leakage_card}', leave_count='{self.leave_count}', sick_leave_count='{self.sick_leave_count}', " \
               f"injury_leave_count='{self.injury_leave_count}', maternity_leave_count='{self.maternity_leave_count}', nursing_leave_count='{self.nursing_leave_count}', " \
               f"breastfeed_leave_count='{self.breastfeed_leave_count}', maternal_examine_leave_count='{self.maternal_examine_leave_count}', " \
               f"prenatal_leave_count='{self.prenatal_leave_count}', home_leave_count='{self.home_leave_count}', marriage_leave_count='{self.marriage_leave_count}', " \
               f"bereavement_leave_count='{self.bereavement_leave_count}', compensatory_leave_count='{self.compensatory_leave_count}', " \
               f"annual_leave_count='{self.annual_leave_count}', train_leave_count='{self.train_leave_count}', " \
               f"secondments_leave_count='{self.secondments_leave_count}', abortion_leave_count='{self.abortion_leave_count}', leave_days='{self.leave_days}', " \
               f"sick_leave_days='{self.sick_leave_days}', injury_leave_days='{self.injury_leave_days}', maternity_leave_days='{self.maternity_leave_days}', " \
               f"nursing_leave_days='{self.nursing_leave_days}', breastfeed_leave_days='{self.breastfeed_leave_days}', " \
               f"maternal_examin_leave_days='{self.maternal_examin_leave_days}', home_leave_days='{self.home_leave_days}', " \
               f"official_bussiness_leave='{self.official_bussiness_leave}', marriage_leave_days='{self.marriage_leave_days}', " \
               f"bereavement_leave_days='{self.bereavement_leave_days}', compensatory_leave_days='{self.compensatory_leave_days}', " \
               f"annual_leave_days='{self.annual_leave_days}', train_leave_days='{self.train_leave_days}', " \
               f"secondments_leave_days='{self.secondments_leave_days}', minor_maternity_leave_days='{self.minor_maternity_leave_days}', " \
               f"leave_time_sum='{self.leave_time_sum}', lack_check='{self.lack_check}', month_day='{self.month_day}', " \
               f"notpost_day='{self.notpost_day}', out_count='{self.out_count}', business_count='{self.business_count}', " \
               f"out_time='{self.out_time}', out_days='{self.out_days}', over_count='{self.over_count}', " \
               f"over_count_weekend='{self.over_count_weekend}', over_count_legal='{self.over_count_legal}', " \
               f"over_time_common='{self.over_time_common}', over_time_weekend='{self.over_time_weekend}', " \
               f"over_time_legal='{self.over_time_legal}', end_time='{self.end_time}', over_time_sum='{self.over_time_sum}', " \
               f"shift_count='{self.shift_count}', should_days='{self.should_days}', signed='{self.signed}', " \
               f"work_days='{self.work_days}')>"

class RewardSubset(Base):
    # 奖励子集
    __tablename__='rewardSubset'
    name = Column(Integer,nullable=False)                               # 姓名
    reward_category = Column(String(200),nullable=True)                 # 奖励类别
    reward_level = Column(String(20),nullable=True)                     # 奖励及荣誉级别
    reward_filename = Column(String(200),nullable=True)                 # 奖励及荣誉文件名称
    publish_organize = Column(String(200),nullable=True)                # 发文机构
    reward_type = Column(String(10),nullable=True)                      # 奖励类型
    approval_number = Column(String(200),nullable=True)                 # 批准文号
    involve_business = Column(String(120),nullable=True)                # 涉及业务
    other_reward_punish = Column(String(100),nullable=True)             # 其他奖惩
    reward_punish_institution = Column(String(120),nullable=True)       # 奖惩时所在机构
    commend_level = Column(String(20),nullable=True)                    # 表彰家里级别
    commend_category = Column(String(20),nullable=True)                 # 表彰奖励类别
    commend_name = Column(String(20),nullable=True)                     # 表彰奖励名称
    commend_year = Column(String(5),nullable=True)                      # 表彰奖励年度
    authority = Column(String(20),nullable=True)                        # 批准单位
    commend_cancel_time = Column(DateTime,nullable=True)                # 表彰奖励取消时间
    commend_cancel_result = Column(String(1000),nullable=True)          # 表彰奖励取消原因
    occur_time = Column(DateTime,nullable=True)                         # 发生时间
    commend_result = Column(String(1000),nullable=True)                 # 表彰奖励原因
    certificate_annex = Column(String(30),nullable=True)                # 证书附件
    person_status = Column(String(20),nullable=True)                    # 人员状态
    a_id = Column(Integer,nullable=True)                                # 序号
    dj_id = Column(String(20),nullable=True)                            # dj_id
    attachment_id = Column(Integer,nullable=True)                       # 信息变更申请附表id

    def __repr__(self):
        return f"<RewardSubset(name='{self.name}', reward_category='{self.reward_category}', " \
               f"reward_level='{self.reward_level}', reward_filename='{self.reward_filename}', " \
               f"publish_organize='{self.publish_organize}', reward_type='{self.reward_type}', " \
               f"approval_number='{self.approval_number}', involve_business='{self.involve_business}', " \
               f"other_reward_punish='{self.other_reward_punish}', " \
               f"reward_punish_institution='{self.reward_punish_institution}', " \
               f"commend_level='{self.commend_level}', commend_category='{self.commend_category}', " \
               f"commend_name='{self.commend_name}', commend_year='{self.commend_year}', " \
               f"authority='{self.authority}', commend_cancel_time='{self.commend_cancel_time}', " \
               f"commend_cancel_result='{self.commend_cancel_result}', " \
               f"occur_time='{self.occur_time}', commend_result='{self.commend_result}', " \
               f"certificate_annex='{self.certificate_annex}', " \
               f"person_status='{self.person_status}', a_id='{self.a_id}', " \
               f"dj_id='{self.dj_id}', attachment_id='{self.attachment_id}')>"

class PartTimeSubset(Base):
    # 社会兼职子集
    __tablename__='partTimeSubset'
    name = Column(Integer,nullable=False)                               # 姓名
    institution = Column(String(200),nullable=True)                     # 机构
    position = Column(String(120),nullable=True)                        # 职务
    start_time = Column(DateTime,nullable=True)                         # 起始日期
    end_time = Column(DateTime,nullable=True)                           # 终止日期
    serial_number = Column(Integer,nullable=True)                       # 序号
    attachment_id = Column(Integer, nullable=True)                      # 信息变更申请附表id

    def __repr__(self):
        return f"<PartTimeSubset(name='{self.name}', institution='{self.institution}', " \
               f"position='{self.position}', start_time='{self.start_time}', " \
               f"end_time='{self.end_time}', serial_number='{self.serial_number}', " \
               f"attachment_id='{self.attachment_id}')>"

class FamilyMember(Base):
    # 家庭成员
    __tablename__='familyMember'
    name = Column(Integer,nullable=False)                               # 姓名
    politica_status = Column(String(50),nullable=True)                  # 政治面貌
    certificate_number = Column(String(20),nullable=True)               # 证件号码
    member_age = Column(Integer,nullable=True)                          # 成员年龄
    # a86411 = Column(String(20),nullable=True)
    relationship = Column(String(20),nullable=True)                     # 与本人关系
    gender = Column(String(20),nullable=True)                           # 性别
    position = Column(String(200),nullable=True)                        # 职务
    military_service = Column(String(20),nullable=True)                 # 是否服兵役
    location = Column(String(200),nullable=True)                        # 所在地（具体到城市）
    work_unit = Column(String(1000),nullable=True)                      # 工作单位及职务
    phone = Column(String(20),nullable=True)                            # 联系电话
    # a864_cw = Column(String(20),nullable=True)
    # a864id = Column(Integer,nullable=True)
    aid = Column(Integer,nullable=True)                                 # 序号
    birthday = Column(DateTime(6),nullable=True)                        # 出生日期
    attachment_id = Column(Integer, nullable=True)                      # 信息变更申请附表id
    name_1 = Column(String(20),nullable=True)                           # 姓名
    nationality = Column(String(20),nullable=True)                      # 国籍
    id_type = Column(String(20),nullable=True)                          # 证件类型

    def __repr__(self):
        return f"<FamilyMember(name='{self.name}', politica_status='{self.politica_status}', " \
               f"certificate_number='{self.certificate_number}', member_age='{self.member_age}', " \
               f"relationship='{self.relationship}', gender='{self.gender}', " \
               f"position='{self.position}', military_service='{self.military_service}', " \
               f"location='{self.location}', work_unit='{self.work_unit}', " \
               f"phone='{self.phone}', aid='{self.aid}', birthday='{self.birthday}', " \
               f"attachment_id='{self.attachment_id}', name_1='{self.name_1}', " \
               f"nationality='{self.nationality}', id_type='{self.id_type}')>"

class ViolateScoreSet(Base):
    # 违规记分子集
    __tablename__ = 'violateScoreSet'
    name = Column(Integer,nullable=False)                               # 姓名
    occur_time = Column(DateTime,nullable=True)                         # 发生日期
    found_time = Column(DateTime,nullable=True)                         # 发现日期
    deduct_point = Column(String(20),nullable=True)                     # 扣分
    overview = Column(String(500),nullable=True)                        # 违规事件概述
    found_channel = Column(String(100),nullable=True)                   # 发现渠道
    checked_institution = Column(String(200),nullable=True)             # 被检查机构
    detail = Column(String(1000),nullable=True)                         # 违规事件明细概述
    aid = Column(Integer,nullable=True)                                 # 序号
    position = Column(String(60),nullable=True)                         # 员工岗位
    attachment_id = Column(Integer, nullable=True)                      # 信息变更申请附表id

    def __repr__(self):
        return f"<ViolateScoreSet(name='{self.name}', occur_time='{self.occur_time}', " \
               f"found_time='{self.found_time}', deduct_point='{self.deduct_point}', " \
               f"overview='{self.overview}', found_channel='{self.found_channel}', " \
               f"checked_institution='{self.checked_institution}', " \
               f"detail='{self.detail}', aid='{self.aid}', position='{self.position}', " \
               f"attachment_id='{self.attachment_id}')>"

class EducationBackgroundSet(Base):
    # 教育背景子集
    __tablename__='educationBackgroundSet'
    name = Column(Integer,nullable=False)                               # 姓名
    start_time = Column(DateTime(6),nullable=True)                      # 起始时间
    education = Column(String(20),nullable=True)                        # 学历
    school = Column(String(200),nullable=True)                          # 学校
    major_type = Column(String(60),nullable=True)                       # 专业类型
    registration_form = Column(String(100),nullable=True)               # 学历电子注册备案表
    degree = Column(String(20),nullable=True)                           # 学位
    learn_type = Column(String(20),nullable=True)                       # 学习方式
    learn_type_detail = Column(String(20),nullable=True)                # 具体学习形式
    graduate_type = Column(String(20),nullable=True)                    # 毕业类型
    education_type = Column(String(20),nullable=True)                   # 教育类型
    double_degree = Column(Integer,nullable=True)                       # 是否双学位
    school_nature = Column(String(20),nullable=True)                    # 学校性质
    certificate_file = Column(String(100),nullable=True)                # 学历证明文件
    school_type = Column(String(20),nullable=True)                      # 学校类型
    highest_education = Column(String(20),nullable=True)                # 是否最高学历
    attachment = Column(String(30),nullable=True)                       # 证书附件
    is_985_211 = Column(String(5),nullable=True)                        # 985/211院校
    certificate_status = Column(String(30),nullable=True)               # 证书附件
    person_status = Column(String(20),nullable=True)                    # 人员状态
    aid = Column(Integer,nullable=True)                                 # 序号
    end_time = Column(DateTime,nullable=True)                           # 终止时间
    attachment_id = Column(Integer, nullable=True)                      # 信息变更申请附表id
    old_degree = Column(String(50),nullable=True)                       # 学位（旧）
    old_education = Column(String(50),nullable=True)                    # 学历（旧）
    line_depart = Column(String(20),nullable=True)                      # 条线部门
    employee_status = Column(String(20),nullable=True)                  # 员工状态
    major = Column(String(100),nullable=True)                           # 专业

    def __repr__(self):
        return f"<EducationBackgroundSet(name='{self.name}', start_time='{self.start_time}', " \
               f"education='{self.education}', school='{self.school}', major_type='{self.major_type}', " \
               f"registration_form='{self.registration_form}', degree='{self.degree}', learn_type='{self.learn_type}', " \
               f"learn_type_detail='{self.learn_type_detail}', graduate_type='{self.graduate_type}', " \
               f"education_type='{self.education_type}', double_degree='{self.double_degree}', " \
               f"school_nature='{self.school_nature}', certificate_file='{self.certificate_file}', " \
               f"school_type='{self.school_type}', highest_education='{self.highest_education}', " \
               f"attachment='{self.attachment}', is_985_211='{self.is_985_211}', " \
               f"certificate_status='{self.certificate_status}', person_status='{self.person_status}', " \
               f"aid='{self.aid}', end_time='{self.end_time}', attachment_id='{self.attachment_id}', " \
               f"old_degree='{self.old_degree}', old_education='{self.old_education}', " \
               f"line_depart='{self.line_depart}', employee_status='{self.employee_status}', " \
               f"major='{self.major}')>"


class ProfessionalCertificateSet(Base):
    # 职业证书子集
    __tablename__='professionalCertificateSet'
    name = Column(Integer,nullable=False)                               # 姓名
    obtain_time = Column(DateTime(6),nullable=True)                     # 证书获得时间
    certificate_name = Column(String(100),nullable=True)                # 证书名称
    grade = Column(String(20),nullable=True)                            # 资质等级
    effective_date = Column(DateTime,nullable=True)                     # 津贴生效日期
    is_highest = Column(String(20),nullable=True)                       # 是否最高
    vocational_level = Column(String(30),nullable=True)                 # 聘任职业技术等级
    qualification_score = Column(Numeric(19,2),nullable=True)           # 专业序列资质分值
    person_status = Column(String(20),nullable=True)                    # 人员状态
    aid = Column(Integer,nullable=True)                                 # 序号
    category = Column(String(20),nullable=True)                         # 类别
    issue_unit = Column(String(100),nullable=True)                      # 发证单位
    affiliate_sequence = Column(String(50),nullable=True)               # 所属序列

    def __repr__(self):
        return f"<ProfessionalCertificateSet(name='{self.name}', obtain_time='{self.obtain_time}', " \
               f"certificate_name='{self.certificate_name}', grade='{self.grade}', " \
               f"effective_date='{self.effective_date}', is_highest='{self.is_highest}', " \
               f"vocational_level='{self.vocational_level}', " \
               f"qualification_score='{self.qualification_score}', person_status='{self.person_status}', " \
               f"aid='{self.aid}', category='{self.category}', issue_unit='{self.issue_unit}', " \
               f"affiliate_sequence='{self.affiliate_sequence}')>"


