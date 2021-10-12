import json

from sqlalchemy import or_, and_

from App import app, db
from flask import jsonify, request, json
from App.entity.User import User, Company, Department, Time_Settings

from flask_cors import cross_origin


# HR注册
@app.route('/company/applyRegister', methods=["POST", "GET"])
def applyRegister():
    method = request.method

    # user_id = request.values.get("id")
    info = request.get_data()
    info = json.loads(info)
    user = db.session.query(User).filter_by(id=info["id"]).first()

    from App.entity.User import Company

    comp = db.session.query(Company).filter_by(name=info["company_name"]).first()
    if user is None and comp is None:
        Company = Company(name=info["company_name"], hr_id=info["id"], legal_person=info["legal_person"])
        db.session.add(Company)
        db.session.commit()
        user = User(id=info["id"], name=info["name"], pwd=info["pwd"], phone="phone",
                    company_name=info["company_name"])
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": 1, "msg": "注册成功"})

    return jsonify({"status": 0, "msg": "工号存在"})


# HR登录
@app.route('/company/modifyLogin', methods=["POST", "GET"])
def modifylogin():
    user_id = request.values.get("id")
    pwd = request.values.get("password")
    info = request.get_data()
    info = json.loads(info)
    if "HR" not in info["id"]:
        return {
            "status": 0,
            "msg": "你不是HR"
        }
    user = db.session.query(User).filter_by(id=info["id"]).first()
    if user is None:
        return {
            "status": 0,
            "msg": "该账号不存在，请注册"
        }
    else:
        if user.pwd == info["pwd"]:
            return {
                "status": 1,
                "msg": "登录成功！",
                "data": {
                    "name": user.name,
                    "company": user.company_name,

                }
            }
        else:
            return {
                "status": 0,
                "msg": "密码错误，请重新输入"
            }


# 获取员工列表
@app.route('/company/getStaff', methods=["POST", "GET"])
def getstaff():
    try:
        info = request.get_data()
        info = json.loads(info)
        print(info)

        if "filters" in info and str(info["filters"]["name"]) != "":
            company_name = request.json.get("company_name")
            res = db.session.query(User).filter(and_(
                or_(User.id == info["filters"]["name"], User.name == info["filters"]["name"],
                    User.department == info["filters"]["name"])), User.company_name==info["company_name"])   # .filter_by( # company_name=company_name)

        else:
            company_name = request.json.get("company_name")
            #print(company_name)
            res = db.session.query(
                User
            ).filter_by(
                company_name=company_name
            )
            # res = db.session.query(User).limit(8).offset((info["page"] - 1) * 8)
        # print(res)
        userlist = []
        for item in res:
            userdict = {}
            userdict["id"] = (item.id)
            userdict["name"] = (item.name)
            userdict["sex"] = (item.sex)
            userdict["head_img"] = (item.head_img)
            userdict["phone"] = (item.phone)
            userdict["company_name"] = (item.company_name)
            userdict["face_data"] = (item.face_data)
            userdict["entry_time"] = (item.entry_time)
            userdict["department"] = (item.department)
            userdict["annual_freedays"] = (item.annual_freedays)
            if item.staff_status == 1:
                staff_status = "出勤"
            elif item.staff_status == 2:
                staff_status = "请假"
            else:
                staff_status = "外派"
            userdict["staff_status"] = staff_status
            userlist.append(userdict)
        total = db.session.query(User).count()
        ##生成部门列表
        from App.entity.User import Department
        company_name = request.json.get("company_name")
        res = db.session.query(Department).filter_by(
            company_name=company_name
        )
        list1 = []
        for item in res:
            dict1 = {}
            dict1["value"] = item.dept_name
            dict1["label"] = item.dept_name
            list1.append(dict1)
        return jsonify({"status": 1, "data": userlist, "total": total, "options": list1})
    except Exception as e:
        print(e)
        return jsonify({"status": 0, "msg": "接口异常"})


# 员工新增
@app.route('/company/addStaff', methods=["POST", "GET"])
def addstaff():
    info = request.get_data()
    info = json.loads(info)
    company_name = request.json.get("company_name")
    user = db.session.query(User).filter_by(id=info["para"]["staff_id"], company_name=User.company_name).first()
    print(info)
    if user is not None:
        return jsonify({
            "status": 0,
            "msg": "该员工已经存在"
        })
    else:
        if info["para"]["sex"] == 1:
            sex = "男"
        else:
            sex = "女"
        # if info["staff_status"]==1:
        #     staff_status="在职"
        # elif info["staff_status"]==2:
        #     staff_status="离职"
        # else:
        #     staff_status="外派"
        print(company_name)
        user = User(id=info["para"]["staff_id"], name=info["para"]["name"], sex=sex, department=info["para"]["department"],
                    annual_freedays=info["para"]["annual_freedays"], entry_time=info["para"]["entry_time"], company_name=company_name,
                    staff_status=info["para"]["staff_status"], )
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": 1, "data": {}, "msg": "添加成功"})


