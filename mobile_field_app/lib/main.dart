import 'package:flutter/material.dart';
import 'screens/zones_screen.dart';

void main() {
  runApp(const RakshaFieldApp());
}

class RakshaFieldApp extends StatelessWidget {
  const RakshaFieldApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RakshaGrid Field',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorSchemeSeed: const Color(0xFF8A2332),
        useMaterial3: true,
        fontFamily: 'Roboto',
      ),
      home: const ZonesScreen(),
    );
  }
}
