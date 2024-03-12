dataSaveQuery = '''INSERT INTO VitalSigns
                  (UserID, hr, hrv, rr, spo2, stress, sbp, dbp, MeasurementTime)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''

signalSaveQuery = '''INSERT INTO VitalSignal
                  (UserID, ppg, MeasurementTime)
                  VALUES (?, ?, ?)'''

loginQuery = "SELECT * FROM users WHERE id = ? AND password = ?"

userTableQuery = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id TEXT, password TEXT)"
userRegisterQuery = "INSERT INTO users (user_id, password) VALUES (?, ?)"
