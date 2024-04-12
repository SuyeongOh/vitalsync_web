class UserData {
  final String userID;
  final double hr;
  final double ibiHr;
  final double hrv;
  final double rr;
  final double spo2;
  final double stress;
  final double bp;
  final double sbp;
  final double dbp;

  UserData({
    required this.userID,
    required this.hr,
    required this.ibiHr,
    required this.hrv,
    required this.rr,
    required this.spo2,
    required this.stress,
    required this.bp,
    required this.sbp,
    required this.dbp,
  });

  factory UserData.fromJson(Map<String, dynamic> json) {
    return UserData(
      userID: json['UserID'],
      hr: json['hr'],
      ibiHr: json['ibi_hr'],
      hrv: json['hrv'],
      rr: json['rr'],
      spo2: json['spo2'],
      stress: json['stress'],
      bp: json['bp'],
      sbp: json['sbp'],
      dbp: json['dbp'],
    );
  }
}
