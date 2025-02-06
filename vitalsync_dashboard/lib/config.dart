import 'package:vitalsync_dashboard/database/user_data.dart';
import 'package:vitalsync_dashboard/database/user_list_data.dart';


class Config{
  List<UserListData> users = [];
  List<UserData> userData = [];
  static Config instance = Config();

}