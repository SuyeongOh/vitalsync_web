from fastapi import FastAPI, HTTPException, status
import sqlite3
import vital.db.user
from vital.db.user import User

userService = FastAPI()

password = "1234"


@userService.get("/login")
async def login(user_id: str):
    conn = sqlite3.connect(vital.USER_DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(vital.service.loginQuery, (user_id, password))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect id or password")
    user_in_db = cursor.fetchone()
    conn.close()
    if user_in_db:
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect id or password")


@userService.post("/register")
async def register(user: User):
    conn = sqlite3.connect(vital.USER_DB_NAME)
    cursor = conn.cursor()
    # 사용자 테이블 생성
    print('size : ' + str(cursor.arraysize))
    cursor.execute(vital.service.userTableQuery)

    print(user.user_id)
    print(user.password)
    # 사용자 추가
    cursor.execute(vital.service.userRegisterQuery, (user.user_id, user.password))

    # 변경 사항 저장하고 연결 종료
    conn.commit()
    conn.close()
