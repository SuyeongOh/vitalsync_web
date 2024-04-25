class UserData {
  final int vitalSignID;
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
  final String measurementTime;

  UserData({
    required this.vitalSignID,
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
    required this.measurementTime,
  });

  factory UserData.fromJson(Map<String, dynamic> json) {
    return UserData(
      vitalSignID: json['VitalSignID'],
      userID: json['UserID'],
      hr: json['hr'].toDouble(),
      ibiHr: json['ibi_hr'].toDouble(),
      hrv: json['hrv'].toDouble(),
      rr: json['rr'].toDouble(),
      spo2: json['spo2'].toDouble(),
      stress: json['stress'].toDouble(),
      bp: json['bp'].toDouble(),
      sbp: json['sbp'].toDouble(),
      dbp: json['dbp'].toDouble(),
      measurementTime: json['MeasurementTime'],
    );
  }

  static List<String> getDataLabels(){
    List<String> labels = [
      'hr',
      'hrv',
      'rr',
      'spo2',
      'stress',
      'bp',
      'ibi_hr'
    ];
    return labels;
  }

  static List<double> getDataList(List<UserData> dataList, String label){
    switch(label) {
      case 'hr':
        return dataList.map((data) => data.hr).toList();
      case 'hrv':
        return dataList.map((data) => data.hrv).toList();
      case 'rr':
        return dataList.map((data) => data.rr).toList();
      case 'spo2':
        return dataList.map((data) => data.spo2).toList();
      case 'stress':
        return dataList.map((data) => data.stress).toList();
      case 'bp':
        return dataList.map((data) => data.hr).toList();
      case 'ibi_hr':
        return dataList.map((data) => data.ibiHr).toList();
      default:
        return [];
    }
  }

  static List<String> getMeasureTime(List<UserData> dataList){
    return dataList.map((data) => TimeTommddHH(data.measurementTime)).toList();
  }

  static String TimeTommddHH(String time){
    String month = time.substring(4, 6);
    String day = time.substring(6, 8);
    String hour = time.substring(8, 10);
    String min = time.substring(10, 12);
    return "$month.$day.$hour:$min";
  }
}
