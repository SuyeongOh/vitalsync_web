import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

import '../database/http.dart';
import '../database/users_data.dart';

class UserPage extends StatefulWidget {
  late _UserPageState _state;
  bool isInitialize = false;

  @override
  State<StatefulWidget> createState() {
    _state = _UserPageState();
    isInitialize = true;
    return _state;
  }

  _UserPageState getState() {
    if (!isInitialize) {
      createState();
    }
    return _state;
  }
}

class _UserPageState extends State<UserPage> {
  @override
  Widget build(BuildContext context) {
    Widget body = FutureBuilder(
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
                      .map((userId) => DataRow(
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

    return Scaffold(
      appBar: AppBar(
        title: Text('User List'),
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
