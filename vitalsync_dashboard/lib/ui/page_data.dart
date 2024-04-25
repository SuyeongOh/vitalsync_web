import 'package:fl_chart/fl_chart.dart';
import 'package:flutter/material.dart';

import '../config.dart';
import '../database/http.dart';
import '../database/user_data.dart';
import '../database/users_data.dart';

class DataPage extends StatefulWidget {
  late _DataPageState _state;
  bool isInitialize = false;

  @override
  State<StatefulWidget> createState() {
    _state = _DataPageState();
    isInitialize = true;
    return _state;
  }

  _DataPageState getState() {
    if (!isInitialize) {
      createState();
    }
    return _state;
  }
}

class _DataPageState extends State<DataPage> {
  late List<double> chartData = [];
  late List<FlSpot> chartDataSpot = [];

  UsersData? selectedUser = null;
  String? selectedUserId = null;
  String? selectedVitalSign = null;

  @override
  Widget build(BuildContext context) {
    Widget body = FutureBuilder(
        future: fetchUsers(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Text('');
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else if (snapshot.hasData) {
            final List<UsersData> usersData = snapshot.requireData;
            List<String> userIdList = usersData.map((e) => e.user_id).toList();
            return Container(
                alignment: Alignment.topLeft,
                padding: EdgeInsets.fromLTRB(50, 10, 50, 0),
                child: Column(
                  children: [
                    Row(
                      children: [
                        DropdownButton<String>(
                          value: selectedUserId ?? userIdList[0],
                          onChanged: (newValue) {
                            setState(() {
                              if (newValue == null) return;
                              selectedUserId = newValue;
                            });
                          },
                          items: userIdList
                              .map<DropdownMenuItem<String>>((String user_id) {
                            return DropdownMenuItem<String>(
                              value: user_id,
                              child: Text(user_id),
                            );
                          }).toList(),
                        ),
                        Container(
                          margin: EdgeInsets.fromLTRB(20, 0, 0, 0),
                          child: DropdownButton<String>(
                            value: selectedVitalSign ??
                                UserData.getDataLabels()[0],
                            onChanged: (label) {
                              setState(() {
                                if (label == null) return;
                                selectedVitalSign = label;
                              });
                            },
                            items: UserData.getDataLabels()
                                .map<DropdownMenuItem<String>>((String label) {
                              return DropdownMenuItem<String>(
                                value: label,
                                child: Text(label),
                              );
                            }).toList()),
                        ),
                      ],
                    ),
                    FutureBuilder(
                        future: fetchUserData(selectedUserId ?? userIdList[0]),
                        builder: (context, snapshot) {
                          if (snapshot.connectionState ==
                              ConnectionState.waiting) {
                            return CircularProgressIndicator();
                          } else if (snapshot.hasError) {
                            return Text('Error: ${snapshot.error}');
                          } else if (snapshot.hasData) {
                            chartData = UserData.getDataList(
                                Config.instance.userData,
                                selectedVitalSign ??
                                    UserData.getDataLabels()[0]);
                            chartDataSpot.clear();
                            double startIdx = 1;
                            if(chartData.length > 10){
                              startIdx = chartData.length - 10;
                            }
                            for (double i = startIdx; i <= chartData.length; i++) {
                              chartDataSpot
                                  .add(FlSpot(i, chartData[i.toInt() - 1]));
                            }
                            return Expanded(
                              child: LineChart(LineChartData(
                                  gridData: FlGridData(show: false),
                                  titlesData: FlTitlesData(
                                      show: true,
                                      topTitles: AxisTitles(
                                        sideTitles: SideTitles(showTitles: false)
                                      ),
                                      bottomTitles: AxisTitles(
                                        axisNameWidget: Text(
                                            (selectedUserId ?? userIdList[0]) + "\'s "
                                                + (selectedVitalSign ?? UserData.getDataLabels()[0])),
                                        sideTitles: SideTitles(
                                            showTitles: true,
                                            reservedSize: 30,
                                            interval: 1,
                                            getTitlesWidget: (value, meta) {
                                              return Text(
                                                UserData.getMeasureTime(Config
                                                    .instance
                                                    .userData)[value.toInt()-1],
                                                textAlign: TextAlign.right,
                                                style: TextStyle(
                                                    fontSize: 12,
                                                    letterSpacing: 0),
                                              );
                                            }
                                        ),
                                      )
                                      ),
                                  borderData: FlBorderData(show: true),
                                  lineBarsData: [
                                    LineChartBarData(
                                      spots: chartDataSpot,
                                      isCurved: false,
                                      color: Colors.blue,
                                      barWidth: 5,
                                      isStrokeCapRound: true,
                                      dotData: FlDotData(show: true),
                                    ),
                                  ]),
                            ));
                          } else {
                            return Text('No data available : ' +
                                (selectedUserId ?? userIdList[0]));
                          }
                        })
                  ],
                ));
          } else {
            return Text('No data available');
          }
        });

    return Scaffold(
      appBar: AppBar(
        title: Text('Data Display'),
      ),
      body: body,
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            DrawerHeader(
              child: Text('Menu'),
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
            ),
            ListTile(
              title: Text('Users'),
              onTap: () {
                Navigator.pushNamed(context, "/user/list");
              },
            ),
            ListTile(
              title: Text('Data'),
              onTap: () {
                Navigator.pushNamed(context, "/user/data");
              },
            ),
          ],
        ),
      ),
    );
  }
}
