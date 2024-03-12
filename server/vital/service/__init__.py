dataSaveQuery = '''INSERT INTO VitalSigns
                  (UserID, hr, ibi_hr, hrv, rr, spo2, stress, sbp, dbp, MeasurementTime)
                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

dataLoadQuery = '''SELECT INTO VitalSigns WHERE UserID = ?'''

signalSaveQuery = '''INSERT INTO VitalSignal
                  (UserID, ppg, r, g, b, MeasurementTime)
                  VALUES (?, ?, ?, ?, ?, ?)'''

signalLoadQuery = '''SELECT * FROM VitalSignal WHERE UserID = ?'''

loginQuery = "SELECT * FROM users WHERE id = ? AND password = ?"

userTableQuery = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_id TEXT, password TEXT)"
userRegisterQuery = "INSERT INTO users (user_id, password) VALUES (?, ?)"
