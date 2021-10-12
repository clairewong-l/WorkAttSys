from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/workattsys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)

# 用户信息表
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(11), primary_key=True)
    pwd = db.Column(db.String(18))
    name = db.Column(db.String(11))
    sex = db.Column(db.String(1))
    head_img = db.Column(db.String(100))
    phone = db.Column(db.String(11))
    company_name = db.Column(db.String(100), db.ForeignKey('company.name'))  #关联公司
    face_data = db.Column(db.String(100))
    entry_time = db.Column(db.Date)
    department = db.Column(db.String(18))
    annual_freedays = db.Column(db.Integer)
    staff_status = db.Column(db.Integer)
    # 关联出勤表 一对多
    attrecs = db.relationship('Att_Record', backref='user')
    # 关联所有申请表 一对多
    msgrecs = db.relationship('Msg_Record', backref='user')
    # 关联月薪表 一对多
    paymons = db.relationship('Pay_Monthly', backref='user')

# 公司信息表
class Company(db.Model):
    __tablename__ = 'company'
    name = db.Column(db.String(11), primary_key=True)
    logo = db.Column(db.String(100))
    legal_person = db.Column(db.String(11))#法人姓名
    member_num = db.Column(db.Integer)
    hr_id = db.Column(db.String(11), unique=True)
    weekend_num = db.Column(db.Integer)
    # 关联员工 一对多
    users = db.relationship('User', backref='company')
    # 关联假期表 一对多
    holidays = db.relationship('Holiday', backref='company')
    # 关联出勤记录表 一对多
    attrecs = db.relationship('Att_Record', backref='company')
    # 关联部门信息表 一对多
    depts = db.relationship('Department', backref='company')
    # 关联所有申请表 一对多
    msgrecs = db.relationship('Msg_Record', backref='company')
    # 关联公告表 一对多
    notices = db.relationship('Notice', backref='company')
    # 关联月薪表 一对多
    paymons = db.relationship('Pay_Monthly', backref='company')

# 各公司假期表 和公司信息表一对多
class Holiday(db.Model):
    __tablename__ = 'holiday'
    id = db.Column(db.Integer, primary_key=True)  #节假日编号
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  #关联公司
    s_time = db.Column(db.Date)
    e_time = db.Column(db.Date)

# 出勤记录表
class Att_Record(db.Model):
    __tablename__ = 'att_record'
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.String(11), db.ForeignKey('user.id'))  #关联员工
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  #关联公司
    status = db.Column(db.Integer)
    mood = db.Column(db.Integer)
    check_time = db.Column(db.DateTime)
    check_type = db.Column(db.Integer)

# 部门信息表
class Department(db.Model):
    __tablename__ = 'department'
    dept_id = db.Column(db.String(11), primary_key=True)
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  #关联公司
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
    id = db.Column(db.Integer, primary_key=True)  #所有申请的id
    type = db.Column(db.String(11))
    staff_id = db.Column(db.String(11), db.ForeignKey('user.id'))  #关联员工
    company_name = db.Column(db.String(11), db.ForeignKey('company.name'))  #关联公司
    msg_id = db.Column(db.String(11), unique=True)  #所有申请在各自类别申请表中的id
    record_time = db.Column(db.DateTime)
    staff_comment = db.Column(db.String(100))
    hr_comment = db.Column(db.String(100))
    status = db.Column(db.Integer)

# 打卡申请表 第一类
class Att_Application(db.Model):
    __tablename__ = 'att_application'
    att_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    type = db.Column(db.Integer)
    worktype = db.Column(db.Integer)
    new_att_status = db.Column(db.Integer)

# 外派申请表 第五类
class Out_Application(db.Model):
    __tablename__ = 'out_application'
    out_id = db.Column(db.Integer, primary_key=True)
    place = db.Column(db.String(11))
    s_date = db.Column(db.Date)
    e_date = db.Column(db.Date)

# 假期申请表 第三类
class Vacation_Application(db.Model):
    __tablename__ = 'vacation_application'
    vaca_id = db.Column(db.Integer, primary_key=True)
    s_date = db.Column(db.Date)
    e_date = db.Column(db.Date)
    days = db.Column(db.Float)

# 销假申请表 第四类
class Back_Application(db.Model):
    __tablename__ = 'back_application'
    back_id = db.Column(db.Integer, primary_key=True)
    e_date = db.Column(db.Date)

# 入职/离职申请表 第二类
class Company_Application(db.Model):
    __tablename__ = 'company_application'
    comp_id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(11))
    entry_quit = db.Column(db.Integer)

# 各公司 公告表
class Notice(db.Model):
    __tablename__ = 'notice'
    notice_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(11),db.ForeignKey('company.name'))  #关联公司
    datetime = db.Column(db.DateTime)
    info = db.Column(db.String(100))

# 各公司 时间限制表 一对一
class Time_Settings(db.Model):
    __tablename__ = 'time_settings'
    company_name = db.Column(db.String(11), primary_key=True)
    late_period = db.Column(db.Integer)
    absence_period = db.Column(db.Integer)
    early_period = db.Column(db.Integer)

# 月薪表 和员工、公司都是一对多
class Pay_Monthly(db.Model):
    __tablename__ = 'pay_monthly'
    id = db.Column(db.String(11),primary_key=True)
    staff_id = db.Column(db.String(11),db.ForeignKey('user.id')) #关联员工
    company_name = db.Column(db.String(11),db.ForeignKey('company.name')) #关联公司
    month = db.Column(db.Date)
    pay = db.Column(db.Integer)

if __name__=="__main__":
    db.drop_all()
    #db.create_all()