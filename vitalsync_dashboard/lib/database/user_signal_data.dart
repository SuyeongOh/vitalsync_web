class UserSignalUnitData{
  final List<double> ppg;
  final List<double> r_signal;
  final List<double> g_signal;
  final List<double> b_signal;
  final String measurementTime;

  UserSignalUnitData({
    required this.ppg,
    required this.r_signal,
    required this.g_signal,
    required this.b_signal,
    required this.measurementTime,
  });

  factory UserSignalUnitData.fromJson(Map<String, dynamic> json) {
    return UserSignalUnitData(
      ppg: List<double>.from(json['ppg'].map((e) => e.toDouble())),
      r_signal: List<double>.from(json['r_signal'].map((e) => e.toDouble())),
      g_signal: List<double>.from(json['g_signal'].map((e) => e.toDouble())),
      b_signal: List<double>.from(json['b_signal'].map((e) => e.toDouble())),
      measurementTime: json['MeasurementTime'],
    );
  }

  static List<String> getDataLabels(){
    List<String> labels = [
      'ppg',
      'r_signal',
      'g_signal',
      'b_signal',
    ];
    return labels;
  }
}

class UserSignalData {
  final List<UserSignalUnitData> data;
  late String user_id;
  UserSignalData({
    required this.data,
  });

  factory UserSignalData.fromJson(Map<String, dynamic> json) {
    return UserSignalData(
      data: (json['data'] as List)
          .map((e) => UserSignalUnitData.fromJson(e))
          .toList(),
    );
  }

  void setUserId(String userId){
    user_id = userId;
  }

}
