class User {
  final String id;
  final String email;
  final String fullName;
  final String phone;
  final String? avatar;
  final bool isActive;

  User({
    required this.id,
    required this.email,
    required this.fullName,
    required this.phone,
    this.avatar,
    this.isActive = true,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        id: json['id'],
        email: json['email'],
        fullName: json['full_name'] ?? '',
        phone: json['phone'] ?? '',
        avatar: json['avatar'],
        isActive: json['is_active'] ?? true,
      );
}

class Company {
  final String id;
  final String name;
  final String role;

  Company({required this.id, required this.name, required this.role});

  factory Company.fromJson(Map<String, dynamic> json) => Company(
        id: json['id'],
        name: json['name'],
        role: json['role'],
      );
}

class Membership {
  final String id;
  final String userId;
  final String company;
  final String companyName;
  final String role;
  final String? branchName;
  final bool isActive;

  Membership({
    required this.id,
    required this.userId,
    required this.company,
    required this.companyName,
    required this.role,
    this.branchName,
    this.isActive = true,
  });

  factory Membership.fromJson(Map<String, dynamic> json) => Membership(
        id: json['id'],
        userId: json['user'],
        company: json['company'],
        companyName: json['company_name'] ?? '',
        role: json['role'],
        branchName: json['branch_name'],
        isActive: json['is_active'] ?? true,
      );
}
