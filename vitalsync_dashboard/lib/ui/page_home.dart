import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/page_main.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  MainPage body = MainPage();


  @override
  Widget build(BuildContext context) {
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
