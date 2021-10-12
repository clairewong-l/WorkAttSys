from App import app, db
from flask import request

from App.entity.User import UserFace
from App.util.httpUtil import serialize


@app.route('/user/uploadFaceData', methods=["POST"])
def uploadFaceData():
    _id = request.values.get("id")
    _data = request.values.get("data")
    print(_data)
    print(type(_data))
    shape = request.values.get("shape")
    flag = request.values.get("flag")
    accuracy = 0.96
    flag_id = 0
    print(flag)
    if flag is None or flag == '0':
        new_data = UserFace(id=_id, data=_data.encode('iso-8859-1'), shape=shape, accuracy=accuracy, flag_id=flag_id)
        db.session.add(new_data)
        db.session.commit()
    else:
        old_data = db.session.query(UserFace).filter_by(id=_id).first()
        old_data._data = _data.encode('iso-8859-1')
        print(old_data._data)
        old_data.shape = shape
        old_data.accuracy -= 0.01
        old_data.flag_id += 1
        accuracy = old_data.accuracy
        flag_id = old_data.flag_id
        db.session.commit()
    return{
        "status": 1,
        "data": {
            "accuracy": accuracy,
            "flag_id": flag_id
        }
    }


@app.route('/user/getFaceData', methods=["POST", "GET"])
def getFaceData():
    _id = request.values.get("id")
    print(request)
    _flag_id = request.values.get("flag_id")
    print(_id)
    print(_flag_id)
    old_data = db.session.query(UserFace).filter_by(id=_id).first()
    if old_data is None:
        print("old_data is None")
        return {
            "status": -1,
            "msg": "更新失败，请重新上传面部数据"
        }
    if _flag_id is None or old_data.flag_id != _flag_id:
        _dict = {
            'data': old_data.data.decode('iso-8859-1'),
            'shape': old_data.shape,
            'accuracy': old_data.accuracy,
            'flag_id': old_data.flag_id
        }
        return {
            "status": 1,
            "data": _dict
        }
    else:
        return {
            "status": 0,
            "msg": "已是最新数据"
        }
