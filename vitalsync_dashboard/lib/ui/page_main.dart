import 'dart:js';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/database/http.dart';
import 'package:vitalsync_dashboard/database/users_data.dart';
import 'package:vitalsync_dashboard/ui/body_data.dart';
import 'package:vitalsync_dashboard/ui/body_user.dart';

import '../database/user_data.dart';

// Router로 userbody, databody 이동.
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
  List<UserData> userData = [];

  final UserBody userBody = UserBody();
  final DataBody dataBody = DataBody(
    onUserCallback: (UsersData data) {
      FutureBuilder(future: fetchUserData(data.user_id),
          builder: (context, snapshot) {
            if(snapshot.hasData){

            }
          });
    },
  );



  void selectPage(int index) {
    setState(() {
      _selectedPageIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    // 각 페이지에 대한 위젯 리스트
    final UserBodyState userState = userBody.getState();
    final DataBodyState dataState = dataBody.getState();

    final List<Widget> _pages = [
      Center(child: userState.build(context)),
      dataState.build(context),
      Center(child: Text('Settings Page')),
    ];

    return _pages[_selectedPageIndex];
  }
}
