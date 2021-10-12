import calendar
import datetime
from datetime import date

from sqlalchemy import and_, extract, cast

from App import app, db
from flask import request

from App.entity.User import Att_Record, User, Department
from App.util.MapUtil import recordStatus, statusNum
from App.util.httpUtil import serialize


@app.route('/company/getExRecordMsg', methods=["POST", "GET"])
def getExRecordMsg():
    company_name = request.values.get("company_name")
    datetime = request.values.get("datetime")
    records = db.session.query(
        Att_Record.status, User.id, User.department, User.name
    ).filter(
        and_(Att_Record.company_name == company_name,
             db.cast(Att_Record.check_time, db.DATE) == db.cast(datetime, db.DATE))
    ).filter(
        Att_Record.status != 1
    ).filter(
        and_(User.id == Att_Record.staff_id)
    ).all()
    if records is None or len(records) < 1:
        return {
            "status": 0,
            "msg": "暂无异常记录"
        }
    # print(records)
    result = []
    for item in records:
        _record = {
            'datetime': datetime,
            'status': recordStatus[item[0] - 1],
            'staff_id': item[1],
            'department': item[2],
            'name': item[3]
        }
        result.append(_record)
    return {
        "status": 1,
        "data": result
    }


@app.route('/company/getAllAttRecord', methods=["POST", "GET"])  # 获取记录和统计信息
def getAllAttRecord():
    company_name = request.values.get("company_name")
    _dateRange = request.values.get("date_range")  # 月份格式为yyyy-mm, 日期格式为yyyy-mm-dd
    if len(_dateRange) > 9:
        [oriDate, endDate] = _dateRange.split(' ')
    else:
        [_year, _month] = _dateRange.split('-')
        days = calendar.monthrange(int(_year), int(_month))[1]  # 获取该月的天数
        oriDate = _dateRange + '-01'
        endDate = _dateRange + str(-days)
    _detailResults = []
    # print(oriDate, endDate)
    # 先查员工，再查记录
    _staffRecords = db.session.query(
        User.id, User.name, User.department
    ).filter_by(company_name=company_name).all()
    if _staffRecords is None or len(_staffRecords) < 1:
        return {
            "status": 0,
            "msg": "一个员工都没有"
        }
    for _staffRecord in _staffRecords:
        # 查询每位员工的数据，主要是查询后需要一个分类统计
        _records0 = db.session.query(
            Att_Record.status, db.func.count(Att_Record.status)
        ).filter(
            Att_Record.check_time.between(oriDate, endDate),
            Att_Record.company_name == company_name
        ).filter(
            Att_Record.staff_id == _staffRecord[0]
        ).group_by(Att_Record.status).all()
        for _record0 in _records0:
            _result = {'staff_id': _staffRecord[0], 'name': _staffRecord[1], 'department': _staffRecord[2],
                        'status': recordStatus[_record0[0] - 1], 'count': _record0[1]}
            _detailResults.append(_result)
    # print(_detailResults)
    if _detailResults is None or len(_detailResults) < 1:
        return {
            "status": 0,
            "msg": "暂无考勤记录"
        }
    # 统计考勤记录
    _countResults = {}

    _records = db.session.query(
        db.func.date_format(Att_Record.check_time, '%Y-%m-%d').label('date'),
        Att_Record.status, db.func.count(Att_Record.status)
    ).filter(
        Att_Record.check_time.between(oriDate, endDate),
        Att_Record.company_name == company_name
    ).group_by(
        'date', Att_Record.status
    ).order_by('date').all()
    # print(_records)
    numRecords = {}
    for _record in _records:
        # _record为某天的某一条记录统计，需要先判断是不是同一天的记录
        _checkTime = _record[0]
        if _checkTime not in _countResults:
            numRecords = {}
            _countResults[_checkTime] = numRecords
        numRecords[statusNum[_record[1] - 1]] = _record[2]     # 加入一类统计记录

    return {
        "status": 1,
        "data": {
            "allAttRecord": _detailResults,
            "allAttRecordCount": _countResults
        }
    }


# 显示日历某月对应打卡颜色以及缺勤总天数
@app.route('/user/staffDetail/showCalenderColor', methods=["POST", "GET"])
def showCalenderColor():
    wage_d, absent = 0, 0  # 日薪、该月缺勤天数
    staff_id = request.values.get("staff_id")
    # 查询时薪
    staff = db.session.query(User).filter_by(id = staff_id).first()
    if staff.department is not None:
        dept = db.session.query(Department).filter_by(dept_name=staff.department).first()
        wage_h = dept.wage_h    # 时薪
        time_e = datetime.datetime.combine(datetime.date.today(), dept.e_time)
        time_s = datetime.datetime.combine(datetime.date.today(), dept.s_time)
        work_time = (time_e-time_s).total_seconds()/(60*60)
        wage_d = wage_h*work_time   # 日薪

    month = request.values.get("month", type=int)
    year = request.values.get("year", type=int)
    s_date = date(year, month, 1)
    e_date = date(year, month + 1, 1)
    print(s_date.isoformat())
    print(e_date.isoformat())
    results = {}
    recs = db.session.query(
        Att_Record.check_time, Att_Record.status).filter(
        and_(Att_Record.staff_id == staff_id,
             cast(Att_Record.check_time, db.Date) >= s_date,
             cast(Att_Record.check_time, db.Date) < e_date)).order_by(
        Att_Record.check_time.asc()).all()
    a = False  # 同一天两个数据标识位
    num = 0  # 计数器
    for rec in recs:
        status = 0  # 考勤是否正常：1正常，0不正常
        if a:
            a = False
            continue
        check_date = rec.check_time.date()
        check_date_str = check_date.isoformat()  # YYYY-MM-DD
        r = db.session.query(Att_Record.status).filter(
            and_(cast(Att_Record.check_time, db.Date) == check_date,
                 Att_Record.staff_id == staff_id)).all()
        if len(r) == 1:
            if rec.status == 1:
                status = 1
                print("1date:", check_date_str, "status:", status)
            else:
                status = 0
                print("2date:", check_date_str, "status:", status)
        elif len(r) == 2:
            if r.count((1,)) == 2:
                status = 1
                a = True
                print("3date:", check_date_str, "status:", status)
            else:
                status = 0
                a = True
                if r.count((4,)) > 0:
                    absent = absent + 1
        result = {
            "status": status,
            "date": check_date_str
        }
        results[f"{num}"] = result
        num = num + 1

    deduct_pay = str(absent*wage_d)
    return {
        "msg": "获取成功",
        "num": num,
        "absent_day": absent,
        "deduct_pay": deduct_pay,
        "data": results
    }
