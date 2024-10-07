import pickle
import sqlite3
import io
import urllib
from http.client import responses

import aiosqlite
import numpy as np
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
import time

import server.vital
from server.vital.db.ground_truth import GtRequest, GtResponse
from server.vital.db.polar import PolarRequest, PolarResponse
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
            vitalResponse.ibi_hr,
            vitalResponse.hrv,
            vitalResponse.rr,
            vitalResponse.spo2,
            vitalResponse.stress,
            vitalResponse.bp,
            vitalResponse.sbp,
            vitalResponse.dbp,
            currentTime
        ))

        # 변경 사항 저장
        await db.commit()


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


# MongoDB에 연결
# 데이터베이스와 컬렉션 선택
username = urllib.parse.quote_plus('admin')
password = urllib.parse.quote_plus('1234')
client = MongoClient('mongodb://%s:%s@localhost:27017/' % (username, password))
db = client['user']
collection = db['polar_verity']


def savePolarSignal(polar_request: PolarRequest):
    # 데이터 생성 (string ID, Array<float> signal, long measurementTime)
    data = {
        "id": polar_request.id,  # string 타입 ID
        "measurementTime": polar_request.measurementTime  # long 타입 measurementTime (유닉스 타임스탬프)
    }

    if polar_request.ecg_signal:
        data["ecg"] = polar_request.ecg_signal  # float 배열 (Array<float>)

    if polar_request.ppg_signal:
        data["ppg"] = polar_request.ppg_signal  # float 배열 (Array<float>)

    response = PolarResponse()
    # 데이터 삽입
    try:
        collection.insert_one(data)
        print("데이터가 성공적으로 저장되었습니다.")
        response.status = 200
        response.message = "saving Polar Data success"
    except Exception as e:
        response.status = 200
        response.message = "Error 발생 !!"
        print(f"데이터 삽입 중 오류 발생: {e}")
    return response


def saveGt(ground_truth: GtRequest):
    try:
        # SQLite 데이터베이스 연결
        conn = sqlite3.connect(server.vital.DATA_DB_NAME)
        cursor = conn.cursor()

        # GroundTruth 테이블 생성
        cursor.execute("CREATE TABLE IF NOT EXISTS GroundTruth ("
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

        # 데이터 삽입
        cursor.execute("INSERT INTO GroundTruth (UserID, hr, hrv, rr, spo2, stress, sbp, dbp, MeasurementTime) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       (ground_truth.id, ground_truth.hr, ground_truth.hrv, ground_truth.rr,
                        ground_truth.spo2, ground_truth.stress, ground_truth.sbp, ground_truth.dbp,
                        ground_truth.measureTime))

        # 변경 사항 저장 및 연결 종료
        conn.commit()
        conn.close()
        response = GtResponse()
        response.status = 200
        response.message = "saving ground truth success"
        return response

    except:
        response = GtResponse()
        response.status = 500
        response.message = "internal error saving ground truth "
        return response


def get_current_time_str():
    # 현재 시간을 datetime 객체로 가져옵니다.
    now = datetime.now()
    # strftime 메소드를 사용하여 원하는 형식의 문자열로 변환합니다.
    time_str = now.strftime('%Y%m%d%H%M')
    return time_str
