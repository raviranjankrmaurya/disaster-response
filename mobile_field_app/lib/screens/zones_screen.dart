import 'package:flutter/material.dart';
import '../models/zone.dart';
import '../services/api_service.dart';
import 'zone_detail_screen.dart';

class ZonesScreen extends StatefulWidget {
  const ZonesScreen({super.key});

  @override
  State<ZonesScreen> createState() => _ZonesScreenState();
}

class _ZonesScreenState extends State<ZonesScreen> {
  final ApiService _api = ApiService();
  late Future<List<Zone>> _zonesFuture;

  @override
  void initState() {
    super.initState();
    _zonesFuture = _api.fetchZones();
  }

  Future<void> _refresh() async {
    setState(() { _zonesFuture = _api.fetchZones(); });
    await _zonesFuture;
  }

  Color _severityColor(String severity) {
    switch (severity) {
      case 'critical': return const Color(0xFFD9455F);
      case 'high': return const Color(0xFFE8823A);
      case 'moderate': return const Color(0xFFD4A72C);
      default: return const Color(0xFF34A468);
    }
  }

  int _severityRank(String severity) {
    const order = {'critical': 0, 'high': 1, 'moderate': 2, 'low': 3};
    return order[severity] ?? 4;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF4F5F7),
      appBar: AppBar(
        title: const Text('My Missions'),
        backgroundColor: const Color(0xFF8A2332),
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: RefreshIndicator(
        onRefresh: _refresh,
        child: FutureBuilder<List<Zone>>(
          future: _zonesFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }
            if (snapshot.hasError) {
              return ListView(
                children: [
                  const SizedBox(height: 80),
                  Icon(Icons.wifi_off, size: 48, color: Colors.grey[400]),
                  const SizedBox(height: 12),
                  Center(
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 32),
                      child: Text(
                        'Could not reach the server.\nCheck ApiConfig.baseUrl in api_service.dart matches your backend address.',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: Colors.grey[600]),
                      ),
                    ),
                  ),
                ],
              );
            }

            final zones = snapshot.data ?? [];
            if (zones.isEmpty) {
              return const Center(child: Text('No active zones assigned.'));
            }

            zones.sort((a, b) => _severityRank(a.severity).compareTo(_severityRank(b.severity)));

            return ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: zones.length,
              itemBuilder: (context, index) {
                final zone = zones[index];
                final color = _severityColor(zone.severity);
                return Card(
                  margin: const EdgeInsets.only(bottom: 10),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                    side: BorderSide(color: color, width: 1),
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                    leading: Container(
                      width: 6,
                      decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(3)),
                    ),
                    title: Text(zone.name, style: const TextStyle(fontWeight: FontWeight.w700)),
                    subtitle: Text('${zone.disasterEvent}\nPop: ${zone.populationEstimate}'),
                    isThreeLine: true,
                    trailing: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                      decoration: BoxDecoration(
                        color: color.withOpacity(0.12),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        zone.severity.toUpperCase(),
                        style: TextStyle(color: color, fontSize: 11, fontWeight: FontWeight.w700),
                      ),
                    ),
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(builder: (_) => ZoneDetailScreen(zone: zone)),
                      );
                    },
                  ),
                );
              },
            );
          },
        ),
      ),
    );
  }
}
