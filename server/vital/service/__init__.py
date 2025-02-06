dataSaveQuery = '''INSERT INTO VitalSigns
                  (UserID, hr, ibi_hr, hrv, rr, spo2, stress, bp, sbp, dbp, MeasurementTime)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

dataLoadQuery = '''SELECT * FROM VitalSigns WHERE UserID = ?'''

signalSaveQuery = '''INSERT INTO VitalSignal
                  (UserID, ppg, r_signal, g_signal, b_signal, MeasurementTime)
                  VALUES (?, ?, ?, ?, ?, ?)'''

signalLoadQuery = '''SELECT * FROM VitalSignal WHERE UserID = ?'''

signalWithTimeLoadQuery = '''SELECT * FROM VitalSignal WHERE UserID = ? AND MeasurementTime = ?'''


gtSaveQuery = '''INSERT INTO GroundTruth
                  (UserID, ppg, r_signal, g_signal, b_signal, MeasurementTime)
                  VALUES (?, ?, ?, ?, ?, ?)'''

gtLoadQuery = '''SELECT * FROM GroundTruth WHERE UserID = ?'''

loginQuery = "SELECT * FROM users WHERE user_id = ? AND password = ?"

userListQuery = '''SELECT * FROM users'''

userTableQuery = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id TEXT, password TEXT)"
userRegisterQuery = "INSERT INTO users (user_id, password) VALUES (?, ?)"
userCheckQuery = "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = ?)"
