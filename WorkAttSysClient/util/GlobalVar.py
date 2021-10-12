import os
import sys
import pymysql

# 生产环境
backendHost = "http://127.0.0.1:5000/"

# 存储新的申请信息
NEW_APP = {
    'app_str': '',
    'app_date': ''
}
# APP_ID[0]当前申请类别,APP_ID[1]申请是否成功
APP_ID = [0, 0]
# 全局变量
rootdir = os.getcwd()
# 摄像头ID
CAMERA_ID = 0
# 默认采集人脸数量
COLLENCT_FACE_NUM_DEFAULT = 3
# 人脸识别提示信息
CHECK_IN_NOTE = {
    'if_blink': 0,
    'check_status': True,
    'check_time': ''
}
# 存储登录状态,当前登录用户基本信息
LOGIN_STATUS = [0, 0]
LOCAL_USER = {'id': '',
              'name': '',
              'pwd': '',
              'phone': '',
              'sex': '',
              'company': '',
              'head_img': '',
              'department': '',
              'annual_freedays': '',
              'flag': 0,
              'if_face': False
              }

# 多少次循环保存一帧图像
LOOP_FRAME = 20

# 初始化循环次数，比如统计20帧中人脸的数量，取最大值进行考勤
FR_LOOP_NUM = 20

# button字体文件
BTN_FONT = f'{rootdir}/util/btn_font.OTF'


# 将execute文件所在目录添加到根目录
def add_path_to_sys():
    rootdir = os.getcwd()
    sys.path.append(rootdir)
    return rootdir


# 连接数据库操作
def connect_to_sql():
    db = pymysql.connect(host="localhost", user="", password="", database="")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    return db, cursor


# 遍历人脸数据文件夹，并统计各人脸的图片数量
def statical_facedata_nums():
    # 人脸数据文件夹根目录
    files_dir = f"{rootdir}/face_dataset/"
    # print(os.listdir(files_dir))

    dirs = os.listdir(files_dir)
    # 初始化字典
    files_num_dict = dict(zip(dirs, [0] * len(dirs)))

    for dir in dirs:
        for file in os.listdir(files_dir + dir):
            # $表示匹配结尾
            # if re.match(r'.*\.jpg$', file) or re.match(r'.*\.png$', file):
            if file.endswith('.jpg') or file.endswith('.png'):
                files_num_dict[dir] += 1

    return files_num_dict


print(os.path.basename(__file__))

if __name__ == '__main__':
    files = statical_facedata_nums()
    print(files)
