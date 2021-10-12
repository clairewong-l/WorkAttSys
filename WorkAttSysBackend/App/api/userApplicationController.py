from App import app, db
from flask import request

from App.entity.User import Vacation_Application, Msg_Record, Att_Application, \
    Company_Application, Back_Application, Out_Application, Company


# 提交打卡异常修改申请
@app.route('/user/attApplication', methods=["POST", "GET"])
def attApplication():
    date = request.values.get('date')
    # type = request.values.get('type')
    worktype = request.values.get('worktype')
    new_att_status = request.values.get('new_att_status')

    staff_comment = request.values.get('staff_comment')
    staff_id = request.values.get('staff_id')
    company_name = request.values.get('company_name')
    record_time = request.values.get('record_time')

    # 不能重复提交
    msg_record = db.session.query(Msg_Record).filter(Msg_Record.staff_id == staff_id). \
        filter(Msg_Record.type == "签到").filter(Msg_Record.status == "0").all()
    if len(msg_record) != 0:
        att_application = Att_Application()
        for i in msg_record:
            att_application = db.session.query(Att_Application).filter(Att_Application.att_id == i.msg_id).filter(
                Att_Application.date == date).filter(
                Att_Application.worktype == worktype).first()
        if att_application is not None:
            return {
                "status": 0,
                "msg": "请勿重复提交!"
            }
        else:
            aa = Att_Application(date=date, worktype=worktype, new_att_status=new_att_status)
            db.session.add(aa)
            db.session.commit()

            temp = aa.att_id
            msg_id = str(temp)
            mr = Msg_Record(msg_id=msg_id, type="签到", staff_id=staff_id, company_name=company_name,
                            staff_comment=staff_comment, record_time=record_time, status=0)
            db.session.add(mr)
            db.session.commit()

            return {
                "status": 1,
                "msg": "提交成功"
            }
    else:
        aa = Att_Application(date=date, worktype=worktype, new_att_status=new_att_status)
        db.session.add(aa)
        db.session.commit()

        temp = aa.att_id
        msg_id = str(temp)
        mr = Msg_Record(msg_id=msg_id, type="签到", staff_id=staff_id, company_name=company_name,
                        staff_comment=staff_comment, record_time=record_time, status=0)
        db.session.add(mr)
        db.session.commit()

        return {
            "status": 1,
            "msg": "提交成功"
        }


# 入职申请
@app.route('/user/entryApplication', methods=["POST", "GET"])
def entryApplication():
    company = request.values.get('company')
    entry_quit = 1

    staff_comment = request.values.get('staff_comment')
    staff_id = request.values.get('staff_id')
    record_time = request.values.get('record_time')

    comp = db.session.query(Company).filter_by(name=company).first()
    if comp is None:
        return {
            "status": 0,
            "msg": "该公司不存在"
        }
    else:
        # 不能重复提交
        msg_record = db.session.query(Msg_Record).filter(Msg_Record.staff_id == staff_id). \
            filter(Msg_Record.type == "入职").filter(Msg_Record.status == "0").all()
        if len(msg_record) != 0:
            company_application = Company_Application()
            for i in msg_record:
                company_application = db.session.query(Company_Application).filter(
                    Company_Application.comp_id == i.msg_id).filter(Company_Application.entry_quit == 1).first()
            if company_application is not None:
                return {
                    "status": 2,
                    "msg": "请勿重复提交!"
                }
            else:
                ca = Company_Application(company=company, entry_quit=entry_quit)
                db.session.add(ca)
                db.session.commit()

                temp = ca.comp_id
                msg_id = str(temp)
                mr = Msg_Record(msg_id=msg_id, type="入职", staff_id=staff_id, company_name=company,
                                staff_comment=staff_comment, record_time=record_time, status=0)
                db.session.add(mr)
                db.session.commit()

                return {
                    "status": 1,
                    "msg": "提交成功"
                }
        else:
            ca = Company_Application(company=company, entry_quit=entry_quit)
            db.session.add(ca)
            db.session.commit()

            temp = ca.comp_id
            msg_id = str(temp)
            mr = Msg_Record(msg_id=msg_id, type="入职", staff_id=staff_id, company_name=company,
                            staff_comment=staff_comment, record_time=record_time, status=0)
            db.session.add(mr)
            db.session.commit()

            return {
                "status": 1,
                "msg": "提交成功"
            }


