import 'package:vitalsync_dashboard/database/user_data.dart';
import 'package:vitalsync_dashboard/database/user_list_data.dart';
import 'package:vitalsync_dashboard/database/user_signal_data.dart';


class Config{
  List<UserListData> users = [];
  List<UserData> userData = [];
  List<UserSignalData> signalData = [];
  static Config instance = Config();

}