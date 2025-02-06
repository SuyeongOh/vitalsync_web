class UserSignalData {
  final List<double> ppg;
  final List<double> r_signal;
  final List<double> g_signal;
  final List<double> b_signal;

  UserSignalData({
    required this.ppg,
    required this.r_signal,
    required this.g_signal,
    required this.b_signal,
  });

  factory UserSignalData.fromJson(Map<String, dynamic> json) {
    return UserSignalData(
      ppg: json['ppg'].map((data) => data.toDouble()).toList(),
      r_signal: json['r_signal'].map((data) => data.toDouble()).toList(),
      g_signal: json['g_signal'].map((data) => data.toDouble()).toList(),
      b_signal: json['b_signal'].map((data) => data.toDouble()).toList(),
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