# 离职申请
@app.route('/user/quitApplication', methods=["POST", "GET"])
def quitApplication():
    company = request.values.get('company')
    entry_quit = 2

    staff_comment = request.values.get('staff_comment')
    staff_id = request.values.get('staff_id')
    record_time = request.values.get('record_time')

    # 不能重复提交
    msg_record = db.session.query(Msg_Record).filter(Msg_Record.staff_id == staff_id). \
        filter(Msg_Record.type == "离职").filter(Msg_Record.status == "0").all()
    if len(msg_record) != 0:
        company_application = Company_Application()
        for i in msg_record:
            company_application = db.session.query(Company_Application).filter(
                Company_Application.comp_id == i.msg_id).filter(Company_Application.entry_quit == 2).first()
        if company_application is not None:
            return {
                "status": 0,
                "msg": "请勿重复提交!"
            }
        else:
            ca = Company_Application(company=company, entry_quit=entry_quit)
            db.session.add(ca)
            db.session.commit()

            temp = ca.comp_id
            msg_id = str(temp)
            mr = Msg_Record(msg_id=msg_id, type="离职", staff_id=staff_id, company_name=company,
                            staff_comment=staff_comment, record_time=record_time, status=0)
            db.session.add(mr)
            db.session.commit()

            return {
                "status": 1,
                "msg": "提交成功"
            }
    else:
        ca = Company_Application(company=company, entry_quit=entry_quit)
        db.session.add(ca)
        db.session.commit()

        temp = ca.comp_id
        msg_id = str(temp)
        mr = Msg_Record(msg_id=msg_id, type="离职", staff_id=staff_id, company_name=company,
                        staff_comment=staff_comment, record_time=record_time, status=0)
        db.session.add(mr)
        db.session.commit()

        return {
            "status": 1,
            "msg": "提交成功"
        }


# 提交请假申请
@app.route('/user/vacaApplication', methods=["POST", "GET"])
def vacaApplication():
    s_date = request.values.get('s_date')
    e_date = request.values.get('e_date')
    days = request.values.get('days')

    staff_comment = request.values.get('staff_comment')
    staff_id = request.values.get('staff_id')
    company_name = request.values.get('company_name')
    record_time = request.values.get('record_time')

    # 不能重复提交
    msg_record = db.session.query(Msg_Record).filter(Msg_Record.staff_id == staff_id). \
        filter(Msg_Record.type == "请假").filter(Msg_Record.status == "0").all()
    if len(msg_record) != 0:
        vacation_application = Vacation_Application()
        for i in msg_record:
            vacation_application = db.session.query(Vacation_Application).filter(
                Vacation_Application.vaca_id == i.msg_id).filter(Vacation_Application.s_date == s_date).filter(
                Vacation_Application.e_date == e_date).first()
        if vacation_application is not None:
            return {
                "status": 0,
                "msg": "请勿重复提交!"
            }
        else:
            va = Vacation_Application(s_date=s_date, e_date=e_date, days=days)
            db.session.add(va)
            db.session.commit()

            temp = va.vaca_id
            msg_id = str(temp)
            mr = Msg_Record(msg_id=msg_id, type="请假", staff_id=staff_id, company_name=company_name,
                            staff_comment=staff_comment, record_time=record_time, status=0)
            db.session.add(mr)
            db.session.commit()

            return {
                "status": 1,
                "msg": "提交成功"
            }
    else:
        va = Vacation_Application(s_date=s_date, e_date=e_date, days=days)
        db.session.add(va)
        db.session.commit()

        temp = va.vaca_id
        msg_id = str(temp)
        mr = Msg_Record(msg_id=msg_id, type="请假", staff_id=staff_id, company_name=company_name,
                        staff_comment=staff_comment, record_time=record_time, status=0)
        db.session.add(mr)
        db.session.commit()

        return {
            "status": 1,
            "msg": "提交成功"
        }


