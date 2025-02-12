import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/page/page_home.dart';
import 'package:vitalsync_dashboard/ui/page/page_userlist.dart';


void main() {
  runApp(const VitalSyncDashBoard());
}

class VitalSyncDashBoard extends StatelessWidget {
  const VitalSyncDashBoard({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vital Sync Dashboard',
      initialRoute: '/',
      routes: {
        '/' : (context) => HomePage(),
        '/user/list' : (context) => UserListPage(),
        //'/user/data' : (context) => DataPage(userID: userID)
      },
    );
  }
}