# 员工修改
@app.route('/company/updateStaff', methods=["POST", "GET"])
def updatestaff():
    try:
        info = request.get_data()
        info = json.loads(info)
        # print(info)
        if info["sex"] == 1:
            sex = "男"
        else:
            sex = "女"
        # if info["staff_status"]==1:
        #     staff_status="在职"
        # elif info["staff_status"]==2:
        #     staff_status="离职"
        # else:
        #     staff_status="外派"
        # user = User(id=info["staff_id"], name=info["name"], sex=sex, department=info["department"],annual_freedays=info["annual_freedays"], entry_time=info["entry_time"],staff_status=info["staff_status"])
        # db.session.query(User).filter_by(id = info["staff_id"],name = info["name"]).update(user)
        # db.session.commit()
        user = db.session.query(User).filter_by(id=info["staff_id"], ).first()
        user.id = info["staff_id"]
        user.name = info["name"]
        user.sex = sex
        user.department = info["department"]
        user.annual_freedays = info["annual_freedays"]
        user.entry_time = info["entry_time"]
        user.staff_status = info["staff_status"]
        db.session.commit()
        return jsonify({"status": 1, "data": {}, "msg": "修改成功"})
    except:
        return jsonify({"status": 0, "data": {}, "msg": "修改失败"})


# 员工删除
@app.route('/company/deleteStaff', methods=["POST", "GET"])
def deleteStaff():
    # try:
    info = request.get_data()
    info = json.loads(info)
    # print(info)
    if "ids" in info:
        idlist = str(info["ids"]).split(",")
        print(idlist)
        for id in idlist:
            user = db.session.query(User).filter_by(id=id, ).first()
            user.company_name = None
            db.session.commit()
        return jsonify({"status": 1, "data": {}, "msg": "删除成功"})

    else:
        user = db.session.query(User).filter_by(id=info["id"], name=info["name"]).first()
        user.company_name = None
        db.session.commit()

        return jsonify({"status": 1, "data": {}, "msg": "删除成功"})


# except:
#     return jsonify({"status": 0, "data": {}, "msg": "修改失败"})

# 部门列表
@app.route('/company/getDepartment', methods=["POST", "GET"])
def getDepartment():
    try:
        info = request.get_data()
        info = json.loads(info)
        print(info, "我这里")
        if "filters" in info :
            company_name = request.json.get("company_name")
            res = db.session.query(Department).filter(and_
                  (Department.dept_name == info["filters"]["dept_name"]), Department.company_name==info["company_name"])
            # User.department == info["filters"]["department"]).limit(8).offset((info["page"] - 1) * 8)
        else:
            company_name = request.json.get("company_name")
            print(company_name)
            res = db.session.query(
                Department
            ).filter_by(
                company_name=company_name
            )
            # res = db.session.query(User).limit(8).offset((info["page"] - 1) * 8)
        # print(res)

        deplist = []
        for item in res:
            depdict = {}
            depdict["dept_id"] = (item.dept_id)
            depdict["company_name"] = (item.company_name)
            depdict["dept_name"] = (item.dept_name)
            depdict["wage_h"] = (item.wage_h)
            depdict["overtime_pay_h"] = (item.overtime_pay_h)
            depdict["s_time"] = (item.s_time.strftime('%H:%M:%S'))
            depdict["e_time"] = (item.e_time.strftime('%H:%M:%S'))
            depdict["r_time"] = (item.r_time.strftime('%H:%M:%S'))
            depdict["late_times"] = (item.late_times)
            depdict["vacation_days"] = (item.vacation_days)
            depdict["absent_times"] = (item.absent_times)
            deplist.append(depdict)
        total = db.session.query(Department).count()
        # print(deplist,total)
        return jsonify({
            "status": 1,
            "data": deplist,
            "total": total
        })
    except Exception as e:
        print(e)
        return jsonify({"status": 0, "msg": "接口异常"})


