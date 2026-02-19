import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class StorageService {
  static const _tokenKey = 'token';
  static const _userKey = 'user';
  static const _membershipKey = 'membership';
  static const _companyIdKey = 'companyId';
  static const _companyNameKey = 'companyName';
  static const _roleKey = 'role';
  static const _companiesKey = 'companies';

  late SharedPreferences _prefs;

  Future<void> init() async {
    _prefs = await SharedPreferences.getInstance();
  }

  // Token
  String? get token => _prefs.getString(_tokenKey);
  Future<void> setToken(String token) => _prefs.setString(_tokenKey, token);

  // Company ID
  String? get companyId => _prefs.getString(_companyIdKey);
  Future<void> setCompanyId(String id) => _prefs.setString(_companyIdKey, id);

  // Company Name
  String? get companyName => _prefs.getString(_companyNameKey);
  Future<void> setCompanyName(String name) =>
      _prefs.setString(_companyNameKey, name);

  // Role
  String? get role => _prefs.getString(_roleKey);
  Future<void> setRole(String role) => _prefs.setString(_roleKey, role);

  // User JSON
  Map<String, dynamic>? get user {
    final s = _prefs.getString(_userKey);
    if (s == null) return null;
    return jsonDecode(s) as Map<String, dynamic>;
  }

  Future<void> setUser(Map<String, dynamic> user) =>
      _prefs.setString(_userKey, jsonEncode(user));

  // Membership JSON
  Map<String, dynamic>? get membership {
    final s = _prefs.getString(_membershipKey);
    if (s == null) return null;
    return jsonDecode(s) as Map<String, dynamic>;
  }

  Future<void> setMembership(Map<String, dynamic> m) =>
      _prefs.setString(_membershipKey, jsonEncode(m));

  // Companies JSON
  List<Map<String, dynamic>>? get companies {
    final s = _prefs.getString(_companiesKey);
    if (s == null) return null;
    return (jsonDecode(s) as List).cast<Map<String, dynamic>>();
  }

  Future<void> setCompanies(List<dynamic> c) =>
      _prefs.setString(_companiesKey, jsonEncode(c));

  // Clear all
  Future<void> clear() async {
    await _prefs.remove(_tokenKey);
    await _prefs.remove(_userKey);
    await _prefs.remove(_membershipKey);
    await _prefs.remove(_companyIdKey);
    await _prefs.remove(_companyNameKey);
    await _prefs.remove(_roleKey);
    await _prefs.remove(_companiesKey);
  }

  bool get isLoggedIn => token != null && companyId != null;
}
