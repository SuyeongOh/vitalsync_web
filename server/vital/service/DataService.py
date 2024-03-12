import sqlite3
import aiosqlite
from datetime import datetime

import server.vital
from server.vital.service.models import VitalResponse


async def saveData(user: str, vitalResponse: VitalResponse, currentTime: str):
    async with aiosqlite.connect(server.vital.DATA_DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS VitalSigns ("
                         "VitalSignID INTEGER PRIMARY KEY,"
                         "UserID TEXT,"
                         "hr DOUBLE,"
                         "hrv DOUBLE,"
                         "rr DOUBLE,"
                         "spo2 DOUBLE,"
                         "stress DOUBLE,"
                         "bp DOUBLE,"
                         "sbp DOUBLE,"
                         "dbp DOUBLE,"
                         "MeasurementTime VARCHAR(12),"
                         "FOREIGN KEY (UserID) REFERENCES users(user_id)"
                         ")")

        # 사용자 추가
        await db.execute(server.vital.service.dataSaveQuery, (
            user,
            vitalResponse.hr,
            vitalResponse.hrv,
            vitalResponse.rr,
            vitalResponse.spo2,
            vitalResponse.stress,
            vitalResponse.sbp,
            vitalResponse.dbp,
            currentTime
        ))

        # 변경 사항 저장
        await db.commit()


# ppg : ndarray
async def savePpgSignal(user: str, ppg, currentTime: str):
    async with aiosqlite.connect(server.vital.PPG_DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS VitalSignal ("
                         "VitalSignalID INTEGER PRIMARY KEY,"
                         "UserID TEXT,"
                         "ppg BLOB"
                         "MeasurementTime VARCHAR(12),"
                         "FOREIGN KEY (UserID) REFERENCES users(user_id)"
                         ")")

        # 사용자 추가
        await db.execute(server.vital.service.dataSaveQuery, (
            user,
            ppg,
            currentTime
        ))

        # 변경 사항 저장
        await db.commit()


def get_current_time_str():
    # 현재 시간을 datetime 객체로 가져옵니다.
    now = datetime.now()
    # strftime 메소드를 사용하여 원하는 형식의 문자열로 변환합니다.
    time_str = now.strftime('%Y%m%d%H%M')
    return time_str
