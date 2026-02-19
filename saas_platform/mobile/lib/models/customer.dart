class Customer {
  final String id;
  final String fullName;
  final String phone;
  final String email;
  final String? address;
  final String? city;
  final String status;
  final String kycStatus;
  final String? registeredBy;
  final String createdAt;

  Customer({
    required this.id,
    required this.fullName,
    required this.phone,
    this.email = '',
    this.address,
    this.city,
    this.status = 'active',
    this.kycStatus = 'pending',
    this.registeredBy,
    required this.createdAt,
  });

  factory Customer.fromJson(Map<String, dynamic> json) => Customer(
        id: json['id'],
        fullName: json['full_name'] ?? '',
        phone: json['phone'] ?? '',
        email: json['email'] ?? '',
        address: json['address'],
        city: json['city'],
        status: json['status'] ?? 'active',
        kycStatus: json['kyc_status'] ?? 'pending',
        registeredBy: json['registered_by_name'],
        createdAt: json['created_at'] ?? '',
      );

  String get initials {
    final parts = fullName.split(' ');
    if (parts.length >= 2) {
      return '${parts[0][0]}${parts[1][0]}'.toUpperCase();
    }
    return fullName.isNotEmpty ? fullName[0].toUpperCase() : '?';
  }
}
