import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/user.dart';

class LoginResult {
  final String token;
  final User user;
  final Membership membership;
  final List<Company> companies;

  LoginResult({
    required this.token,
    required this.user,
    required this.membership,
    required this.companies,
  });
}

class CompanySelectionResult {
  final List<Company> companies;

  CompanySelectionResult({required this.companies});
}

class TwoFactorRequiredResult {
  final String tempToken;
  final String message;

  TwoFactorRequiredResult({required this.tempToken, required this.message});
}

class AuthService {
  /// Attempts login. Returns either a [LoginResult], a
  /// [CompanySelectionResult], or a [TwoFactorRequiredResult].
  Future<dynamic> login(
    String email,
    String password, [
    String? companyId,
  ]) async {
    final body = <String, dynamic>{
      'email': email,
      'password': password,
    };
    if (companyId != null) {
      body['company_id'] = companyId;
    }

    final resp = await http.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.loginUrl}'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(body),
    );

    if (resp.statusCode == 401 || resp.statusCode == 403) {
      final data = jsonDecode(resp.body);
      throw AuthException(data['error'] ?? 'Login failed');
    }

    if (resp.statusCode != 200) {
      throw AuthException('Unexpected error (${resp.statusCode})');
    }

    final data = jsonDecode(resp.body) as Map<String, dynamic>;

    // 2FA required
    if (data['requires_2fa'] == true) {
      return TwoFactorRequiredResult(
        tempToken: data['temp_token'],
        message: data['message'] ?? 'Enter your authenticator code.',
      );
    }

    // Multi-company selection required
    if (data['requires_company_selection'] == true) {
      final companies = (data['companies'] as List)
          .map((c) => Company.fromJson(c))
          .toList();
      return CompanySelectionResult(companies: companies);
    }

    // Full login success
    return LoginResult(
      token: data['token'],
      user: User.fromJson(data['user']),
      membership: Membership.fromJson(data['membership']),
      companies: (data['companies'] as List)
          .map((c) => Company.fromJson(c))
          .toList(),
    );
  }

  /// Verify a 2FA code (TOTP or backup code) using the temp token.
  Future<LoginResult> verify2FA(String tempToken, String code) async {
    final resp = await http.post(
      Uri.parse('${ApiConfig.baseUrl}${ApiConfig.twoFAVerifyUrl}'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({
        'temp_token': tempToken,
        'code': code,
      }),
    );

    if (resp.statusCode == 401) {
      final data = jsonDecode(resp.body);
      throw AuthException(data['error'] ?? 'Invalid authentication code.');
    }

    if (resp.statusCode != 200) {
      throw AuthException('Verification failed (${resp.statusCode})');
    }

    final data = jsonDecode(resp.body) as Map<String, dynamic>;

    return LoginResult(
      token: data['token'],
      user: User.fromJson(data['user']),
      membership: Membership.fromJson(data['membership']),
      companies: (data['companies'] as List)
          .map((c) => Company.fromJson(c))
          .toList(),
    );
  }

  Future<void> logout(String token) async {
    try {
      await http.post(
        Uri.parse('${ApiConfig.baseUrl}${ApiConfig.logoutUrl}'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Token $token',
        },
      );
    } catch (_) {
      // Best-effort logout
    }
  }
}

class AuthException implements Exception {
  final String message;
  AuthException(this.message);

  @override
  String toString() => message;
}
