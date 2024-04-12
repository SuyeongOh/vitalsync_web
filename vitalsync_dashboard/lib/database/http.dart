import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:vitalsync_dashboard/database/user_data.dart';

Future<List<UserData>> fetchData(String userId) async {
  final response = await http.get(Uri.parse('YOUR_DATABASE_API_ENDPOINT?userId=$userId'));
  if (response.statusCode == 200) {
    List<dynamic> dataJson = jsonDecode(response.body);
    return dataJson.map((data) => UserData.fromJson(data)).toList();
  } else {
    throw Exception('Failed to load data');
  }
}
