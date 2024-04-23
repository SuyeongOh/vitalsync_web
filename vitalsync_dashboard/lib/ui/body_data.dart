import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

import '../database/http.dart';
import '../database/user_data.dart';
import '../database/users_data.dart';

class DataBody extends StatefulWidget{
  late DataBodyState _state;
  bool isInitialize = false;
  final Function(UsersData) onUserCallback;

  DataBody({
    Key? key,
    required this.onUserCallback
  }) : super(key: key);
  @override
  State<StatefulWidget> createState() {
    _state = DataBodyState();
    isInitialize = true;
    return _state;
  }

  DataBodyState getState(){
    if(!isInitialize){
      createState();
    }
    return _state;
  }
}

class DataBodyState extends State<DataBody> {
  late List<double> chartData = [];
  late List<FlSpot> chartDataSpot = [];
  @override
  Widget build(BuildContext context) {
    chartData = [70, 75, 80, 85]; // 이 부분은 선택된 사용자에 따라 변경될 수 있습니다.
    for (double i = 1; i <= chartData.length; i++) {
      chartDataSpot.add(FlSpot(i, chartData[i.toInt() - 1]));
    }

    return FutureBuilder(
        future: fetchUsers(),
        builder: (context, snapshot) {
          final List<UsersData> usersData = snapshot.requireData;
          UsersData selectedUser = usersData[0];
          String selectedUserId = selectedUser.user_id;
          if (snapshot.connectionState == ConnectionState.waiting) {
            return CircularProgressIndicator();
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else if (snapshot.hasData) {
            return Container(
                alignment: Alignment.topLeft,
                padding: EdgeInsets.fromLTRB(50, 10, 50, 0),
                child: Column(
                  children: [
                    DropdownButton<UsersData>(
                      value: selectedUser,
                      onChanged: (newValue) {
                        // 여기서 선택된 사용자에 따라 chartData를 업데이트할 수 있습니다.
                        print("On Change Target User");
                        setState(() {
                          if (newValue == null) return;
                          selectedUser = newValue;
                          selectedUserId = newValue.user_id;
                        });
                      },
                      items: usersData
                          .map<DropdownMenuItem<UsersData>>((UsersData user) {
                        return DropdownMenuItem<UsersData>(
                          value: user,
                          child: Text(user.user_id),
                        );
                      }).toList(),
                    ),
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
                  ],
                ));
          } else {
            return Text('No data available');
          }
        });
  }

  void setLineData(UserData data){

  }
}