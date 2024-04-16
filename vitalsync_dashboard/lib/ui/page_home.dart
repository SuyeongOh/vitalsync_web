import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Vital Sync Dashboard'),
      ),
      body: Center(
        child: Text('메인 콘텐츠'),
      ),
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            DrawerHeader(
              child: Text('헤더'),
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
            ),
            ListTile(
              title: Text('메뉴 1'),
              onTap: () {
                Navigator.pop(context); // 사이드바 닫기
              },
            ),
            ListTile(
              title: Text('메뉴 2'),
              onTap: () {
                Navigator.pop(context); // 사이드바 닫기
              },
            ),
          ],
        ),
      ),
    );
  }
}