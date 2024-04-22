class UsersData {
  int id;
  String user_id;
  String password;

  UsersData({required this.id, required this.user_id, required this.password});

  factory UsersData.fromJson(Map<String, dynamic> json) {
    return UsersData(
      user_id: json['user_id'],
      id: json['id'],
      password: json['password'],
    );
  }
}

