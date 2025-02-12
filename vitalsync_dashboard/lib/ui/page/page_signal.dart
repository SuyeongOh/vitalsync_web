import 'dart:async';
import 'dart:math';

import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import '../../database/user_signal_data.dart'; // UserSignalData 클래스 추가
import '../../service/http_service.dart';

class SignalDataPage extends StatefulWidget {
  final String userID;
  final String measurementTime;

  SignalDataPage({required this.userID, required this.measurementTime});

  @override
  _SignalDataPageState createState() => _SignalDataPageState();
}

class _SignalDataPageState extends State<SignalDataPage> {
  late Future<UserSignalUnitData> signalData;
  Map<String, bool> selectedData = {}; // 체크된 데이터 목록
  Map<String, Color> dataColors = {}; // 데이터별 색상 매핑

  double maxY = 255;
  double minY = 0;

  double maxPpg = 5;
  double minPpg = -5;

  @override
  void initState() {
    super.initState();
    initializeDataSelection();
    signalData = fetchUserSignalDataWithTime(widget.userID, widget.measurementTime);
  }

  void initializeDataSelection() {
    List<String> labels = UserSignalUnitData.getDataLabels();
    List<Color> colors = [Colors.cyan, Colors.red, Colors.green, Colors.blue];

    for (int i = 0; i < labels.length; i++) {
      selectedData[labels[i]] = false; // 기본값 false로 설정
      dataColors[labels[i]] = colors[i % colors.length]; // 색상 매핑
    }
  }

  List<double> normalizePpgData(List<double> data) {
    return data.map((ppgValue) {
      return minY + ((ppgValue - minPpg) / (maxPpg - minPpg)) * (maxY - minY);
    }).toList();
  }

  void updateRangeY(UserSignalUnitData signalData) {
    List<double> selectedValues = selectedData.entries
        .where((entry) => entry.value) // ppg 제외한 값만 사용
        .expand((entry) => getSignalData(signalData, entry.key))
        .toList();

    if (selectedData['ppg'] ?? false) {
      double minValue = signalData.ppg.reduce(min);
      double maxValue = signalData.ppg.reduce(max);
      double range = (maxValue - minValue) * 0.05;

      setState(() {
        minPpg = (minValue - range);
        maxPpg = (maxValue + range);
      });
    }

    if (selectedValues.isNotEmpty) {
      double minValue = selectedValues.reduce(min);
      double maxValue = selectedValues.reduce(max);
      double range = (maxValue - minValue) * 0.05;

      setState(() {
        minY = (minValue - range);
        maxY = (maxValue + range);
      });
    } else {
      setState(() {
        minY = 0;
        maxY = 255;
      });
    }
  }

  @override
  Widget build(BuildContext context) {

    return Scaffold(
      appBar: AppBar(title: Text("${widget.userID}'s Signal Data Graph")),
      body: FutureBuilder<UserSignalUnitData>(
        future: signalData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData) {
            return Center(child: Text("No data found for ${widget.userID}"));
          }

          UserSignalUnitData signalData = snapshot.data!;

          return Column(
            children: [
              // 체크박스 리스트 (신호 선택)
              Container(
                margin: EdgeInsets.symmetric(horizontal: 10),
                height: 50,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: selectedData.length,
                  itemBuilder: (context, index) {
                    String label = selectedData.keys.elementAt(index);
                    return Row(children: [
                      Checkbox(
                        value: selectedData[label],
                        activeColor: dataColors[label], // 체크박스 색상 적용
                        onChanged: (bool? value) {
                          setState(() {
                            selectedData[label] = value ?? false;
                          });
                          updateRangeY(signalData); // 선택된 데이터 기반으로 min/max 업데이트
                        },
                      ),
                      Text(label.toUpperCase(), style: TextStyle(fontSize: 16)),
                      SizedBox(width: 10)
                    ]);
                  },
                ),
              ),

              // 그래프 표시
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: LineChart(
                    LineChartData(
                      minY: minY, // minY 조정
                      maxY: maxY, // maxY 조정
                      titlesData: FlTitlesData(
                        rightTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true, //
                            reservedSize: 50, //
                            interval: (maxY - minY) / 20,
                            getTitlesWidget: (value, meta) {
                              if (meta.max == value) {
                                return Padding(
                                  padding: EdgeInsets.fromLTRB(0, 0, 8, 20),
                                  child: Text(
                                    "COLOR",  //
                                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.black),
                                    textAlign: TextAlign.left,
                                  ),
                                );
                              }
                              return Padding(
                                padding: EdgeInsets.only(left: 8),
                                child: Text(
                                  value.toInt().toString(), //
                                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold), //
                                  textAlign: TextAlign.left, //
                                ),
                              );
                            },
                          ),
                        ),
                        leftTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true, // selectedData['ppg'] ?? false, // ppg 체크 시만 Y축 레이블 표시
                            reservedSize: 50, // Y축 공간 확보
                            getTitlesWidget: (value, meta) {
                              double mappedValue = minPpg + ((value - minY) / (maxY - minY)) * (maxPpg - minPpg);

                              if (meta.max == value) {
                                return Padding(
                                  padding: EdgeInsets.fromLTRB(8, 0, 0, 16),
                                  child: Text(
                                    "PPG",
                                    style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.black),
                                    textAlign: TextAlign.right,
                                  ),
                                );
                              }
                              return Padding(
                                padding: EdgeInsets.only(right: 8),
                                child: Text(
                                  mappedValue.toStringAsFixed(3),
                                  style: TextStyle(
                                    fontSize: 12,
                                    fontWeight: FontWeight.bold,
                                    color: selectedData['ppg'] ?? false ? Colors.black : Colors.transparent, // 선택적으로 값 보이게
                                  ),
                                  textAlign: TextAlign.right,
                                ),
                              );
                            },
                          ),
                        ),
                        topTitles: AxisTitles(
                          sideTitles: SideTitles(showTitles: false), // X축 숨김
                        ),
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            reservedSize: 30,
                            getTitlesWidget: (value, meta) {
                              return Padding(
                                padding: EdgeInsets.only(top: 8),
                                child: Text(
                                  value.toInt().toString(),
                                  style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold),
                                  textAlign: TextAlign.center,
                                ),
                              );
                            },
                          ),
                        ),
                      ),
                      lineBarsData: selectedData.entries
                          .where((entry) => entry.value) // 체크된 데이터만 그래프에 반영
                          .map((selectedEntry) {
                        return LineChartBarData(
                          spots: getSignalData(signalData, selectedEntry.key)
                              .asMap()
                              .entries
                              .map((entry) => FlSpot(entry.key.toDouble(), entry.value))
                              .toList(),
                          isCurved: false,
                          color: dataColors[selectedEntry.key],
                          barWidth: 5,
                          dotData: FlDotData(show: true),
                        );
                      }).toList(),
                    ),
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }

  // 선택한 신호 데이터 반환
  List<double> getSignalData(UserSignalUnitData data, String label) {
    switch (label) {
      case 'ppg':
        return normalizePpgData(data.ppg);
      case 'r_signal':
        return data.r_signal;
      case 'g_signal':
        return data.g_signal;
      case 'b_signal':
        return data.b_signal;
      default:
        return [];
    }
  }
}
