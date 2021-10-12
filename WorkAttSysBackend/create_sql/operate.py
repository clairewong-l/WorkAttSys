from models import db,User,Company_Application,Company,Out_Application,\
    Back_Application,Att_Application,Vacation_Application,\
    Notice,Att_Record,Msg_Record,Department,Holiday,Pay_Monthly,Time_Settings
#
# u1 = User(id='u0001',name='张三',sex='女',company_name='淘宝')
# u2 = User(id='u0002',name='李三',sex='女',company_name='天猫')
# u3 = User(id='u0003',name='李三一',sex='女',company_name='天猫')
# u4 = User(id='u0004',name='成木',sex='男',company_name='饿了么')
# u5 = User(id='u0005',name='陈问',sex='男',company_name='美团')
# u6 = User(id='u0006',name='时加',sex='女',company_name='新浪')
# u7 = User(id='u0007',name='许子听',sex='女',company_name='美团')
# db.session.add_all([u1,u2,u3,u4,u5,u6,u7])
#
# c1 = Company(name='天猫')
# c2 = Company(name='淘宝')
# c3 = Company(name='饿了么')
# c4 = Company(name='美团',hr_id='h0001')
# c5 = Company(name='新浪',hr_id='h0002')
# c6 = Company(name='腾讯',hr_id='h0003')
# db.session.add_all([c1,c2,c3,c4,c5,c6])
#
# mr = Msg_Record(id='1',type_id='1',staff_id='u0001',company_name='淘宝',msg_id='a1',hr_comment='同意')
# aa = Att_Application(att_id='a1',type='1')
# db.session.add_all([mr,aa])
# db.session.commit()
#
# user = User.query.get('u0001')
# user = User.query.all()

# user = db.session.query(User).filter_by(id='u0001').first()
# print(user.name)

# 通过公司表查询员工姓名 get根据主键
# com = Company.query.get('天猫')
# for i in com.users:
#     print(i.name)

# 通过员工表查询公司表的内容
# user = db.session.query(User).filter_by(id='u0005').first()
# print(user.company.hr_id)
# va = Vacation_Application(s_date='2020-07-04',e_date='2020-08-05')
# db.session.add(va)
# db.session.commit()
# d=va.vaca_id
#
# msg_id = "vaca"+str(d)
# mr = Msg_Record(msg_id=msg_id)
# db.session.add(mr)
# db.session.commit()