import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:vitalsync_dashboard/config.dart';
import 'package:vitalsync_dashboard/database/user_data.dart';
import 'package:vitalsync_dashboard/database/users_data.dart';

String BASE_URL = "http://35.220.206.239:3000/";

Future<List<UsersData>> fetchUsers() async {
  String api = "user/list";
  final response = await http.get(Uri.parse(BASE_URL + api));
  if (response.statusCode == 200) {
    List<dynamic> dataJson = jsonDecode(response.body);
    List<UsersData> userList = dataJson.map((data) => UsersData.fromJson(data)).toList();
    Config.instance.users = userList;
    return userList;
  } else {
    throw Exception('Failed to load data');
  }
}

Future<List<UserData>> fetchUserData(String user_id) async {
  String api = "vital/data/vital";
  final response = await http.get(Uri.parse("$BASE_URL$api?user_id=$user_id"));

  if(response.statusCode == 200){
    List<dynamic> dataJson = jsonDecode(response.body);
    List<UserData> userData = dataJson.map((data) => UserData.fromJson(data)).toList();

    Config.instance.userData = userData;

    return userData;
  } else{
    throw Exception(response.body);
  }
}



