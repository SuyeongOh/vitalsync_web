import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:vitalsync_dashboard/config.dart';

class OpenDataPage extends StatefulWidget {
  @override
  _OpenDataPageState createState() => _OpenDataPageState();
}

class _OpenDataPageState extends State<OpenDataPage> {
  String selectedDataset = "UBFC"; // 기본 선택값
  String? videoFileName;
  String? annotationFileName;

  // 파일 선택 함수
  Future<void> pickFile(String datasetType, bool isVideo) async {
    String datasetExtension = OpenDatasetInputExtension[datasetType]![0];
    String labelExtension = OpenDatasetInputExtension[datasetType]![1];

    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: isVideo ? [datasetExtension] : [labelExtension],
    );

    if (result != null) {
      setState(() {
        if (isVideo) {
          videoFileName = result.files.single.name;
        } else {
          annotationFileName = result.files.single.name;
        }
      });
    }
  }

  void _showManualDialog() {
    showDialog(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: Text("사용자 메뉴얼"),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text("1. 데이터셋 유형 선택 (UBFC / PURE)"),
              Text("2. 비디오 파일 업로드"),
              Text("3. 어노테이션 파일 업로드"),
              Text("4. 시작 버튼을 눌러 데이터 처리"),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: Text("닫기"),
            ),
          ],
        );
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Open Data Page"),
        actions: [
          IconButton(
            icon: Icon(Icons.help_outline),
            onPressed: _showManualDialog,
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text("Select Dataset Type:", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            DropdownButton<String>(
              value: selectedDataset,
              items: ["UBFC", "PURE"].map((dataset) {
                return DropdownMenuItem<String>(
                  value: dataset,
                  child: Text(dataset),
                );
              }).toList(),
              onChanged: (value) {
                setState(() {
                  selectedDataset = value!;
                });
              },
            ),

            SizedBox(height: 20),

            Text("Upload Video File:", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            ElevatedButton.icon(
              icon: Icon(Icons.video_library),
              label: Text("Select Video"),
              onPressed: () => pickFile(selectedDataset, true),
            ),
            if (videoFileName != null) Text("Selected: $videoFileName", style: TextStyle(color: Colors.blue)),

            SizedBox(height: 20),

            Text("Upload Annotation File:", style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
            SizedBox(height: 8),
            ElevatedButton.icon(
              icon: Icon(Icons.upload_file),
              label: Text("Select Annotation File"),
              onPressed: () => pickFile(selectedDataset, false),
            ),
            if (annotationFileName != null) Text("Selected: $annotationFileName", style: TextStyle(color: Colors.blue)),
          ],
        ),
      ),
    );
  }
}
