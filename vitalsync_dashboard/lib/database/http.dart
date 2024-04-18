import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:vitalsync_dashboard/database/user_data.dart';

String BASE_URL = "http://35.220.206.239:3000/";

Future<List<UserData>> fetchUsers() async {
  String api = "user/list";
  final response = await http.get(Uri.parse(BASE_URL + api));
  if (response.statusCode == 200) {
    print("response body : " + response.body);
    List<dynamic> dataJson = jsonDecode(response.body);
    return dataJson.map((data) => UserData.fromJson(data)).toList();
  } else {
    throw Exception('Failed to load data');
  }
}
