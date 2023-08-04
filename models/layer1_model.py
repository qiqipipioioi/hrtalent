'''
该模型为数据源表
涂迅
2023/6/21
'''
from sqlalchemy import Column, Integer, String, DateTime, Float, DECIMAL, NUMERIC, INTEGER, CHAR, VARCHAR, DATETIME, \
    INT, BINARY, SMALLINT
from sqlalchemy.ext.declarative import declarative_base

# 创建一个基类
Base = declarative_base()


class A01(Base):
    # 基本信息表
    __tablename__ = 'a01'
    a0188 = Column(INTEGER, nullable=False, primary_key=True)  # uid
    a0190 = Column(VARCHAR(20), nullable=True, index=True)  # 员工号
    a0101 = Column(VARCHAR(20), nullable=False, index=True)  # 姓名
    dept_1 = Column(VARCHAR(40), nullable=False)  # 一级机构
    dept_2 = Column(VARCHAR(40), nullable=False)  # 二级机构
    dept_code = Column(VARCHAR(200), nullable=False)  # 中心
    a0141 = Column(DATETIME(8), nullable=False)  # 入行时间
    a01145 = Column(DATETIME(8), nullable=True)  # 任现岗位时间
    a01686 = Column(VARCHAR(20), nullable=True)  # 行员等级
    e0101 = Column(VARCHAR(10), nullable=True)  # 岗位
    a01687 = Column(VARCHAR(20),nullable=True) # 聘任职业技术等级
    a01679 = Column(VARCHAR(20), nullable=True) # 录用类型

    def __repr__(self):
        return f"<A01(a0190='{self.a0190}',a0101='{self.a0101}',dept_1='{self.dept_1}',dept_2='{self.dept_2}',dept_code='{self.dept_code}'" \
               f",a0141='{self.a0141}',a01145='{self.a01145}',a01686='{self.a01686}',e0101='{self.e0101}'," \
               f"a01687='{self.a01686},a01679='{self.a01679}')>"


class A04(Base):
    # 教育背景子集
    __tablename__ = 'a04'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # recordid
    a0447 = Column(VARCHAR(20), nullable=False)  # 教育类型
    endtime = Column(DATETIME(8), nullable=False)  # 终止时间
    a0431 = Column(VARCHAR(200), nullable=False)  # 学校
    a0429 = Column(VARCHAR(20), nullable=False)  # 学历
    a0440 = Column(VARCHAR(100), nullable=True)  # 学位
    fjo = Column(VARCHAR(1000), nullable=True)  # 学历附件
    fjt = Column(VARCHAR(1000), nullable=True)  # 学位附件
    fj3 = Column(VARCHAR(1000), nullable=True)  # 学信网在线验证报告

    def __repr__(self):
        return f"<A04(a0447='{self.a0447}',endtime='{self.endtime}',a0431='{self.a0431}',a0429='{self.a0429}',a0440='{self.a0440}',fjo='{self.fjo}',fjt='{self.fjt}',fj3='{self.fj3}')>"


class A8145(Base):
    # 违规计分子集
    __tablename__ = 'a8145'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False, index=True)  # 员工号，姓名
    a81452 = Column(DATETIME(8), nullable=True)  # 发现日期
    a81453 = Column(VARCHAR(20), nullable=True)  # 扣分

    def __repr__(self):
        return f"<A8145(a0188='{self.a0188}',a81452='{self.a81452}',a81453='{self.a81453}')>"


class A815(Base):
    # 奖励子集
    __tablename__ = 'a815'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False, index=True)  # 员工号，姓名
    a81535 = Column(VARCHAR(5), nullable=True)  # 表彰奖励年月
    a81531 = Column(VARCHAR(20), nullable=True)  # 表彰奖励级别

    def __repr__(self):
        return f"<A815(a0188='{self.a0188}',a81535='{self.a81535}',a81531='{self.a81531}')>"


class A8192(Base):
    # 惩处数据子集
    __tablename__ = 'a8192'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a81923 = Column(VARCHAR(1000), nullable=True)  # 惩罚
    a81921 = Column(DATETIME(8), nullable=True)  # 惩处年度
    a0188 = Column(INTEGER, nullable=False)  # 姓名

    def __repr__(self):
        return f"<A8192(a0188='{self.a0188}',a81921='{self.a81921}',a81923='{self.a81923}')>"


class A832(Base):
    # 职业证书子集
    __tablename__ = 'a832'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a83211 = Column(VARCHAR(100), nullable=False)  # 证书名称

    def __repr__(self):
        return f"<A832(a83211='{self.a83211}')>"


