import 'package:flutter/material.dart';
import '../models/zone.dart';
import '../services/api_service.dart';

class ZoneDetailScreen extends StatefulWidget {
  final Zone zone;
  const ZoneDetailScreen({super.key, required this.zone});

  @override
  State<ZoneDetailScreen> createState() => _ZoneDetailScreenState();
}

class _ZoneDetailScreenState extends State<ZoneDetailScreen> {
  final ApiService _api = ApiService();
  late Future<DemandPrediction> _demandFuture;

  @override
  void initState() {
    super.initState();
    _demandFuture = _api.fetchDemand(widget.zone.id);
  }

  Widget _manifestRow(String label, String value, IconData icon) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Row(
        children: [
          Icon(icon, size: 20, color: const Color(0xFF8A2332)),
          const SizedBox(width: 12),
          Expanded(child: Text(label, style: const TextStyle(fontSize: 14.5))),
          Text(value, style: const TextStyle(fontWeight: FontWeight.w700, fontSize: 14.5)),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final zone = widget.zone;
    return Scaffold(
      backgroundColor: const Color(0xFFF4F5F7),
      appBar: AppBar(
        title: Text(zone.name),
        backgroundColor: const Color(0xFF8A2332),
        foregroundColor: Colors.white,
        elevation: 0,
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            child: Padding(
              padding: const EdgeInsets.all(16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(zone.disasterEvent, style: const TextStyle(color: Colors.grey, fontSize: 13)),
                  const SizedBox(height: 8),
                  Text('Severity: ${zone.severity.toUpperCase()}', style: const TextStyle(fontWeight: FontWeight.w700)),
                  const SizedBox(height: 4),
                  Text('Affected population: ${zone.populationEstimate}'),
                  Text('Vulnerable: ${(zone.vulnerablePopulationPct * 100).toStringAsFixed(0)}%'),
                ],
              ),
            ),
          ),
          const SizedBox(height: 16),
          const Text('Supply Manifest', style: TextStyle(fontSize: 16, fontWeight: FontWeight.w700)),
          const SizedBox(height: 8),
          Card(
            shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: FutureBuilder<DemandPrediction>(
                future: _demandFuture,
                builder: (context, snapshot) {
                  if (snapshot.connectionState == ConnectionState.waiting) {
                    return const Padding(padding: EdgeInsets.all(20), child: Center(child: CircularProgressIndicator()));
                  }
                  if (snapshot.hasError) {
                    return const Padding(padding: EdgeInsets.all(16), child: Text('Could not load demand prediction.'));
                  }
                  final d = snapshot.data!;
                  return Column(
                    children: [
                      _manifestRow('Food packets', d.foodPackets.toStringAsFixed(0), Icons.rice_bowl_outlined),
                      const Divider(height: 1),
                      _manifestRow('Water (litres)', d.waterLiters.toStringAsFixed(0), Icons.water_drop_outlined),
                      const Divider(height: 1),
                      _manifestRow('Medical kits', d.medicalKits.toStringAsFixed(0), Icons.medical_services_outlined),
                      const Divider(height: 1),
                      _manifestRow('Shelter capacity', d.shelterCapacity.toStringAsFixed(0), Icons.home_outlined),
                    ],
                  );
                },
              ),
            ),
          ),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: () {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Check-in recorded (local only — not yet wired to backend)')),
              );
            },
            icon: const Icon(Icons.check_circle_outline),
            label: const Text('Check In at This Zone'),
            style: ElevatedButton.styleFrom(
              backgroundColor: const Color(0xFF8A2332),
              foregroundColor: Colors.white,
              minimumSize: const Size.fromHeight(48),
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(10)),
            ),
          ),
        ],
      ),
    );
  }
}
