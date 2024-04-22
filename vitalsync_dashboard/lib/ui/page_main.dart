import 'dart:js';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/body_data.dart';
import 'package:vitalsync_dashboard/ui/body_user.dart';

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

  UserBody userBody = UserBody();
  DataBody dataBody = DataBody();

  void selectPage(int index) {
    setState(() {
      _selectedPageIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    // 각 페이지에 대한 위젯 리스트
    UserBodyState userState = userBody.getState();
    DataBodyState dataState = dataBody.getState();

    final List<Widget> _pages = [
      Center(child: userState.build(context)),
      Center(child: dataState.build(context)),
      Center(child: Text('Settings Page')),
    ];

    return _pages[_selectedPageIndex];
  }
}