# 提交销假申请
@app.route('/user/backApplication', methods=["POST", "GET"])
def backApplication():
    e_date = request.values.get('e_date')

    staff_comment = request.values.get('staff_comment')
    staff_id = request.values.get('staff_id')
    company_name = request.values.get('company_name')
    record_time = request.values.get('record_time')

    # 不能重复提交
    msg_record = db.session.query(Msg_Record).filter(Msg_Record.staff_id == staff_id). \
        filter(Msg_Record.type == "销假").filter(Msg_Record.status == "0").all()
    if len(msg_record) != 0:
        back_application = Back_Application()
        for i in msg_record:
            back_application = db.session.query(Back_Application).filter(
                Back_Application.back_id == i.msg_id).filter(Back_Application.e_date == e_date).first()
        if back_application is not None:
            return {
                "status": 0,
                "msg": "请勿重复提交!"
            }
        else:
            ba = Back_Application(e_date=e_date)
            db.session.add(ba)
            db.session.commit()

            temp = ba.back_id
            msg_id = str(temp)
            mr = Msg_Record(msg_id=msg_id, type="销假", staff_id=staff_id, company_name=company_name,
                            staff_comment=staff_comment, record_time=record_time, status=0)
            db.session.add(mr)
            db.session.commit()

            return {
                "status": 1,
                "msg": "提交成功"
            }
    else:
        ba = Back_Application(e_date=e_date)
        db.session.add(ba)
        db.session.commit()

        temp = ba.back_id
        msg_id = str(temp)
        mr = Msg_Record(msg_id=msg_id, type="销假", staff_id=staff_id, company_name=company_name,
                        staff_comment=staff_comment, record_time=record_time, status=0)
        db.session.add(mr)
        db.session.commit()

        return {
            "status": 1,
            "msg": "提交成功"
        }


# 提交外派申请
@app.route('/user/outApplication', methods=["POST", "GET"])
def outApplication():
    s_date = request.values.get('s_date')
    e_date = request.values.get('e_date')
    place = request.values.get('place')

    staff_comment = request.values.get('staff_comment')
    staff_id = request.values.get('staff_id')
    company_name = request.values.get('company_name')
    record_time = request.values.get('record_time')

    # 不能重复提交
    msg_record = db.session.query(Msg_Record).filter(Msg_Record.staff_id == staff_id). \
        filter(Msg_Record.type == "外派").filter(Msg_Record.status == "0").all()
    if len(msg_record) != 0:
        out_application = Out_Application()
        for i in msg_record:
            out_application = db.session.query(Out_Application).filter(
                Out_Application.out_id == i.msg_id).filter(Out_Application.s_date == s_date).filter(
                Out_Application.e_date == e_date).filter(Out_Application.place == place).first()
        if out_application is not None:
            return {
                "status": 0,
                "msg": "请勿重复提交!"
            }
        else:
            oa = Out_Application(place=place, s_date=s_date, e_date=e_date)
            db.session.add(oa)
            db.session.commit()

            temp = oa.out_id
            msg_id = str(temp)
            mr = Msg_Record(msg_id=msg_id, type="外派", staff_id=staff_id, company_name=company_name,
                            staff_comment=staff_comment, record_time=record_time, status=0)
            db.session.add(mr)
            db.session.commit()

            return {
                "status": 1,
                "msg": "提交成功"
            }
    else:
        oa = Out_Application(place=place, s_date=s_date, e_date=e_date)
        db.session.add(oa)
        db.session.commit()

        temp = oa.out_id
        msg_id = str(temp)
        mr = Msg_Record(msg_id=msg_id, type="外派", staff_id=staff_id, company_name=company_name,
                        staff_comment=staff_comment, record_time=record_time, status=0)
        db.session.add(mr)
        db.session.commit()

        return {
            "status": 1,
            "msg": "提交成功"
        }
