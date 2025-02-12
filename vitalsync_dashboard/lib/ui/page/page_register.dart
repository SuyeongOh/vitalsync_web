import 'package:flutter/material.dart';
import '../../service/http_service.dart';

class RegisterPage extends StatefulWidget {
  @override
  _RegisterPageState createState() => _RegisterPageState();
}

class _RegisterPageState extends State<RegisterPage> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController userIdController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController nameController = TextEditingController();
  final TextEditingController emailController = TextEditingController();

  Future<void> handleRegister() async {
    if (!_formKey.currentState!.validate()) return;

    bool success = await registerUser(
      userId: userIdController.text,
      password: passwordController.text,
      name: nameController.text,
      email: emailController.text,
    );

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(success ? "Registration successful!" : "Registration failed. Please try again."),
        backgroundColor: success ? Colors.green : Colors.red,
      ),
    );

    if (success) Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    double screenHeight = MediaQuery.of(context).size.height; // 전체 화면 높이
    double screenWidth = MediaQuery.of(context).size.width; // 전체 화면 너비

    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          child: Align(
            alignment: Alignment.center,
            child: Container(
              width: screenWidth * 0.5, // 화면 너비의 50%
              height: screenHeight * 0.7, // 화면 높이의 70%
              child: Card(
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12.0)),
                elevation: 6.0,
                child: Padding(
                  padding: EdgeInsets.all(20.0),
                  child: Form(
                    key: _formKey,
                    child: Column(
                      mainAxisSize: MainAxisSize.min, // 내용물 크기에 맞게 카드 크기 조정
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Center(
                          child: Text("Sign Up", style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                        ),
                        SizedBox(height: 30),

                        RegisterTextFieldWidgets.commonTextField(
                          controller: userIdController,
                          label: "User ID",
                          hint: "Enter your user ID",
                          validator: (value) =>
                          value == null || value.isEmpty ? "Please enter a user ID" : null,
                        ),

                        RegisterTextFieldWidgets.commonTextField(
                          controller: passwordController,
                          label: "Password",
                          hint: "Enter your password",
                          obscureText: true,
                          validator: (value) =>
                          value == null || value.length < 6 ? "Password must be at least 6 characters" : null,
                        ),

                        RegisterTextFieldWidgets.commonTextField(
                          controller: nameController,
                          label: "Name",
                          hint: "Enter your full name",
                          validator: (value) =>
                          value == null || value.isEmpty ? "Please enter your name" : null,
                        ),

                        RegisterTextFieldWidgets.commonTextField(
                          controller: emailController,
                          label: "Email",
                          hint: "Enter your email",
                          validator: (value) =>
                          value == null || !value.contains("@") ? "Enter a valid email" : null,
                        ),
                        SizedBox(height: 40),

                        Center(
                          child: RegisterTextFieldWidgets.commonButton(
                            text: "Register",
                            onPressed: handleRegister,
                          ),
                        ),
                        SizedBox(height: 10),
                        // Already have an account? Sign In
                        Center(
                          child: TextButton(
                            onPressed: () => Navigator.pop(context),
                            child: Text("Already have an account? Sign In"),
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class RegisterTextFieldWidgets {
  // 📌 공통 입력 필드
  static Widget commonTextField({
    required TextEditingController controller,
    required String label,
    required String hint,
    bool obscureText = false,
    String? Function(String?)? validator,
  }) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: TextStyle(fontWeight: FontWeight.bold)),
        SizedBox(height: 5),
        TextFormField(
          controller: controller,
          obscureText: obscureText,
          decoration: InputDecoration(
            hintText: hint,
            filled: true,
            fillColor: Colors.grey[100],
            border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
          ),
          validator: validator,
        ),
        SizedBox(height: 15),
      ],
    );
  }

  // 📌 공통 버튼
  static Widget commonButton({
    required String text,
    required VoidCallback onPressed,
    Color color = Colors.blueAccent,
  }) {
    return SizedBox(
      width: 400,
      height: 50,
      child: ElevatedButton(
        onPressed: onPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: color,
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
        ),
        child: Text(text, style: TextStyle(fontSize: 18)),
      ),
    );
  }
}
