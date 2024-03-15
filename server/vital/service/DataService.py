import pickle
import sqlite3
import io
import aiosqlite
import numpy as np
from datetime import datetime

import server.vital
from server.vital.db.ground_truth import GtRequest
from server.vital.db.vital import VitalResponse


async def saveData(user: str, vitalResponse: VitalResponse, currentTime: str):
    async with aiosqlite.connect(server.vital.DATA_DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS VitalSigns ("
                         "VitalSignID INTEGER PRIMARY KEY,"
                         "UserID TEXT,"
                         "hr DOUBLE,"
                         "ibi_hr DOUBLE,"
                         "hrv DOUBLE,"
                         "rr DOUBLE,"
                         "spo2 DOUBLE,"
                         "stress DOUBLE,"
                         "bp DOUBLE,"
                         "sbp DOUBLE,"
                         "dbp DOUBLE,"
                         "MeasurementTime VARCHAR(14),"
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


async def getData(user: str):
    async with aiosqlite.connect(server.vital.DATA_DB_NAME) as db:
        cursor = await db.cursor()
        await db.execute(server.vital.service.dataLoadQuery, (user,))
        data = await cursor.fetchall()

        return data


# ppg : ndarray
async def savePpgSignal(user: str, ppg, r: list[float], g: list[float], b: list[float], currentTime: str):
    async with aiosqlite.connect(server.vital.DATA_DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS VitalSignal ("
                         "VitalSignalID INTEGER PRIMARY KEY,"
                         "UserID TEXT,"
                         "ppg BLOB,"
                         "r_signal BLOB,"
                         "g_signal BLOB,"
                         "b_signal BLOB,"
                         "MeasurementTime VARCHAR(14),"
                         "FOREIGN KEY (UserID) REFERENCES users(user_id)"
                         ")")

        # 사용자 추가
        await db.execute(server.vital.service.signalSaveQuery, (
            user,
            ppg,
            pickle.dumps(r),
            pickle.dumps(g),
            pickle.dumps(b),
            currentTime
        ))

        # 변경 사항 저장
        await db.commit()


async def getPpgSignal(user: str):
    async with aiosqlite.connect(server.vital.DATA_DB_NAME) as db:
        cursor = await db.cursor()
        await db.execute(server.vital.service.signalLoadQuery, (user,))
        data = await cursor.fetchall()

        return data


async def saveGt(ground_truth: GtRequest):
    async with aiosqlite.connect(server.vital.DATA_DB_NAME) as db:
        await db.execute("CREATE TABLE IF NOT EXISTS GroundTruth ("
                         "GroundTruthID INTEGER PRIMARY KEY,"
                         "UserID TEXT,"
                         "hr DOUBLE,"
                         "hrv DOUBLE,"
                         "rr DOUBLE,"
                         "spo2 DOUBLE,"
                         "stress DOUBLE,"
                         "sbp DOUBLE,"
                         "dbp DOUBLE,"
                         "MeasurementTime VARCHAR(14),"
                         "FOREIGN KEY (UserID) REFERENCES users(user_id)"
                         ")")

        # 사용자 추가
        await db.execute(server.vital.service.gtSaveQuery, (
            ground_truth.id,
            ground_truth.hr,
            ground_truth.hrv,
            ground_truth.rr,
            ground_truth.spo2,
            ground_truth.stress,
            ground_truth.sbp,
            ground_truth.dbp,
            ground_truth.measureTime
        ))

        # 변경 사항 저장
        await db.commit()


async def getGt(user: str):
    async with aiosqlite.connect(server.vital.DATA_DB_NAME) as db:
        cursor = await db.cursor()
        await db.execute(server.vital.service.gtLoadQuery, (user,))
        data = await cursor.fetchall()

        return data


def get_current_time_str():
    # 현재 시간을 datetime 객체로 가져옵니다.
    now = datetime.now()
    # strftime 메소드를 사용하여 원하는 형식의 문자열로 변환합니다.
    time_str = now.strftime('%Y%m%d%H%M')
    return time_str
