class UserListData {
  final int id;
  final String user_id;
  final String password;
  final String name;
  final String email;

  UserListData({
    required this.id,
    required this.user_id,
    required this.password,
    required this.name,
    required this.email,
  });

  factory UserListData.fromJson(Map<String, dynamic> json) {
    return UserListData(
      id: json['id'],
      user_id: json['user_id'],
      password: json['password'],
      name: json['name'] ?? "",
      email: json['email'] ?? "",
    );
  }

}