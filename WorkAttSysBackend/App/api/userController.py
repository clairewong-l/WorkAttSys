#!/usr/bin/python3
# encoding:utf-8
# coding: UTF-8
import json

import pymysql
from sqlalchemy import and_

from App import app, db
from flask import request

from App.entity.User import User, Att_Record, Notice, UserFace
from App.util.httpUtil import serialize
import traceback


# 改密码
@app.route('/user/staffDetail/changePsw', methods = ["POST", "GET", "PUT"])
def change_psw():
    user_id = request.values.get("id")
    new_psw = request.values.get("new_psw")
    user = db.session.query(User).filter_by(id = user_id).first()
    user.pwd = new_psw
    db.session.commit()
    return f"密码已修改，新密码为{user.pwd}"


# 显示员工打卡记录
@app.route('/user/staffDetail/showAttRec', methods = ["POST", "GET"])
def show_attrec():
    date = request.values.get('date')
    staff_id = request.values.get('staff_id')
    attrecs = db.session.query(Att_Record).filter(
        and_(db.cast(Att_Record.check_time, db.DATE) == date, Att_Record.staff_id == staff_id)).all()
    print(attrecs)
    temp_status = []  # 存放打卡状态
    temp_type = []  # 存放上下班类别
    for i in attrecs:
        temp_type.append(i.check_type)
        temp_status.append(i.status)
    if len(temp_status) > 2:
        temp_type = temp_type[:2]
        temp_status = temp_status[:2]

    if len(temp_status) == 0:
        return {
            "status": 0,
            "msg": "\\"
        }
    elif len(temp_status) == 1:
        if temp_type[0] == 1:  # 上班
            type2 = "\\"
            if temp_status[0] == 1:
                type1 = "出勤"
            elif temp_status[0] == 2:
                type1 = "迟到"
            elif temp_status[0] == 4:
                type1 = "缺勤"
            elif temp_status[0] == 5:
                type1 = "请假"
        else:  # 下班
            type1 = "无"
            if temp_status[0] == 1:
                type2 = "出勤"
            elif temp_status[0] == 3:
                type2 = "早退"
            elif temp_status[0] == 4:
                type2 = "缺勤"
            elif temp_status[0] == 5:
                type2 = "请假"

        return {
            "status": 1,
            "msg": "打卡一次",
            "data": {
                "type1": type1,
                "type2": type2
            }
        }
    elif len(temp_status) == 2:
        if temp_status[0] == 1:
            type1 = "出勤"
        elif temp_status[0] == 2:
            type1 = "迟到"
        elif temp_status[0] == 4:
            type1 = "缺勤"
        elif temp_status[0] == 5:
            type1 = "请假"

        if temp_status[1] == 1:
            type2 = "出勤"
        elif temp_status[1] == 3:
            type2 = "早退"
        elif temp_status[1] == 4:
            type2 = "缺勤"
        elif temp_status[1] == 5:
            type2 = "请假"

        return {
            "status": 1,
            "msg": "打卡两次",
            "data": {
                "type1": type1,
                "type2": type2
            }
        }


# 登录
@app.route('/user/login', methods = ["POST", "GET"])
def login():
    user_id = request.values.get("id")
    psw = request.values.get("password")
    user = db.session.query(User).filter_by(id=user_id).first()
    user_face = db.session.query(UserFace).filter_by(id=user_id).first()
    if user is None:
        return {
            "status": 0,
            "msg": "该账号不存在，请注册"
        }
    else:
        if user.pwd == psw:
            if user_face==None:
                flag = 0
            else: flag = 1
            return {
                "status": 1,
                "msg": "登录成功！",
                "data": {
                    "id": user_id,
                    "name": user.name,
                    "company": user.company_name,
                    'pwd': user.pwd,
                    'phone': user.phone,
                    'sex': user.sex,
                    'head_img': user.head_img,
                    'department': user.department,
                    'annual_freedays': user.annual_freedays,
                    "flag": flag
                }
            }
        else:
            return {
                "status": 0,
                "msg": "密码错误，请重新输入"
            }


# 注册
@app.route('/user/register', methods=["POST", "GET"])
def register():
    user_id = request.values.get("id")
    if len(user_id) == 0:
        return {
            "status": 0,
            "msg": "请填写工号！"
        }
    user = db.session.query(User).filter_by(id = user_id).first()
    if user is None:
        username = request.values.get("name")
        pwd = request.values.get("pwd")
        pwd_2 = request.values.get("pwd_2")
        sex = request.values.get("sex")
        phone = request.values.get("phone")
        if len(username) == 0:
            return {
                "status": 0,
                "msg": "请填写姓名！"
            }
        elif len(pwd) == 0:
            return {
                "status": 0,
                "msg": "请填写密码！"
            }
        elif len(phone) == 0:
            return {
                "status": 0,
                "msg": "请填写手机号！"
            }
        elif pwd != pwd_2:
            return {
                "status": 0,
                "msg": "两次密码填写不一致！"
            }
        else:
            user = User(id = user_id, name = username, pwd = pwd, sex = sex, phone = phone)
            db.session.add(user)
            db.session.commit()
            return {
                "status": 1,
                "msg": "注册成功"
            }
    else:
        return {
            "status": 0,
            "msg": "该账号已存在!"
        }


# 员工查看公司公告信息
@app.route('/user/staffDetail/showNotice', methods = ["POST", "GET"])
def showNotice():
    company = request.values.get("company")
    notice = db.session.query(Notice).filter_by(company_name = company).all()
    list = []  # 存储多条数据
    for i in notice:
        i = serialize(i)  # 序列化
        i['datetime'] = str(i['datetime'])
        list.append(i)
    if len(list) == 0:
        return {
            "status": 0,
            "msg": "该公司暂无公告信息"
        }
    else:
        return {
            "status": 1,
            "msg": "获取成功",
            "data": {
                "notice": list
            }
        }

