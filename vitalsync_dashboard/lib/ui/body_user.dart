import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../database/http.dart';
import '../database/users_data.dart';

class UserBody extends StatefulWidget{
  late UserBodyState _state;
  bool isInitialize = false;

  @override
  State<StatefulWidget> createState() {
    _state = UserBodyState();
    isInitialize = true;
    return _state;
  }

  UserBodyState getState(){
    if (!isInitialize) {
      createState();
    }
    return _state;
  }
}

class UserBodyState extends State<UserBody> {
  @override
  Widget build(BuildContext context) {
    return FutureBuilder(
        future: fetchUsers(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return CircularProgressIndicator();
          } else if (snapshot.hasError) {
            return Text('Error: ${snapshot.error}');
          } else if (snapshot.hasData) {
            List<UsersData> userIds = snapshot.requireData;
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
                      .map((userId) =>
                      DataRow(
                        cells: [
                          DataCell(Text(userId.user_id)),
                        ],
                      ))
                      .toList(),
                ),
              ),
            );
          } else {
            return Text('No data available');
          }
        });
  }

}