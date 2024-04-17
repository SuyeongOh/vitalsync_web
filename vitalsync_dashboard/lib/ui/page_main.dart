import 'package:flutter/material.dart';

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
    if(!isInitialize){
      createState();

    }
    return _state;
  }
}

class MainPageState extends State<MainPage> {
  int _selectedPageIndex = 0;

  // 각 페이지에 대한 위젯 리스트
  final List<Widget> _pages = [
    Center(child: Text('User Page')),
    Center(child: Text('Chart Page')),
    Center(child: Text('Settings Page')),
  ];

  void selectPage(int index) {
    setState(() {
      _selectedPageIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    return _pages[_selectedPageIndex];
  }
}