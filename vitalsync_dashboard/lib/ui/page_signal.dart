import 'dart:async';
import 'dart:math';

import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import '../database/user_signal_data.dart'; // UserSignalData 클래스 추가
import '../service/http_service.dart';

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

  int minY = 0;
  int maxY = 255;

  @override
  void initState() {
    super.initState();
    initializeDataSelection();

    signalData =
        fetchUserSignalDataWithTime(widget.userID, widget.measurementTime);
  }

  void initializeDataSelection() {
    List<String> labels = UserSignalUnitData.getDataLabels();
    List<Color> colors = [Colors.black, Colors.red, Colors.green, Colors.blue];

    for (int i = 0; i < labels.length; i++) {
      selectedData[labels[i]] = false; // 기본값 false로 설정
      dataColors[labels[i]] = colors[i % colors.length]; // 색상 매핑
    }
  }

  void updateRangeY(UserSignalUnitData signalData) {
    List<double> selectedValues = selectedData.entries
        .where((entry) => entry.value) // 체크된 항목만 필터링
        .expand((entry) => getSignalData(signalData, entry.key)) // 데이터 가져오기
        .toList();

    if (selectedValues.isNotEmpty) {
      double minValue = selectedValues.reduce((a, b) => a < b ? a : b);
      double maxValue = selectedValues.reduce((a, b) => a > b ? a : b);
      double range = (maxValue - minValue) * 0.05;

      setState(() {
        minY = (minValue - range).floor();
        maxY = (maxValue + range).ceil();
      });
    } else {
      setState(() {
        minY = -255; // 기본값으로 초기화
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
                          updateRangeY(signalData); // 선택된 데이터 기반으로 minY 업데이트
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
                      minY: minY - 1, // 데이터 최소값 설정
                      maxY: maxY + 1, // 데이터 최대값 설정
                      titlesData: FlTitlesData(
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: false, // X축 타이틀 숨김
                          ),
                        ),
                        leftTitles: AxisTitles(
                          sideTitles: SideTitles(showTitles: true), // Y축 타이틀 표시
                        ),
                      ),
                      lineBarsData: selectedData.entries
                          .where((entry) => entry.value) // 체크된 데이터만 그래프에 반영
                          .map((selectedEntry) {
                        return LineChartBarData(
                          spots: getSignalData(signalData, selectedEntry.key)
                              .asMap()
                              .entries
                              .map((entry) =>
                                  FlSpot(entry.key.toDouble(), entry.value))
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

              // 그래프 색상 가이드 (범례)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 10),
                child: Wrap(
                  spacing: 10,
                  children: selectedData.keys
                      .where((key) => selectedData[key]!) // 체크된 데이터만 표시
                      .map((label) {
                    return Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Container(
                          width: 12,
                          height: 12,
                          decoration: BoxDecoration(
                            color: dataColors[label],
                            shape: BoxShape.circle,
                          ),
                        ),
                        SizedBox(width: 5),
                        Text(label.toUpperCase(),
                            style: TextStyle(fontSize: 12)),
                      ],
                    );
                  }).toList(),
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
        return data.ppg;
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
