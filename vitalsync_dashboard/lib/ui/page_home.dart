import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/page_main.dart';
import 'package:vitalsync_dashboard/database/http.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  MainPage body = MainPage();


  @override
  Widget build(BuildContext context) {
    MainPageState bodyState = body.getState();
    return Scaffold(
      appBar: AppBar(
        title: Text('Vital Sync Dashboard'),
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
                Navigator.pop(context);
                fetchUsers();
                bodyState.selectPage(0);
              },
            ),
            ListTile(
              title: Text('Data'),
              onTap: () {
                Navigator.pop(context);
                bodyState.selectPage(1);
              },
            ),
          ],
        ),
      ),
    );
  }
}
