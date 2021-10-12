from sqlalchemy import cast, Date, TIMESTAMP, DateTime, String, BIGINT, func, and_
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from App import app, db
from flask import request

from App.entity.User import User, Msg_Record, Department, Time_Settings, Att_Record, Att_Application, \
    Company_Application, \
    Vacation_Application, Back_Application, Out_Application


import time
import datetime
from App.util.MapUtil import expression


@app.route('/user/checkin', methods=["POST", "GET"])
def checkin():
    # 获取前端用户id、公司名、部门名、打卡时间、用户表情
    staff_id = request.values.get('staff_id')
    company_name = request.values.get('company_name')
    department = request.values.get('department')
    check_time_str = request.values.get('check_time')
    mood = request.values.get('mood')
    print(check_time_str)

    check = datetime.datetime.strptime(check_time_str, "%Y-%m-%d %H:%M:%S")
    check_date = check.date()
    check_time = check.time()
    # 根据部门获取：规定打卡时间
    dept = db.session.query(Department).filter_by(dept_name=department).first()
    s_time = dept.s_time
    e_time = dept.e_time

    # 根据公司获得：规定打卡时间段
    comp = db.session.query(Time_Settings).filter_by(company_name=company_name).first()
    late_period = comp.late_period
    early_period = comp.early_period
    late_time = datetime.time(hour=s_time.hour + late_period, minute=s_time.minute, second=s_time.second)
    early_time = datetime.time(hour=e_time.hour - early_period, minute=e_time.minute, second=e_time.second)
    print(late_time.isoformat())
    print(early_time.isoformat())
    # 判断打卡为上下班
    today_records = db.session.query(Att_Record).filter(
        and_(cast(Att_Record.check_time, db.Date) == check_date, Att_Record.staff_id == staff_id)).all()
    print(today_records)
    if len(today_records) >= 2:
        return {
            "status": 1,
            "msg": "本日已完成两次打卡哟"
        }
    # 下班打卡
    elif len(today_records) == 1:
        check_type = 2
        h = datetime.timedelta(hours=early_period)
        if check_time >= e_time:
            status = 1  # 出勤
        elif check_time >= early_time:
            status = 3  # 早退
        else:
            status = 4  # 缺勤
    # 上班打卡
    elif len(today_records) == 0:
        check_type = 1
        if check_time <= s_time:
            status = 1  # 出勤
        elif check_time <= late_time:
            status = 2  # 迟到
        else:
            status = 4  # 缺勤
    # 表情提示
    if mood == 'normal':
        mood_msg = "ヽ(✿ﾟ▽ﾟ)ノ状态良好\n"
    elif mood == 'positive':
        mood_msg = "╰(*°▽°*)╯又是开心的一天\n"
    elif mood == 'negative':
        mood_msg = "ʕっ•ᴥ•ʔっ振作起来\n"
    else:mood_msg = "(づ￣ ³￣)づ\n"
    # 上班打卡状态为缺勤时，更改当日所有状态为缺勤
    if check_type == 1 and status == 4:
        chk_s = Att_Record(staff_id=staff_id, company_name=company_name,
                           status=status, check_time=check, check_type=1, mood=expression.index(mood))
        chk_e = Att_Record(staff_id=staff_id, company_name=company_name,
                           status=status, check_time=check, check_type=2, mood=expression.index(mood))
        db.session.add(chk_s)
        db.session.add(chk_e)
        db.session.commit()
        msg = "打卡成功！今日缺勤，下班无需打卡喽～"

    elif check_type == 1:
        chk = Att_Record(staff_id=staff_id, company_name=company_name, status=status, check_time=check,
                         check_type=check_type, mood=expression.index(mood))
        db.session.add(chk)
        db.session.commit()
        msg = "上班打卡成功！Have a nice day～"
    elif check_type == 2:
        chk = Att_Record(staff_id=staff_id, company_name=company_name, status=status, check_time=check,
                         check_type=check_type, mood=expression.index(mood))
        db.session.add(chk)
        db.session.commit()
        msg = "下班打卡成功！Bye～"
    else:
        msg = "好像哪里出了问题"

    return {
        "status": 1,
        "msg": mood_msg+msg
    }
