import 'package:flutter/material.dart';

void main() {
  runApp(const VitalSyncDashBoard());
}

class VitalSyncDashBoard extends StatelessWidget {
  const VitalSyncDashBoard({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "Vital Sync Info Center",
      home:
        Scaffold(appBar: AppBar(
              elevation: 0,
              backgroundColor: Colors.transparent,
              title: Text("Vital Sync Info Center")
          ),
        )
    );
  }
}