class A864(Base):
    # 家庭成员
    __tablename__ = 'a864'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    name = Column(VARCHAR(20), nullable=False)  # 亲属姓名
    a0188 = Column(INTEGER, nullable=False)  # 姓名
    a86412 = Column(VARCHAR(30), nullable=False)  # 与本人关系

    def __repr__(self):
        return f"<A864(a0188='{self.a0188}',a86412='{self.a86412}',name='{self.name}')>"


class A865(Base):
    # 社会兼职子集
    __tablename__ = 'a865'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False)  # 姓名

    def __repr__(self):
        return f"<A864(a0188='{self.a0188}')>"


class A866(Base):
    # 工作经历子集
    __tablename__ = 'a866'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False)  # 姓名
    a8661 = Column(DATETIME(8), nullable=False)  # 起始时间
    a8662 = Column(DATETIME(8), nullable=True)  # 终止时间

    def __repr__(self):
        return f"<A866(a0188='{self.a0188}',a8661='{self.a8661}',a8662='{self.a8662}')>"


class A875(Base):
    # 年度考核子集
    __tablename__ = 'a875'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a8759 = Column(VARCHAR(6), nullable=False)  # 年月
    a0188 = Column(INTEGER, nullable=False, index=True)  # 姓名
    khqk = Column(VARCHAR(20), nullable=False)  # 考核情况

    def __repr__(self):
        return f"<A875(a8759='{self.a8759}',a0188='{self.a0188}',khqk='{self.khqk}')>"


class Bm_gxsjb(Base):
    # 高校数据库V5
    __tablename__ = 'bm_gxsjb'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # record id
    mc0000 = Column(VARCHAR(40), nullable=False, index=True)  # name
    sfsyl = Column(VARCHAR(20), nullable=True)  # 是否双一流
    sfjbw = Column(VARCHAR(20), nullable=True)  # 是否985
    sf = Column(VARCHAR(20), nullable=True)  # 是否211
    qs100 = Column(VARCHAR(20), nullable=True)  # 是否QS100
    sfqs2 = Column(VARCHAR(20), nullable=True)  # 是否QS200

    def __repr__(self):
        return f"<Bm_gxsjb(mc0000='{self.mc0000}',sfsyl='{self.sfsyl}',sfjbw='{self.sfjbw}',sf='{self.sf}',qs100='{self.qs100}',sfqs2='{self.sfqs2}')>"


class Empat17(Base):
    # 内训师
    __tablename__ = 'empat17'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0190 = Column(VARCHAR(20), nullable=False, primary_key=True)  # 员工号
    a0188 = Column(INTEGER, nullable=False)  # 姓名
    years = Column(VARCHAR(4), nullable=True)  # 年度
    a81884 = Column(VARCHAR(50), nullable=True)  # 年末考核得分
    a81882 = Column(VARCHAR(20), nullable=True)  # 内训师现等级

    def __repr__(self):
        return f"<Empat17(a0190='{self.a0190}',a0188='{self.a0188}', years='{self.years}', a81884='{self.a81884}'," \
               f"a81882 = '{self.a81882}')>"


class Empat18(Base):
    # 学习平台
    __tablename__ = 'empat18'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False)  # 姓名
    years = Column(VARCHAR(4), nullable=True)  # 年度
    empat181 = Column(VARCHAR(50), nullable=True)  # 学习平台总学分

    def __repr__(self):
        return f"<Empat18(a0188='{self.a0188}', years='{self.years}', empat181='{self.empat181}')>"


# TODO empat19 字段不明确
class Empat19(Base):
    # 全员轮训
    __tablename__ = 'empat19'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False)  # 姓名
    years = Column(VARCHAR(4), nullable=True)  # 年度
    bixiuke = Column(VARCHAR(200),nullable=True) # 必修课
    gongkaike = Column(VARCHAR(200),nullable=True) # 公开课

    def __repr__(self):
        return f"<Empat19(a0188='{self.a0188}', years='{self.years}', bixiuke='{self.bixiuke}', " \
               f"gongkaike = '{self.gongkaike}')>"

class Gxlygydjx(Base):
    # 龙虎榜排名，各序列员工月度绩效
    __tablename__ = 'gxlygydjx'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    a0188 = Column(INTEGER, nullable=False)  # 姓名
    yjjxje = Column(NUMERIC(19, 2), nullable=True)  # 月均绩效金额
    year = Column(VARCHAR(4), nullable=True)  # 年份

    def __repr__(self):
        return f"<Gxlygydjx(a0188='{self.a0188}',yjjxje='{self.yjjxje}',year='{self.year}')>"


