from sqlalchemy import and_, or_

from App import app, db
from flask import request

from App.entity.User import User, Msg_Record, Att_Application, Company_Application, \
    Vacation_Application, Back_Application, Out_Application, Att_Record


@app.route('/company/getApplicationMsg', methods=["POST", "GET"])
def getApplicationMsg():
    company_name = request.values.get("company_name")
    _records = db.session.query(
        Msg_Record.id, Msg_Record.type, Msg_Record.staff_id, Msg_Record.staff_comment, Msg_Record.record_time,
        User.name, User.department, User.head_img, Msg_Record.msg_id
        # Msg_Record, User
    ).join(User, Msg_Record.staff_id == User.id).filter(
        and_(Msg_Record.company_name == company_name, Msg_Record.status == 0)  # 只需要待处理的申请
    ).all()
    # print(_records)
    if _records is None or len(_records) < 1:
        return {
            "status": 0,
            "msg": "暂无申请记录"
        }
    result = []
    for item in _records:
        print(len(item))
        # 处理具体的申请消息
        targetType = item[1]
        targetID = item[8]
        # print(targetType, targetID)
        baseInfo = info = ''
        if targetType == "签到":
            baseInfo = db.session.query(Att_Application).filter_by(att_id=targetID).first()
        elif targetType == "入职" or targetType == "离职":
            baseInfo = db.session.query(Company_Application).filter_by(comp_id=targetID).first()
        elif targetType == "请假":
            baseInfo = db.session.query(Vacation_Application).filter_by(vaca_id=targetID).first()
        elif targetType == "销假":
            baseInfo = db.session.query(Back_Application).filter_by(back_id=targetID).first()
        elif targetType == "外派":
            baseInfo = db.session.query(Out_Application).filter_by(out_id=targetID).first()
        info = item[5] + baseInfo.output() if baseInfo else "暂无具体消息"
        _dict = {
            'application_id': item[0], 'type': item[1], 'name': item[5],
            'head_img': item[7], 'staff_id': item[2], 'department': item[6],
            'info': info, 'staff_comment': item[3], 'datetime': item[4].strftime("%Y-%m-%d")
        }
        result.append(_dict)
    return {
        "status": 1,
        "data": result
    }


@app.route('/user/getUserApplicationMsg', methods=["POST", "GET"])
def getUserApplicationMsg():
    user_id = request.values.get("id")
    # 在申请记录表中查找该员工所有记录并按时间降序排列
    records = db.session.query(Msg_Record).filter_by(staff_id=user_id).order_by(Msg_Record.record_time.asc()).all()
    results = {}
    # record = db.session.query(Msg_Record).filter_by(staff_id=user_id).first()
    # msg = db.session.query(Att_Application).filter_by(att_id=record.msg_id).first()
    # print(msg.date.isoformat())
    appNum = {
        "attApp": 0,
        "entryApp": 0,
        "vacaApp": 0,
        "backApp": 0,
        "outApp": 0
    }
    for record in records:

        record_time_str = record.record_time.strftime("%Y-%m-%d %H:%M")
        print(record_time_str)
        if record.status == 0 or record.status is None:
            record_status = "待审批"
        elif record.status == 1:
            record_status = "已通过"
        elif record.status == 2:
            record_status = "未通过"
        else:
            record_status = "无"
        if record.type == "签到":
            appNum["attApp"] = appNum["attApp"] + 1
            msg = db.session.query(Att_Application).filter_by(att_id=record.msg_id).first()
            if msg.worktype == 1:
                work_type = "上班"
            elif msg.worktype == 2:
                work_type = "下班"
            else:
                pass
            if msg.new_att_status == 1:
                att_status = "出勤"
            elif msg.new_att_status == 2:
                att_status = "迟到"
            elif msg.new_att_status == 3:
                att_status = "早退"
            elif msg.new_att_status == 4:
                att_status = "缺勤"
            elif msg.new_att_status == 5:
                att_status = "请假"
            result = {
                "type": record.type,
                "date": msg.date.isoformat(),
                "worktype": work_type,
                "new_att_status": att_status,
                "record_time": record_time_str,
                "record_status": record_status
            }
            i = appNum["attApp"]
            results[f"{record.type}{i}"] = result
        elif record.type == "入职" or record.type == "离职":
            appNum["entryApp"] = appNum["entryApp"] + 1
            msg = db.session.query(Company_Application).filter_by(comp_id=record.msg_id).first()
            result = {
                "type": record.type,
                "company": msg.company,
                "record_time": record_time_str,
                "record_status": record_status
            }
            i = appNum["entryApp"]
            results[f"{record.type}{i}"] = result
        elif record.type == "请假":
            appNum["vacaApp"] = appNum["vacaApp"] + 1
            msg = db.session.query(Vacation_Application).filter_by(vaca_id=record.msg_id).first()
            result = {
                "type": record.type,
                "s_date": msg.s_date.isoformat(),
                "e_date": msg.e_date.isoformat(),
                "days": msg.days,
                "record_time": record_time_str,
                "record_status": record_status
            }
            i = appNum["vacaApp"]
            results[f"{record.type}{i}"] = result
        elif record.type == "销假":
            appNum["backApp"] = appNum["backApp"] + 1
            msg = db.session.query(Back_Application).filter_by(back_id=record.msg_id).first()
            result = {
                "type": record.type,
                "e_date": msg.e_date.isoformat(),
                "record_time": record_time_str,
                "record_status": record_status
            }
            i = appNum["backApp"]
            results[f"{record.type}{i}"] = result
        elif record.type == "外派":
            appNum["outApp"] = appNum["outApp"] + 1
            msg = db.session.query(Out_Application).filter_by(out_id=record.msg_id).first()
            result = {
                "type": record.type,
                "s_date": msg.s_date.isoformat(),
                "e_date": msg.e_date.isoformat(),
                "place": msg.place,
                "record_time": record_time_str,
                "record_status": record_status
            }
            i = appNum["backApp"]
            results[f"{record.type}{i}"] = result
        else:
            pass
    print("1")
    return {
        "status": 1,
        "appNum": appNum,
        "results": results
    }


@app.route('/company/disposeApplicationMsg', methods=["POST"])
def disposeApplicationMsg():
    _id = request.json.get("id")
    print(_id)
    record = db.session.query(Msg_Record).filter_by(id=_id).first()
    user = db.session.query(User).filter_by(id=record.staff_id).first()
    if record is None:
        return {
            "status": 0,
            "msg": "该申请不存在！"
        }
    record.status = request.json.get("status")
    if record.status == 1:
        if record.type == "入职":
            comp = db.session.query(Company_Application).filter_by(comp_id=record.msg_id).first()
            user.company_name = comp.company
        if record.type == "离职":
            user.company_name = None
        if record.type == "外派":
            user.staff_status = 3
        if record.type == "请假":
            user.staff_status = 2
        if record.type == "销假":
            user.staff_status = 1
        if record.type == "签到":
            att_application = db.session.query(Att_Application).filter_by(att_id=record.msg_id).first()
            att = db.session.query(Att_Record).filter(
                Att_Record.check_type == att_application.worktype
            ).filter(
                db.cast(Att_Record.check_time, db.DATE) == att_application.date
            ).filter(
                Att_Record.staff_id == record.staff_id
            ).first()
            att.status = att_application.new_att_status
    record.hr_comment = request.json.get("hr_comment")
    db.session.commit()
    return {
        "status": 1,
        "msg": "修改成功"
    }
