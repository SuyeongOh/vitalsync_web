import 'package:flutter/material.dart';
import 'package:vitalsync_dashboard/ui/page/page_data.dart'; // Graph 페이지
import 'package:vitalsync_dashboard/ui/page/page_history.dart';
import '../../database/user_list_data.dart';
import '../../service/http_service.dart';

class UserListPage extends StatefulWidget {
  @override
  _UserListPageState createState() => _UserListPageState();
}

class _UserListPageState extends State<UserListPage> {
  late Future<List<UserListData>> futureUsers;
  List<UserListData> allUsers = []; // 전체 사용자 목록
  List<UserListData> filteredUsers = []; // 검색된 사용자 목록
  TextEditingController searchController = TextEditingController();

  int currentPage = 0;
  static const int pageSize = 10;

  @override
  void initState() {
    super.initState();
    fetchUserList().then((users) {
      setState(() {
        allUsers = users;
        filteredUsers = users;
      });
    });
  }

  void filterSearchResults(String query) {
    setState(() {
      filteredUsers = allUsers.where((user) {
        return user.user_id.toLowerCase().contains(query.toLowerCase());
      }).toList();
    });
  }

  List<UserListData> getPaginatedUsers() {
    int startIndex = currentPage * pageSize;
    int endIndex = startIndex + pageSize;
    return filteredUsers.sublist(startIndex, endIndex.clamp(0, filteredUsers.length));
  }

  void nextPage() {
    if ((currentPage + 1) * pageSize < filteredUsers.length) {
      setState(() {
        currentPage++;
      });
    }
  }

  void prevPage() {
    if (currentPage > 0) {
      setState(() {
        currentPage--;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    List<UserListData> displayedUsers = getPaginatedUsers();

    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Text(
              "User List",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            SizedBox(width: 50),
            Flexible(
              child: Container(
                width: 400,
                height: 40,
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(8),
                ),
                child: TextField(
                  controller: searchController,
                  decoration: InputDecoration(
                    hintText: "Search User ID...",
                    prefixIcon: Icon(Icons.search, color: Colors.grey),
                    border: InputBorder.none,
                    contentPadding: EdgeInsets.symmetric(vertical: 10),
                  ),
                  onChanged: filterSearchResults,
                ),
              ),
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              itemCount: displayedUsers.length,
              itemBuilder: (context, index) {
                return Card(
                  margin: EdgeInsets.symmetric(vertical: 6, horizontal: 16),
                  child: ListTile(
                    leading: CircleAvatar(child: Text(displayedUsers[index].user_id[0])),
                    title: Text(displayedUsers[index].user_id),
                    subtitle: Text(displayedUsers[index].name),
                    trailing: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        // History 버튼
                        ElevatedButton.icon(
                          icon: Icon(Icons.history, size: 18),
                          label: Text("History"),
                          style: ElevatedButton.styleFrom(
                            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            textStyle: TextStyle(fontSize: 12),
                          ),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => UserHistoryPage(userID: displayedUsers[index].user_id),
                              ),
                            );
                          },
                        ),
                        SizedBox(width: 8),
                        // Graph 버튼
                        ElevatedButton.icon(
                          icon: Icon(Icons.show_chart, size: 18),
                          label: Text("Graph"),
                          style: ElevatedButton.styleFrom(
                            padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                            textStyle: TextStyle(fontSize: 12),
                          ),
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => DataPage(userID: displayedUsers[index].user_id),
                              ),
                            );
                          },
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(vertical: 8),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton(
                  onPressed: prevPage,
                  child: Text("Prev"),
                ),
                Text(
                  "Page ${currentPage + 1} / ${((filteredUsers.length / pageSize).ceil()).clamp(1, double.infinity).toInt()}",
                  style: TextStyle(fontSize: 14),
                ),
                ElevatedButton(
                  onPressed: nextPage,
                  child: Text("Next"),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
