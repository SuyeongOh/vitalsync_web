import 'package:flutter/material.dart';
import 'page_signal.dart';
import '../../database/user_data.dart';
import '../../service/http_service.dart';

class UserHistoryPage extends StatefulWidget {
  final String userID;

  UserHistoryPage({required this.userID});

  @override
  _UserHistoryPageState createState() => _UserHistoryPageState();
}

class _UserHistoryPageState extends State<UserHistoryPage> {
  late Future<List<UserData>> futureUserData;
  List<UserData> allUserData = [];
  List<UserData> paginatedUserData = [];

  int currentPage = 0;
  static const int pageSize = 10; // 한 페이지당 10개씩 표시

  @override
  void initState() {
    super.initState();
    futureUserData = fetchUserData(widget.userID);
    fetchUserData(widget.userID).then((data) {
      data.sort((a, b) => b.measurementTime.compareTo(a.measurementTime));

      setState(() {
        allUserData = data;
        paginatedUserData = getPaginatedData();
      });
    });
  }

  List<UserData> getPaginatedData() {
    int startIndex = currentPage * pageSize;
    int endIndex = (startIndex + pageSize).clamp(0, allUserData.length);
    return allUserData.sublist(startIndex, endIndex);
  }

  void nextPage() {
    if ((currentPage + 1) * pageSize < allUserData.length) {
      setState(() {
        currentPage++;
        paginatedUserData = getPaginatedData();
      });
    }
  }

  void prevPage() {
    if (currentPage > 0) {
      setState(() {
        currentPage--;
        paginatedUserData = getPaginatedData();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("${widget.userID}'s Measurement History")),
      body: FutureBuilder<List<UserData>>(
        future: futureUserData,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          } else if (snapshot.hasError) {
            return Center(child: Text("Error: ${snapshot.error}"));
          } else if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return Center(child: Text("No data found for ${widget.userID}"));
          }

          return Column(
            children: [
              // 데이터 리스트뷰
              Expanded(
                child: ListView.builder(
                  itemCount: paginatedUserData.length,
                  itemBuilder: (context, index) {
                    UserData data = paginatedUserData[index];
                    return GestureDetector(
                      onTap: () {
                        Navigator.push(context,
                            MaterialPageRoute(
                              builder: (context) => SignalDataPage(
                                userID: data.userID,
                                measurementTime: data.measurementTime,
                              ),
                            )
                        );
                      },
                      child: Card(
                        margin: EdgeInsets.symmetric(vertical: 6, horizontal: 16),
                        child: Padding(
                          padding: EdgeInsets.all(8.0),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              // 측정 시간 (왼쪽 정렬)
                              Text(
                                UserData.TimeTommddHH(data.measurementTime),
                                style: TextStyle(fontSize: 14, fontWeight: FontWeight.bold),
                              ),
                              SizedBox(width: 10),

                              // 데이터 값 (오른쪽 정렬)
                              Expanded(
                                child: SingleChildScrollView(
                                  scrollDirection: Axis.horizontal,
                                  child: Row(
                                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                                    children: [
                                      dataCell("HR", data.hr),
                                      dataCell("HRV", data.hrv),
                                      dataCell("RR", data.rr),
                                      dataCell("SpO2", data.spo2),
                                      dataCell("Stress", data.stress),
                                      dataCell("BP", data.bp),
                                      dataCell("IBI_HR", data.ibiHr),
                                    ],
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    );
                  },
                ),
              ),

              // 페이지네이션 버튼
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
                      "Page ${currentPage + 1} / ${((allUserData.length / pageSize).ceil()).clamp(1, double.infinity).toInt()}",
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
          );
        },
      ),
    );
  }

  // 데이터 셀 (각 데이터 값을 나타내는 위젯)
  Widget dataCell(String label, double value) {
    return Container(
      width: 70,
      padding: EdgeInsets.symmetric(vertical: 4, horizontal: 8),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey.shade300),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        children: [
          Text(label, style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
          Text(value.toStringAsFixed(1), style: TextStyle(fontSize: 14)),
        ],
      ),
    );
  }
}
