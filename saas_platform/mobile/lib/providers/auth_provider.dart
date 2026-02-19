import 'package:flutter/material.dart';
import '../models/user.dart';
import '../services/auth_service.dart';
import '../services/storage_service.dart';
import '../services/api_service.dart';

class AuthProvider extends ChangeNotifier {
  final StorageService _storage;
  final AuthService _authService = AuthService();

  User? _user;
  Membership? _membership;
  ApiService? _api;
  bool _loading = false;
  String? _error;

  // Multi-company selection
  List<Company>? _pendingCompanies;
  String? _pendingEmail;
  String? _pendingPassword;

  // Two-Factor Authentication
  bool _requires2FA = false;
  String? _tempToken;

  AuthProvider(this._storage) {
    _restoreSession();
  }

  // Getters
  User? get user => _user;
  Membership? get membership => _membership;
  ApiService? get api => _api;
  bool get loading => _loading;
  String? get error => _error;
  bool get isLoggedIn => _storage.isLoggedIn && _api != null;
  String get companyName => _storage.companyName ?? '';
  String get role => _storage.role ?? '';
  List<Company>? get pendingCompanies => _pendingCompanies;
  bool get requires2FA => _requires2FA;

  void _restoreSession() {
    if (_storage.isLoggedIn) {
      final userData = _storage.user;
      if (userData != null) {
        _user = User.fromJson(userData);
      }
      final memData = _storage.membership;
      if (memData != null) {
        _membership = Membership.fromJson(memData);
      }
      _api = ApiService(
        token: _storage.token!,
        companyId: _storage.companyId!,
      );
    }
  }

  Future<bool> login(String email, String password) async {
    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final result = await _authService.login(email, password);

      if (result is TwoFactorRequiredResult) {
        _requires2FA = true;
        _tempToken = result.tempToken;
        _pendingEmail = email;
        _pendingPassword = password;
        _loading = false;
        notifyListeners();
        return false; // Needs 2FA verification
      }

      if (result is CompanySelectionResult) {
        _pendingCompanies = result.companies;
        _pendingEmail = email;
        _pendingPassword = password;
        _loading = false;
        notifyListeners();
        return false; // Needs company selection
      }

      final loginResult = result as LoginResult;
      await _storeLoginResult(loginResult);
      _loading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _loading = false;
      notifyListeners();
      return false;
    }
  }

  Future<bool> verify2FA(String code) async {
    if (_tempToken == null) return false;

    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final result = await _authService.verify2FA(_tempToken!, code);
      await _storeLoginResult(result);
      _requires2FA = false;
      _tempToken = null;
      _pendingEmail = null;
      _pendingPassword = null;
      _loading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _loading = false;
      notifyListeners();
      return false;
    }
  }

  void cancel2FA() {
    _requires2FA = false;
    _tempToken = null;
    _pendingEmail = null;
    _pendingPassword = null;
    _error = null;
    notifyListeners();
  }

  Future<bool> selectCompany(String companyId) async {
    if (_pendingEmail == null || _pendingPassword == null) return false;

    _loading = true;
    _error = null;
    notifyListeners();

    try {
      final result = await _authService.login(
        _pendingEmail!,
        _pendingPassword!,
        companyId,
      );

      if (result is TwoFactorRequiredResult) {
        _requires2FA = true;
        _tempToken = result.tempToken;
        _pendingCompanies = null;
        _loading = false;
        notifyListeners();
        return false;
      }

      if (result is CompanySelectionResult) {
        _error = 'Please select a company';
        _loading = false;
        notifyListeners();
        return false;
      }

      final loginResult = result as LoginResult;
      await _storeLoginResult(loginResult);
      _pendingCompanies = null;
      _pendingEmail = null;
      _pendingPassword = null;
      _loading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString();
      _loading = false;
      notifyListeners();
      return false;
    }
  }

  void cancelCompanySelection() {
    _pendingCompanies = null;
    _pendingEmail = null;
    _pendingPassword = null;
    notifyListeners();
  }

  Future<void> _storeLoginResult(LoginResult result) async {
    await _storage.setToken(result.token);
    await _storage.setUser({
      'id': result.user.id,
      'email': result.user.email,
      'full_name': result.user.fullName,
      'phone': result.user.phone,
    });
    await _storage.setMembership({
      'id': result.membership.id,
      'user': result.membership.userId,
      'company': result.membership.company,
      'company_name': result.membership.companyName,
      'role': result.membership.role,
      'branch_name': result.membership.branchName,
    });
    await _storage.setCompanyId(result.membership.company);
    await _storage.setCompanyName(result.membership.companyName);
    await _storage.setRole(result.membership.role);

    _user = result.user;
    _membership = result.membership;
    _api = ApiService(
      token: result.token,
      companyId: result.membership.company,
    );
  }

  Future<void> logout() async {
    if (_storage.token != null) {
      await _authService.logout(_storage.token!);
    }
    await _storage.clear();
    _user = null;
    _membership = null;
    _api = null;
    notifyListeners();
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}
