import json
import struct

from fastapi import FastAPI, HTTPException, status
import sqlite3
import server.vital.db.user
from server.vital.db.user import User
from server.vital.service import *
from server.vital import *

userService = FastAPI()

password = "1234"

@userService.get("/login")
async def login(user_id: str):
    conn = sqlite3.connect(server.vital.USER_DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(server.vital.service.loginQuery, (user_id, password))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error LoginQuery")
    user_in_db = cursor.fetchone()
    conn.close()
    if user_in_db:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect id or password")


@userService.post("/register")
async def register(user: User):
    conn = sqlite3.connect(server.vital.USER_DB_NAME)
    cursor = conn.cursor()
    # 사용자 테이블 생성
    print('size : ' + str(cursor.arraysize))
    cursor.execute(userTableQuery)

    cursor.execute(userCheckQuery, (user.user_id,))
    result = cursor.fetchone()[0]
    if result > 0:
        return {"message": "user_id already exists"}

    print(user.user_id)
    print(user.password)
    # 사용자 추가
    cursor.execute(userRegisterQuery, (user.user_id, user.password))

    # 변경 사항 저장하고 연결 종료
    conn.commit()
    conn.close()

    return {"message": "register successful"}


@userService.get("/user/list")
async def getUsers():
    db = sqlite3.connect(server.vital.USER_DB_NAME)
    cursor = db.cursor()

    cursor.execute(userListQuery)

    data = cursor.fetchall()
    fields = [description[0] for description in cursor.description]

    jsonData = []
    for e in data:
        parseData = {}
        for field, value in zip(fields, e):
            parseData[field] = value
        jsonData.append(parseData)
    return jsonData


@userService.get("/vital/data/vital")
async def getData(user_id: str):
    db = sqlite3.connect(DATA_DB_NAME)
    cursor = db.cursor()

    cursor.execute(dataLoadQuery, (user_id,))

    data = cursor.fetchall()
    fields = [description[0] for description in cursor.description]

    jsonData = []
    for e in data:
        parseData = {}
        for field, value in zip(fields, e):
            parseData[field] = value
        jsonData.append(parseData)
    return jsonData


@userService.get("/vital/data/signal")
async def getPpgSignal(user_id: str):
    db = sqlite3.connect(DATA_DB_NAME)
    cursor = db.cursor()

    cursor.execute(signalLoadQuery, (user_id,))

    data = cursor.fetchall()
    fields = [description[0] for description in cursor.description]
    print(fields)
    jsonData = []
    for e in data:
        parseData = {}
        for field, value in zip(fields, e):
            if(field == 'ppg'
                    or field == 'r_signal'
                    or field == 'g_signal'
                    or field == 'b_signal'):
                parseData[field] = blob_to_floatlist(value)
            parseData[field] = value
        jsonData.append(parseData)

    #TODO blob -> float array issue 해결

    return jsonData




@userService.get("/vital/data/gt")
def getGT(user_id: str):
    db = sqlite3.connect(DATA_DB_NAME)
    cursor = db.cursor()

    cursor.execute(gtLoadQuery, (user_id,))
    data = cursor.fetchall()
    fields = [description[0] for description in cursor.description]

    jsonData = []
    for e in data:
        parseData = {}
        for field, value in zip(fields, e):
            parseData[field] = value
        jsonData.append(parseData)
    return jsonData


def blob_to_floatlist(blob_data):
    unit_size = 4
    float_array = []

    for i in range(0, len(blob_data), unit_size):
        binary_data = blob_data[i:i + unit_size]

        float_value = struct.unpack('f', binary_data)[0]
        float_array.append(float_value)

    return float_array
