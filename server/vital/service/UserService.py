import json

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
    conn = sqlite3.connect(USER_DB_NAME)
    cursor = conn.cursor()
    # 사용자 테이블 생성
    print('size : ' + str(cursor.arraysize))
    cursor.execute(userTableQuery)

    cursor.execute(userCheckQuery, (user.user_id))
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


@userService.get("/vital/data/vital")
async def getData(user_id: str):
    db = sqlite3.connect(DATA_DB_NAME)
    cursor = db.cursor()
    db.execute(server.vital.service.dataLoadQuery, (user_id,))
    data = cursor.fetchall()

    return json.dumps(data)


@userService.get("/vital/data/signal")
async def getPpgSignal(user_id: str):
    db = sqlite3.connect(DATA_DB_NAME)
    cursor = db.cursor()
    db.execute(server.vital.service.signalLoadQuery, (user_id,))
    data = cursor.fetchall()

    return json.dumps(data)


@userService.get("/vital/data/gt")
def getGT(user_id: str):
    db = sqlite3.connect(DATA_DB_NAME)
    cursor = db.cursor()
    cursor.execute(gtLoadQuery, (user_id,))
    data = cursor.fetchall()

    return json.dumps(data)