class K_month(Base):
    # 月结果
    __tablename__ = 'k_month'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    gz_ym = Column(VARCHAR(6), nullable=False)  # 年月
    leave_time_11 = Column(NUMERIC(19, 2), nullable=True)  # 事假天数
    leave_time_12 = Column(NUMERIC(19, 2), nullable=True)  # 病假天数

    def __repr__(self):
        return f"<K_month(gz_ym='{self.gz_ym}',leave_time_11='{self.leave_time_11}',leave_time_12='{self.leave_time_12}')>"


class Tability(Base):
    # 综合能力测评
    __tablename__ = 'tability'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    totalscore = Column(DECIMAL(4, 2), nullable=False)  # 总分

    def __repr__(self):
        return f"<Tability(totalscore='{self.totalscore}')>"


class Tpersonality(Base):
    # 性格测评
    __tablename__ = 'tpersonality'
    recordid = Column(INTEGER, nullable=False, primary_key=True, autoincrement=True)  # record id
    dominance = Column(INTEGER, nullable=False)  # 支配型
    influence = Column(INTEGER, nullable=False)  # 影响型
    steadiness = Column(INTEGER, nullable=False)  # 支持型
    compliance = Column(INTEGER, nullable=False)  # 思考型

    def __repr__(self):
        return f"<Tpersonality(dominance='{self.dominance}',influence='{self.influence}',steadiness='{self.steadiness}',compliance='{self.compliance}')>"

class A8187(Base):
    # 日志表
    __tablename__ = 'a8187'
    recordid = Column(INTEGER,nullable=False,primary_key=True) #记录标识号
    a_id = Column(INTEGER,nullable=True) #序号
    infochgfbid = Column(INTEGER,nullable=True) #信息变更申请附表ID
    a0188 = Column(INTEGER,nullable=False) #姓名
    gz_ym = Column(VARCHAR(6),nullable=False) #年月
    a81871 = Column(VARCHAR(20),nullable=True) #工号
    dept_code = Column(VARCHAR(200),nullable=False) #部门
    a81872 = Column(NUMERIC(19,2),nullable=True) #发布量
    a81873 = Column(NUMERIC(19,2),nullable=True) #点赞量
    a81874 = Column(NUMERIC(19,2),nullable=True) #浏览量
    a81875 = Column(NUMERIC(19,2),nullable=True) #回复量
    a81876 = Column(NUMERIC(19,2),nullable=True) #转发量
    a81877 = Column(NUMERIC(19,2),nullable=True) #互动总量
    a81878 = Column(NUMERIC(19,2),nullable=True) #总字数
    a81879 = Column(VARCHAR(20),nullable=True) #上榜次数
    opname = Column(VARCHAR(100),nullable=True) #操作者
    opdate = Column(DATETIME(8),nullable=True) #操作时间
    signed = Column(SMALLINT(2),nullable=True) #审批标记

    def __repr__(self):
        return f"<A8187(recordid='{self.recordid}',a_id='{self.a_id}',infochgfbid='{self.infochgfbid}',a0188='{self.a0188}',gz_ym='{self.gz_ym}',a81871='{self.a81871}',dept_code='{self.dept_code}',a81872='{self.a81872}',a81873='{self.a81873}',a81874='{self.a81874}',a81875='{self.a81875}',a81876='{self.a81876}',a81877='{self.a81877}',a81878='{self.a81878}',a81879='{self.a81879}',opname='{self.opname}',opdate='{self.opdate}',signed='{self.signed}')>"

class A8196(Base):
    # 项目活动子集
    __tablename__ = 'a8196'
    recordid = Column(INTEGER,nullable=False,primary_key=True) #记录标识号
    a0188 = Column(INTEGER,nullable=False) #姓名
    a_id = Column(INTEGER,nullable=True) #序号
    infochgfbid = Column(INTEGER,nullable=True) #信息变更申请附表ID
    a81961 = Column(VARCHAR(20),nullable=True) #项目/活动类型
    a81962 = Column(DATETIME(8),nullable=True) #开始时间
    a81963 = Column(DATETIME(8),nullable=True) #结束时间
    a81964 = Column(VARCHAR(500),nullable=True) #项目/活动名称
    a81965 = Column(VARCHAR(500),nullable=True) #项目/活动角色
    a81966 = Column(VARCHAR(500),nullable=True) #参与程度
    a81967 = Column(VARCHAR(1000),nullable=True) #项目/活动描述
    a81968 = Column(VARCHAR(500),nullable=True) #项目/活动负责人
    a81969 = Column(VARCHAR(500),nullable=True) #项目/活动照片
    signed = Column(SMALLINT(2),nullable=True) #审批标记
    opname = Column(VARCHAR(100),nullable=True) #操作者
    opdate = Column(DATETIME(8),nullable=True) #操作时间

    def __repr__(self):
        return f"<A8196(recordid='{self.recordid}',a0188='{self.a0188}',a_id='{self.a_id}',infochgfbid='{self.infochgfbid}',a81961='{self.a81961}',a81962='{self.a81962}',a81963='{self.a81963}',a81964='{self.a81964}',a81965='{self.a81965}',a81966='{self.a81966}',a81967='{self.a81967}',a81968='{self.a81968}',a81969='{self.a81969}',signed='{self.signed}',opname='{self.opname}',opdate='{self.opdate}')>"

