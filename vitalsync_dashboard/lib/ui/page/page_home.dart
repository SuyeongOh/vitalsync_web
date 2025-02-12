import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/page/page_opendata.dart';
import 'page_main.dart';
import 'page_userlist.dart';
import 'page_register.dart';

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
              title: Text('Register'),
              onTap: () {
                setState(() {
                  body = RegisterPage();
                });
                Navigator.pop(context);
              },
            ),
            ListTile(
              title: Text('Test open data'),
              onTap: () {
                setState(() {
                  body = OpenDataPage();
                });
                Navigator.pop(context);
              },
            ),
          ],
        ),
      ),
    );
  }
}
