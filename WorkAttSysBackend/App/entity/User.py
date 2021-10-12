from App import db

# 用户信息表
from App.util.MapUtil import attApplicationType, checkType, recordStatus


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(11), primary_key = True)
    pwd = db.Column(db.String(18))
    name = db.Column(db.String(11))
    sex = db.Column(db.String(1))
    head_img = db.Column(db.String(100))
    phone = db.Column(db.String(11))
    company_name = db.Column(db.String(100), db.ForeignKey('company.name'))  # 关联公司
    face_data = db.Column(db.String(100))
    entry_time = db.Column(db.Date)
    department = db.Column(db.String(18))
    annual_freedays = db.Column(db.Integer)
    staff_status = db.Column(db.Integer)
    # 关联出勤表 一对多
    attrecs = db.relationship('Att_Record', backref = 'user')
    # 关联所有申请表 一对多
    msgrecs = db.relationship('Msg_Record', backref = 'user')
    # 关联月薪表 一对多
    paymons = db.relationship('Pay_Monthly', backref = 'user')


class UserFace(db.Model):
    __tablename__ = "user_face"
    id = db.Column(db.String(11), primary_key=True)
    data = db.Column(db.LargeBinary)    # 面部128维特征的向量
    shape = db.Column(db.String(11))    # 矩阵形状，一般为n*128，n表示图片数量
    accuracy = db.Column(db.Float)      # 最低余弦相似度，判别相似标准
    flag_id = db.Column(db.Integer)     # 标识更新次数


# 公司信息表
class Company(db.Model):
    __tablename__ = 'company'
    name = db.Column(db.String(11), primary_key = True)
    logo = db.Column(db.String(100))
    legal_person = db.Column(db.String(11))  # 法人姓名
    member_num = db.Column(db.Integer)
    hr_id = db.Column(db.String(11), unique = True)
    weekend_num = db.Column(db.Integer)
    # 关联员工 一对多
    users = db.relationship('User', backref = 'company')
    # 关联假期表 一对多
    holidays = db.relationship('Holiday', backref = 'company')
    # 关联出勤记录表 一对多
    attrecs = db.relationship('Att_Record', backref = 'company')
    # 关联部门信息表 一对多
    depts = db.relationship('Department', backref = 'company')
    # 关联所有申请表 一对多
    msgrecs = db.relationship('Msg_Record', backref = 'company')
    # 关联公告表 一对多
    notices = db.relationship('Notice', backref = 'company')
    # 关联月薪表 一对多
    paymons = db.relationship('Pay_Monthly', backref = 'company')


# 各公司假期表 和公司信息表一对多
class Holiday(db.Model):
    __tablename__ = 'holiday'
    id = db.Column(db.Integer, primary_key = True)  # 节假日编号
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  # 关联公司
    date = db.Column(db.Date)
    status = db.Column(db.String(11))


# 出勤记录表
class Att_Record(db.Model):
    __tablename__ = 'att_record'
    id = db.Column(db.Integer, primary_key = True)
    staff_id = db.Column(db.String(11), db.ForeignKey('user.id'))  # 关联员工
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  # 关联公司
    status = db.Column(db.Integer)
    mood = db.Column(db.Integer)
    check_time = db.Column(db.DateTime)
    check_type = db.Column(db.Integer)


# 部门信息表
class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.String(11), primary_key = True)
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  # 关联公司
    dept_name = db.Column(db.String(11))
    wage_h = db.Column(db.Integer)
    overtime_pay_h = db.Column(db.Integer)
    s_time = db.Column(db.Time)
    e_time = db.Column(db.Time)
    r_time = db.Column(db.Time)
    late_times = db.Column(db.Integer)
    vacation_days = db.Column(db.Integer)
    absent_times = db.Column(db.Integer)


# 所有申请记录表
class Msg_Record(db.Model):
    __tablename__ = 'msg_record'
    id = db.Column(db.Integer, primary_key = True)  # 所有申请的id
    type = db.Column(db.String(11))
    staff_id = db.Column(db.String(11), db.ForeignKey('user.id'))  # 关联员工
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  # 关联公司
    msg_id = db.Column(db.String(11))  # 所有申请在各自类别申请表中的id
    record_time = db.Column(db.DateTime)
    staff_comment = db.Column(db.String(100))
    hr_comment = db.Column(db.String(100))
    status = db.Column(db.Integer)


# 打卡申请表 第一类
class Att_Application(db.Model):
    __tablename__ = 'att_application'
    att_id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date)
    # type = db.Column(db.Integer)
    worktype = db.Column(db.Integer)
    new_att_status = db.Column(db.Integer)

    def output(self):
        return "申请修改" + str(self.date) + checkType[self.worktype - 1] \
               + "的状态为" + recordStatus[self.new_att_status - 1]


# 外派申请表 第五类
class Out_Application(db.Model):
    __tablename__ = 'out_application'
    out_id = db.Column(db.Integer, primary_key = True)
    place = db.Column(db.String(11))
    s_date = db.Column(db.Date)
    e_date = db.Column(db.Date)

    def output(self):
        return "申请于" + str(self.s_date) + "至" + str(self.e_date) + "外派至" + self.place


# 假期申请表 第三类
class Vacation_Application(db.Model):
    __tablename__ = 'vacation_application'
    vaca_id = db.Column(db.Integer, primary_key = True)
    s_date = db.Column(db.Date)
    e_date = db.Column(db.Date)
    days = db.Column(db.Float)

    def output(self):
        return "申请请假从" + str(self.s_date) + "至" + str(self.e_date) + "，共" + str(self.days) + "天"


# 销假申请表 第四类
class Back_Application(db.Model):
    __tablename__ = 'back_application'
    back_id = db.Column(db.Integer, primary_key = True)
    e_date = db.Column(db.Date)

    def output(self):
        return "申请提前于" + str(self.e_date) + "销假"


# 入职/离职申请表 第二类
class Company_Application(db.Model):
    __tablename__ = 'company_application'
    comp_id = db.Column(db.Integer, primary_key = True)
    company = db.Column(db.String(11))
    entry_quit = db.Column(db.Integer)

    def output(self):
        if self.entry_quit == 1:  # 入职
            return "请求加入" + self.company
        else:
            return "请求从所在公司" + self.company + "辞职"


# 各公司 公告表
class Notice(db.Model):
    __tablename__ = 'notice'
    notice_id = db.Column(db.Integer, primary_key = True)
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  # 关联公司
    datetime = db.Column(db.DateTime)
    info = db.Column(db.String(100))


# 各公司 时间限制表 一对一
class Time_Settings(db.Model):
    __tablename__ = 'time_settings'
    company_name = db.Column(db.String(11), primary_key = True)
    late_period = db.Column(db.Integer)
    early_period = db.Column(db.Integer)


# 月薪表 和员工、公司都是一对多
class Pay_Monthly(db.Model):
    __tablename__ = 'pay_monthly'
    id = db.Column(db.String(11), primary_key = True)
    staff_id = db.Column(db.String(11), db.ForeignKey('user.id'))  # 关联员工
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  # 关联公司
    month = db.Column(db.Date)
    pay = db.Column(db.Integer)
