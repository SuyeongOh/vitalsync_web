import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

import '../database/user_data.dart';
import '../service/http_service.dart';

class DataPage extends StatefulWidget {
  final String userID; // 특정 사용자 ID

  DataPage({required this.userID});

  @override
  _DataPageState createState() => _DataPageState();
}

class _DataPageState extends State<DataPage> {
  late Future<List<UserData>> futureUserData;
  String selectedLabel = "hr"; // 초기 선택 데이터 (심박수)

  @override
  void initState() {
    super.initState();
    futureUserData = fetchUserData(widget.userID);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("User Data Graph (${widget.userID})")),
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
              // 데이터 선택 드롭다운
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: DropdownButton<String>(
                  value: selectedLabel,
                  items: UserData.getDataLabels().map((label) {
                    return DropdownMenuItem(value: label, child: Text(label.toUpperCase()));
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      selectedLabel = value!;
                    });
                  },
                ),
              ),

              // 그래프 표시
              Expanded(
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: LineChart(
                    LineChartData(
                      titlesData: FlTitlesData(
                        leftTitles: AxisTitles(
                          sideTitles: SideTitles(showTitles: true),
                        ),
                        bottomTitles: AxisTitles(
                          sideTitles: SideTitles(
                            showTitles: true,
                            getTitlesWidget: (value, meta) {
                              int index = value.toInt();
                              if (index < userData.length) {
                                return Text(UserData.TimeTommddHH(userData[index].measurementTime),
                                    style: TextStyle(fontSize: 10));
                              }
                              return Text('');
                            },
                            reservedSize: 22,
                          ),
                        ),
                      ),
                      lineBarsData: [
                        LineChartBarData(
                          spots: UserData.getDataList(userData, selectedLabel)
                              .asMap()
                              .entries
                              .map((entry) => FlSpot(entry.key.toDouble(), entry.value))
                              .toList(),
                          isCurved: true,
                          color: Colors.blue,
                          barWidth: 3,
                          dotData: FlDotData(show: false),
                        ),
                      ],
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
}