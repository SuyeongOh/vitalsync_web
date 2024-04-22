import 'package:vitalsync_dashboard/database/user_data.dart';

import 'database/users_data.dart';

class Config{
  List<UsersData> users = [];
  List<UserData> userData = [];
  static Config instance = Config();

}