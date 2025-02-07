import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:vitalsync_dashboard/config.dart';
import 'package:vitalsync_dashboard/database/user_data.dart';
import 'package:vitalsync_dashboard/database/user_list_data.dart';

import '../database/user_signal_data.dart';

String BASE_URL = "http://35.220.206.239:3000/";

Future<List<UserListData>> fetchUserList() async {
  String api = "user/list";
  final response = await http.get(Uri.parse(BASE_URL + api));
  if (response.statusCode == 200) {
    List<dynamic> dataJson = jsonDecode(response.body);
    List<UserListData> userList =
        dataJson.map((data) => UserListData.fromJson(data)).toList();
    Config.instance.users = userList;
    return userList;
  } else {
    throw Exception('Failed to load data');
  }
}

Future<List<UserData>> fetchUserData(String user_id) async {
  String api = "vital/data/vital";
  final response = await http.get(Uri.parse("$BASE_URL$api?user_id=$user_id"));

  if (response.statusCode == 200) {
    List<dynamic> dataJson = jsonDecode(response.body);
    List<UserData> userData =
        dataJson.map((data) => UserData.fromJson(data)).toList();

    Config.instance.userData = userData;

    return userData;
  } else {
    throw Exception(response.body);
  }
}

Future<bool> registerUser({
  required String userId,
  required String password,
  required String name,
  required String email,
}) async {
  Map<String, dynamic> userData = {
    "user_id": userId,
    "password": password,
    "name": name,
    "email": email,
  };

  String api = "/register";
  final response = await http.post(
    Uri.parse("$BASE_URL$api"),
    headers: {"Content-Type": "application/json"},
    body: jsonEncode(userData),
  );

  if (response.statusCode == 201) {
    return true; // 회원가입 성공
  } else {
    return false; // 회원가입 실패
  }
}

Future<UserSignalData> fetchUserSignalData(String user_id) async {
  String api = "vital/data/signal";
  final response = await http.get(Uri.parse("$BASE_URL$api?user_id=$user_id"));

  if (response.statusCode == 200) {
    Map<String, dynamic> dataJson = jsonDecode(response.body);

    UserSignalData userSignalData = UserSignalData.fromJson(dataJson);
    userSignalData.setUserId(user_id);

    Config.instance.signalData = userSignalData;
    return userSignalData;
  } else {
    throw Exception("Failed to load data: ${response.body}");
  }
}

Future<UserSignalUnitData> fetchUserSignalDataWithTime(String user_id, String measurementTime) async {
  String api = "vital/data/signal_time";
  final response = await http.get(Uri.parse("$BASE_URL$api?user_id=$user_id&measurementTime=$measurementTime"));

  if (response.statusCode == 200) {
    dynamic dataJson = jsonDecode(response.body);

    if (dataJson.isNotEmpty){
      UserSignalUnitData userSignalData = UserSignalUnitData.fromJson(dataJson);
      return userSignalData;
    }
    throw Exception("No data found for $user_id at $measurementTime");

  } else {
    throw Exception("Failed to load data: ${response.body}");
  }
}