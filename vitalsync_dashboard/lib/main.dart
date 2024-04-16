import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/page_home.dart';

void main() {
  runApp(const VitalSyncDashBoard());
}

class VitalSyncDashBoard extends StatelessWidget {
  const VitalSyncDashBoard({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Vital Sync Dashboard',
      home: HomePage(),
    );
  }
}