# 部门新增
@app.route('/company/addDepartment', methods=["POST", "GET"])
def addDepartment():
    info = request.get_data()
    info = json.loads(info)
    company_name = request.json.get("company_name")
    # print(company_name)
    print(info)
    from App.entity.User import Department

    Depa = db.session.query(Department).filter_by(dept_id=info["para"]["dept_id"], ).first()
    if Depa is not None:
        return jsonify({
            "status": 0,
            "msg": "该部门已经存在"
        })
    else:
        print(company_name)
        Department = Department(dept_id=info["para"]["dept_id"], dept_name=info["para"]["dept_name"], wage_h=info["para"]["wage_h"],
                                overtime_pay_h=info["para"]["overtime_pay_h"],
                                s_time=info["para"]["s_time"], e_time=info["para"]["e_time"], late_times=info["para"]["late_times"],
                                vacation_days=info["para"]["vacation_days"], company_name=company_name,
                                absent_times=info["para"]["absent_times"],
                                r_time=info["para"]["r_time"])
       # Department.company_name=request.json.get("company_name")
        db.session.add(Department)
        db.session.commit()
        return jsonify({"status": 1, "data": {}, "msg": "添加成功"})


# 部门修改
@app.route('/company/updateDepartment', methods=["POST", "GET"])
@cross_origin()
def updatedepartment():
    try:
        info = request.get_data()
        info = json.loads(info)
        print(info)
        from App.entity.User import Department

        Depa = db.session.query(Department).filter_by(dept_id=info["dept_id"], ).first()
        # print(Depa)
        Depa.dept_id = info["dept_id"]
        Depa.dept_name = info["dept_name"]
        Depa.wage_h = info["wage_h"]
        Depa.overtime_pay_h = info["overtime_pay_h"]
        Depa.s_time = info["s_time"]
        Depa.e_time = info["e_time"]
        Depa.r_time = info["r_time"]
        Depa.late_times = info["late_times"]
        Depa.vacation_days = info["vacation_days"]
        Depa.absent_times = info["absent_times"]

        db.session.commit()
        return jsonify({"status": 1, "data": {}, "msg": "修改成功"})
    except:
        return jsonify({"status": 0, "data": {}, "msg": "修改失败"})


# 部门删除
@app.route('/company/deleteDepartment', methods=["POST", "GET"])
def deletedepartment():
    try:
        info = request.get_data()
        info = json.loads(info)
        from App.entity.User import Department
        print(info)
        if "ids" in info:
            for id in info["ids"]:
                user = db.session.query(Department).filter_by(dept_id=id, ).delete()
                db.session.commit()
                return jsonify({"status": 1, "data": {}, "msg": "删除成功"})

        else:
            user = db.session.query(Department).filter_by(dept_id=info["dept_id"]).delete()
            db.session.commit()

            return jsonify({"status": 1, "data": {}, "msg": "删除成功"})
    except:
        return jsonify({"status": 0, "data": {}, "msg": "修改失败"})


# 修改公司时间
@app.route('/company/updateTime', methods=["POST", "GET"])
def updateTime():
    try:
       # company_name = request.json.get("company_name")
        info = request.get_data()
        info = json.loads(info)
        company_name = request.json.get("company_name")
        from App.entity.User import Time_Settings

        #print(company_name)
        timeset = db.session.query(Time_Settings).filter_by(company_name=company_name, ).first()

        timeset.late_period = int(info["para"]["late_period"])
        timeset.early_period = int(info["para"]["early_period"])
        #print(timeset.late_period)

        db.session.commit()
        return jsonify({"status": 1, "data": {}, "msg": "修改成功"})
    except Exception as e:
        print(str(e))
        return jsonify({"status": 0, "data": {}, "msg": "修改失败"})


# 时间设置
@app.route('/company/getTime', methods=["POST", "GET"])
def getTime():
    try:

        company_name = request.json.get("company_name")
        #print(company_name)
        recs = db.session.query(
            Time_Settings
        ).filter_by(
            company_name=company_name
        ).all()
        #print(recs)
        timelist = []
        for item in recs:
            timesetting = {}
            timesetting["late_period"] = (item.late_period)
            timesetting["early_period"] = (item.early_period)
            timelist.append(timesetting)
        return jsonify({
            "status": 1,
            "data": timelist

        })
    except Exception as e:
        print(e)
        return jsonify({"status": 0, "msg": "接口异常"})


@app.route('/company/getDepartmentName', methods=["POST", "GET"])
def getDepartmentName():
    company_name = request.values.get("company_name")
    names = db.session.query(Department.dept_name).filter_by(
        company_name=company_name
    ).distinct().all()
    if names is None or len(names) < 1:
        return {
            "status": 0,
            "msg": "该公司暂无任何部门"
        }
    results = []
    for name in names:
        # 实际上只有name[0]
        results.append(name[0])
    return {
        "status": 1,
        "data": results
    }
