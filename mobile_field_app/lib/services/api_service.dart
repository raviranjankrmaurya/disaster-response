import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/zone.dart';

class ApiConfig {
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator alias for host localhost
}

class ApiService {
  Future<List<Zone>> fetchZones() async {
    final response = await http.get(Uri.parse('${ApiConfig.baseUrl}/api/zones/'));
    if (response.statusCode != 200) {
      throw Exception('Failed to load zones (${response.statusCode})');
    }
    final List<dynamic> data = json.decode(response.body);
    return data.map((z) => Zone.fromJson(z)).toList();
  }

  Future<DemandPrediction> fetchDemand(int zoneId) async {
    final response = await http.get(Uri.parse('${ApiConfig.baseUrl}/api/demand/$zoneId'));
    if (response.statusCode != 200) {
      throw Exception('Failed to load demand prediction (${response.statusCode})');
    }
    return DemandPrediction.fromJson(json.decode(response.body));
  }
}
