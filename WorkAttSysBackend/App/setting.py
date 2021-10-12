DIALCT = "mysql"
DRIVER = "pymysql"
USERNAME = "root"
PASSWORD = "root"
HOST = "119.3.234.38"
PORT = "3306"
DATABASE = "WorkAttSys"
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALCT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
