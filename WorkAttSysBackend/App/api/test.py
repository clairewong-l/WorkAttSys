#coding=utf-8
import numpy as np
from sqlalchemy import cast, Date, TIMESTAMP, DateTime, String, BIGINT, func, and_
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from App import app, db
from flask import request

from App.entity.User import User, Msg_Record, Department, Time_Settings, Att_Record, Att_Application, \
    Company_Application, \
    Vacation_Application, Back_Application, Out_Application, UserFace

import time
import datetime

if __name__ == '__main__':
    print(datetime.datetime.now())
