import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../../database/user_data.dart';
import '../../service/http_service.dart';

class DataPage extends StatefulWidget {
  final String userID; // 특정 사용자 ID

  DataPage({required this.userID});

  @override
  _DataPageState createState() => _DataPageState();
}

class _DataPageState extends State<DataPage> {
  late Future<List<UserData>> futureUserData;
  List<String> dataLabels = UserData.getDataLabels(); // 데이터 레이블 목록
  Map<String, bool> selectedData = {}; // 체크된 데이터 목록
  Map<String, Color> dataColors = {}; // 데이터별 색상 매핑

  @override
  void initState() {
    super.initState();
    futureUserData = fetchUserData(widget.userID);
    initializeDataSelection();
  }

  // 초기 선택값 및 색상 설정
  void initializeDataSelection() {
    List<Color> colors = [
      Colors.blue,
      Colors.red,
      Colors.green,
      Colors.orange,
      Colors.purple,
      Colors.cyan,
      Colors.teal
    ];

    for (int i = 0; i < dataLabels.length; i++) {
      selectedData[dataLabels[i]] = false; // 기본값 false로 설정
      dataColors[dataLabels[i]] = colors[i % colors.length]; // 색상 매핑
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("${widget.userID}'s Health Data Graph")),
      body: FutureBuilder<List<UserData>>(
        future: futureUserData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text("No data found for ${widget.userID}"));
          }

          List<UserData> userData = snapshot.data!;

          return Column(
            children: [
              Container(
                margin: EdgeInsets.symmetric(horizontal: 10),
                height: 50,
                child: ListView.builder(
                  scrollDirection: Axis.horizontal,
                  itemCount: dataLabels.length,
                  itemBuilder: (context, index) {
                    String label = dataLabels[index];
                    return Row(children: [
                      Checkbox(
                        value: selectedData[label],
                        activeColor: dataColors[label], // 체크박스 색상 적용
                        onChanged: (bool? value) {
                          setState(() {
                            if (value != null) {
                              selectedData[label] = value;
                            }
                          });
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
                      minY: 0,
                      maxY: 200,
                      titlesData: FlTitlesData(
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            getTitlesWidget: (value, meta) {
                              int index = value.toInt();
                              if (index < userData.length) {
                                return Text(
                                    UserData.TimeTommddHH(
                                        userData[index].measurementTime),
                                    style: TextStyle(fontSize: 10));
                              }
                              return Text('');
                            },
                            reservedSize: 22,
                          ),
                        ),
                      ),
                      lineBarsData: selectedData.entries
                          .where((entry) => entry.value)
                          .map((selectedEntry) { // ✅ 변수명 명확하게 변경
                        return LineChartBarData(
                          spots: UserData.getDataList(userData, selectedEntry.key)
                              .asMap()
                              .entries
                              .map((entry) => FlSpot(entry.key.toDouble(), entry.value))
                              .toList(),
                          isCurved: true,
                          color: dataColors[selectedEntry.key],
                          barWidth: 3,
                          dotData: FlDotData(show: false),
                        );
                      }).toList(),
                    ),
                  ),
                ),
              ),

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
}
