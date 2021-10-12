# 人脸数据相关 乱七八糟的
import dlib
import joblib
import numpy as np
import requests
from sklearn.metrics.pairwise import cosine_similarity

from util.GlobalVar import backendHost, rootdir

predictor_path = f'{rootdir}/model_blink_detection/shape_predictor_68_face_landmarks.dat'
face_rec_model_path = f"{rootdir}/model_face_recognition/dlib_face_recognition_resnet_model_v1.dat"
# 人脸正脸分类器
detector = dlib.get_frontal_face_detector()
# 人脸特征分类器 128维
predictor = dlib.shape_predictor(predictor_path)
# 128维向量提取
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
# 加载训练好的分类器,这个位置可能会出问题，自己调一下
svc = joblib.load(f'{rootdir}/static/expression.pkl')

# 人脸检测，img传入原图即可，返回人脸位置的rectangle数组
def getFacePosition(img):
    return detector(img, 1)


# 返回人脸数据向量
def getFaceData(img, rect):
    # 获取特征位置
    faceShape = predictor(img, rect)
    # 计算人脸的128维的向量
    face_feature = face_rec_model.compute_face_descriptor(img=img, face=faceShape)
    return list(face_feature)


# 读取人脸特征位置,筛选多余点并转化为位置比例,返回各点比例的list
def catchFaceExpressionData(image, rect):
    # 表情识别中不需要用到的特征点
    extraPoint = [7, 8, 9, 10, 11, 28, 29, 30, 31, 32, 33, 34, 35, 36]
    result = []
    x, y, w, h = rectToPosition(rect)     # x,y 是左上角
    shape = predictor(image, rect)
    # shape得到的是68个特征的绝对位置，需要排除多余点
    for i in range(68):
        try:
            extraPoint.index(i)
            continue
        except ValueError:
            # 不在extraPoint中才是正常的
            normalX = (shape.part(i).x - x) / w
            normalY = (y - shape.part(i).y) / h
            result.append(normalX)
            result.append(normalY)
    return result


# 表情识别，传入图片和人脸位置的rectangle
def recognizeExpression(image, rect):
    _expression = ''
    _data = catchFaceExpressionData(image, rect)
    if len(_data) > 0:
        _expression = svc.predict([_data])[0]
    else:
        _expression = '未识别'
    return _expression


# 获取rectangle的位置和长宽
def rectToPosition(rect):  # 获得人脸矩形的坐标信息
    _x = rect.left()
    _y = rect.top()
    _w = rect.right() - _x
    _h = rect.bottom() - _y
    return _x, _y, _w, _h


# 使用余弦相似度作为相似度判别标准,值为0-1
def getSimilarity(_face_feature1, _face_feature2):
    return cosine_similarity([_face_feature1], [_face_feature2])


# 涉及到与后端的数据交互，requests可能需要异步，暂时放这
# 提交面部数据到服务器，_face_features为矩阵类型,这里的_flag和_flag不同，只有0、1两种值，表示是要添加还是更新
def commitFaceData(_face_features, _id, _flag=0):
    shape = _face_features.shape
    shape_str = "".join(str(shape))     # 形式: m n
    requestParams = {
        'id': _id,
        'data': _face_features.tostring().decode('iso-8859-1'),
        'shape': shape_str,
        'flag': _flag
    }
    return requests.post("http://127.0.0.1:5000/user/uploadFaceData", data=requestParams).json()


# 获取面部数据，_flag_id应从本地读取,拿到面部数据后再修改本地的data、flag_id
def updateFaceData(_id, _flag_id):
    requestParams = {
        'id': _id,
        'flag_id': _flag_id
    }
    responseJson = requests.get(f"{backendHost}user/getFaceData", params=requestParams).json()
    _status = responseJson['status']
    result = [_status]
    if _status == 1:
        faceJson = responseJson['data']
        _face_features = np.fromstring(string=faceJson['data'].encode('iso-8859-1'))
        shape = tuple(eval(faceJson['shape']))
        _face_features.shape = shape    # 将行向量重新转化为矩阵原来的形状
        result.append(_face_features)   # 不确定能否存储
        result.append(faceJson['accuracy'])
        result.append(faceJson['flag_id'])
    return result   # [_status, _face_features, accuracy, flag_id]


# 本地存取矩阵,我们只会用到存储用来验证的面部数据
def localSaveMatrix(_path, _matrix):    # _path试过用face_features.npz
    np.savez(_path, face_features=_matrix)


# _matrixName 为存储时用到的名称/键 返回一个矩阵
def localReadMatrix(_path, matrixname='face_features'):
    face_features_file = np.load(_path)
    return face_features_file[matrixname]

