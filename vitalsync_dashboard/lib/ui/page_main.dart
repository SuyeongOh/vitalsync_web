import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class MainPage extends StatefulWidget {
  late MainPageState _state;
  bool isInitialize = false;

  @override
  MainPageState createState() {
    _state = MainPageState();
    isInitialize = true;
    return _state;
  }

  MainPageState getState() {
    if (!isInitialize) {
      createState();
    }
    return _state;
  }
}

class MainPageState extends State<MainPage> {
  int _selectedPageIndex = 0;

  // 각 페이지에 대한 위젯 리스트
  final List<Widget> _pages = [
    Center(child: userBody()),
    Center(child: dataBody()),
    Center(child: Text('Settings Page')),
  ];

  void selectPage(int index) {
    setState(() {
      _selectedPageIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return _pages[_selectedPageIndex];
  }
}

Widget userBody(String test) {
  final List<String> userIds = ['User123', 'User456', 'User789', 'User101'];
  return Container(
    alignment: Alignment.topCenter,
    child: SingleChildScrollView(
      scrollDirection: Axis.vertical,
      padding: EdgeInsets.fromLTRB(50, 10, 50, 0),
      child: DataTable(
        columns: const [
          DataColumn(label: Text('User ID')),
        ],
        rows: userIds
            .map((userId) => DataRow(
                  cells: [
                    DataCell(Text(userId)),
                  ],
                ))
            .toList(),
      ),
    ),
  );
}

Widget dataBody() {
  final List<double> chartData = [70, 75, 80, 85];
  List<FlSpot> chartDataSpot = [];
  for (double i = 1; i <= chartData.length; i++) {
    chartDataSpot.add(FlSpot(i, chartData[i.toInt() - 1]));
  }
  return Container(
    alignment: Alignment.topLeft,
    padding: EdgeInsets.fromLTRB(50, 10, 50, 0),
    child: Column(
      children: [
        const Text("Hello"),
        Expanded(
          child: LineChart(LineChartData(
              gridData: FlGridData(show: true),
              titlesData: FlTitlesData(show: true),
              borderData: FlBorderData(show: true),
              lineBarsData: [
                LineChartBarData(
                  spots: chartDataSpot,
                  isCurved: true,
                  color: Colors.blue,
                  barWidth: 5,
                  isStrokeCapRound: true,
                  dotData: FlDotData(show: true),
                ),
              ])),
        )
      ]
    )
  );
}
