class Zone {
  final int id;
  final String name;
  final String disasterEvent;
  final int populationEstimate;
  final double vulnerablePopulationPct;
  final String severity;

  Zone({
    required this.id,
    required this.name,
    required this.disasterEvent,
    required this.populationEstimate,
    required this.vulnerablePopulationPct,
    required this.severity,
  });

  factory Zone.fromJson(Map<String, dynamic> json) {
    return Zone(
      id: json['id'],
      name: json['name'] ?? 'Unnamed zone',
      disasterEvent: json['disaster_event'] ?? '',
      populationEstimate: json['population_estimate'] ?? 0,
      vulnerablePopulationPct: (json['vulnerable_population_pct'] ?? 0).toDouble(),
      severity: json['severity'] ?? 'moderate',
    );
  }
}

class DemandPrediction {
  final double foodPackets;
  final double waterLiters;
  final double medicalKits;
  final double shelterCapacity;

  DemandPrediction({
    required this.foodPackets,
    required this.waterLiters,
    required this.medicalKits,
    required this.shelterCapacity,
  });

  factory DemandPrediction.fromJson(Map<String, dynamic> json) {
    return DemandPrediction(
      foodPackets: (json['predicted_food_packets'] ?? 0).toDouble(),
      waterLiters: (json['predicted_water_liters'] ?? 0).toDouble(),
      medicalKits: (json['predicted_medical_kits'] ?? 0).toDouble(),
      shelterCapacity: (json['predicted_shelter_capacity'] ?? 0).toDouble(),
    );
  }
}
