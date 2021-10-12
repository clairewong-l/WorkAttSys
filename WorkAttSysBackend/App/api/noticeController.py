from App import app, db
from flask import request

from App.entity.User import Notice, Att_Record, User
from App.util.MapUtil import recordStatus
from App.util.httpUtil import serialize


@app.route('/company/getNewNotice', methods=["POST", "GET"])
def getNewNotice():
    company_name = request.values.get("company_name")
    notices = db.session.query(Notice).filter_by(company_name=company_name).order_by(Notice.datetime.desc())
    if notices is None:
        return {
            "status": 0,
            "msg": "该公司暂无公告"
        }
    result = []
    for item in notices:
        item.datetime = str(item.datetime)
        result.append(serialize(item))
    return{
        "status": 1,
        "data": result
    }


# 暂用
@app.route('/company/getStaffNews', methods=["POST", "GET"])
def getStaffNews():
    company_name = request.values.get("company_name")
    news_length = request.values.get("news_length")
    staffNews = db.session.query(
        User.name, Att_Record.check_time, Att_Record.status
    ).filter(
        Att_Record.company_name == company_name
    ).filter(
        User.id == Att_Record.staff_id
    ).order_by(Att_Record.check_time.desc()).limit(news_length).all()
    if staffNews is None or len(staffNews) < 1:
        return {
            "status": 0,
            "msg": "暂无动态"
        }
    result = []
    for item in staffNews:
        _dict = {'name': item[0], 'time': item[1].strftime("%Y-%m-%d"), 'info': recordStatus[item[2]-1]}
        result.append(_dict)
    return{
        "status": 1,
        "data": result
    }


@app.route('/company/addNotice', methods=["POST"])
def addNotice():
    company_name = request.json.get("company_name")
    datetime = request.json.get("datetime")
    info = request.json.get("info")
    _notice = Notice(company_name=company_name, datetime=datetime, info=info)
    db.session.add(_notice)
    db.session.commit()
    return{
        "status": 1,
        "data": {
            "notice_id": _notice.notice_id
        },
        "msg": "发布成功"
    }


@app.route('/company/updateNotice', methods=["POST"])
def updateNotice():
    _id = request.json.get("id")
    notice = db.session.query(Notice).filter_by(notice_id=_id).first()
    if notice is None:
        return {
            "status": 0,
            "msg": "该公告不存在！"
        }
    notice.datetime = request.json.get("datetime")
    notice.info = request.json.get("info")
    db.session.commit()
    return{
        "status": 1,
        "msg": "修改成功"
    }


@app.route('/company/deleteNotice', methods=["POST", "GET"])
def deleteNotice():
    _id = request.values.get("id")
    db.session.query(Notice).filter_by(notice_id=_id).delete()
    db.session.commit()
    return{
        "status": 1,
        "msg": "删除成功"
    }
