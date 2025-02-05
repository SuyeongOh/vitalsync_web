import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/page_main.dart';
import 'package:vitalsync_dashboard/ui/page_userlist.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Widget body = MainPage();

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
              title: Text('User List'),
              onTap: () {
                setState(() {
                  body = UserListPage();
                });
                Navigator.pop(context);
              },
            ),
            ListTile(
              title: Text('Data'),
              onTap: () {
                Navigator.pushNamed(context, "/user/data");
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
    );
  }
}