class Kol(Base):
    # kol表
    __tablename__ = 'kol'
    recordid = Column(INTEGER,nullable=False,primary_key=True) #记录标识号
    a_id = Column(INTEGER,nullable=True) #序号
    infochgfbid = Column(INTEGER,nullable=True) #信息变更申请附表ID
    a0190 = Column(VARCHAR(20),nullable=True,index=True) #员工号
    a0188 = Column(INTEGER,nullable=False) #姓名
    gz_ym = Column(VARCHAR(6),nullable=False) #年月
    jf = Column(NUMERIC(19,2),nullable=True) #积分
    opname = Column(VARCHAR(100),nullable=True) #操作者
    opdate = Column(DATETIME(8),nullable=True) #操作时间
    signed = Column(SMALLINT(2),nullable=True) #审批标记

    def __repr__(self):
        return f"<Kol(recordid='{self.recordid}',a_id='{self.a_id}',infochgfbid='{self.infochgfbid}',a0190='{self.a0190}',a0188='{self.a0188}',gz_ym='{self.gz_ym}',jf='{self.jf}',opname='{self.opname}',opdate='{self.opdate}',signed='{self.signed}')>"


# 码表
class Bmyh_xl(Base):
    # 学历
    __tablename__ = 'bmyh_xl'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bmyh_xl(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bmyh_xw(Base):
    # 学位
    __tablename__ = 'bmyh_xw'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bmyh_xw(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bm_gxcw(Base):
    # 与本人关系
    __tablename__ = 'bm_gxcw'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bm_gxcw(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bm_jp_a01(Base):
    # 行员等级
    __tablename__ = 'bm_jp_a01'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bm_jp_a01(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bm_jylx(Base):
    # 教育类型
    __tablename__ = 'bm_jylx'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bm_jylx(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bm_sf0(Base):
    # 是否最高
    __tablename__ = 'bm_sf0'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bm_sf0(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bm_starlevel(Base):
    # 胜任力星级
    __tablename__ = 'bm_starlevel'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bm_starlevel(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bm_xldj(Base):
    # 职称
    __tablename__ = 'bm_xldj'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(40), nullable=False)  # 名称
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bm_xldj(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class Bm_zwtx(Base):
    # 职务
    __tablename__ = 'bm_zwtx'
    bm0000 = Column(VARCHAR(10), nullable=False, primary_key=True)  # 编码
    mc0000 = Column(VARCHAR(100), nullable=False)  # 职务岗位
    parentbm = Column(VARCHAR(10), nullable=True)  # 父编码
    grade = Column(INTEGER, nullable=True)  # 级数

    def __repr__(self):
        return f"<Bm_zwtx(bm0000='{self.bm0000}',mc0000='{self.mc0000}',parentbm='{self.parentbm}',grade='{self.grade}')>"


class B01(Base):
    # ’一级机构‘，’二级机构‘，’中心‘
    __tablename__ = 'b01'
    dept_code = Column(VARCHAR(100), nullable=False, primary_key=True)  # 机构内码
    content = Column(VARCHAR(100), nullable=False)  # 机构名称
    b0110 = Column(VARCHAR(200), nullable=True)  # 机构全称
    grade = Column(INTEGER, nullable=False)  # 机构级数
    bm0000 = Column(VARCHAR(20), nullable=True)  # 机构所属党组织

    def __repr__(self):
        return f"<B01(dept_code='{self.dept_code}',content='{self.content}',b0110='{self.b0110}',grade='{self.grade}',bm0000='{self.bm0000}')>"


class E01(Base):
    # 岗位
    __tablename__ = 'e01'
    e0101 = Column(INTEGER, nullable=False, primary_key=True)  # 岗位分布号
    dept_code = Column(VARCHAR(20), nullable=False)  # 部门名称
    bm0000 = Column(VARCHAR(60), nullable=False)  # 标准岗位名称
    mc0000 = Column(VARCHAR(200), nullable=True)  # 实体岗位名称

    def __repr__(self):
        return f"<E01(e0101='{self.e0101}',dept_code='{self.dept_code}',bm0000='{self.bm0000}',mc0000='{self.mc0000}')>"
