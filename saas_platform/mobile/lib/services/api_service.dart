import 'dart:convert';
import 'package:http/http.dart' as http;
import '../config/api_config.dart';
import '../models/customer.dart';
import '../models/transaction.dart';
import '../models/provider_balance.dart';

class ApiService {
  final String token;
  final String companyId;

  ApiService({required this.token, required this.companyId});

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        'Authorization': 'Token $token',
        'X-Company-ID': companyId,
      };

  Uri _uri(String path) => Uri.parse('${ApiConfig.baseUrl}$path');

  // ---------------------------------------------------------------------------
  // Customers
  // ---------------------------------------------------------------------------
  Future<List<Customer>> getCustomers({String? search}) async {
    var url = ApiConfig.customersUrl;
    if (search != null && search.isNotEmpty) {
      url += '?search=$search';
    }
    final resp = await http.get(_uri(url), headers: _headers);
    _checkResponse(resp);
    final list = jsonDecode(resp.body) as List;
    return list.map((j) => Customer.fromJson(j)).toList();
  }

  Future<Customer> createCustomer({
    required String fullName,
    required String phone,
    String email = '',
    String address = '',
    String city = '',
  }) async {
    final resp = await http.post(
      _uri(ApiConfig.customersUrl),
      headers: _headers,
      body: jsonEncode({
        'full_name': fullName,
        'phone': phone,
        if (email.isNotEmpty) 'email': email,
        if (address.isNotEmpty) 'address': address,
        if (city.isNotEmpty) 'city': city,
      }),
    );
    _checkResponse(resp);
    return Customer.fromJson(jsonDecode(resp.body));
  }

  Future<void> deleteCustomer(String customerId) async {
    final resp = await http.delete(
      _uri(ApiConfig.customerDetailUrl(customerId)),
      headers: _headers,
    );
    _checkResponse(resp);
  }

  // ---------------------------------------------------------------------------
  // Transactions
  // ---------------------------------------------------------------------------
  Future<List<Transaction>> getTransactions({
    String? type,
    String? status,
  }) async {
    var url = ApiConfig.transactionsUrl;
    final params = <String>[];
    if (type != null) params.add('type=$type');
    if (status != null) params.add('status=$status');
    if (params.isNotEmpty) url += '?${params.join('&')}';

    final resp = await http.get(_uri(url), headers: _headers);
    _checkResponse(resp);
    final list = jsonDecode(resp.body) as List;
    return list.map((j) => Transaction.fromJson(j)).toList();
  }

  Future<Transaction> createBankDeposit({
    required double amount,
    required String bankName,
    required String accountNumber,
    required String accountName,
    required String depositorName,
    String? customerId,
    String description = '',
    String slipNumber = '',
  }) async {
    final resp = await http.post(
      _uri(ApiConfig.bankDepositUrl),
      headers: _headers,
      body: jsonEncode({
        'amount': amount,
        'bank_name': bankName,
        'account_number': accountNumber,
        'account_name': accountName,
        'depositor_name': depositorName,
        if (customerId != null) 'customer': customerId,
        if (description.isNotEmpty) 'description': description,
        if (slipNumber.isNotEmpty) 'slip_number': slipNumber,
      }),
    );
    _checkResponse(resp);
    return Transaction.fromJson(jsonDecode(resp.body));
  }

  Future<Transaction> createMomoTransaction({
    required String transactionType, // 'deposit' or 'withdrawal'
    required double amount,
    required String network, // 'mtn', 'vodafone', 'airteltigo'
    required String serviceType,
    required String senderNumber,
    String? customerId,
    String receiverNumber = '',
    String momoReference = '',
    String description = '',
  }) async {
    final resp = await http.post(
      _uri(ApiConfig.momoTransactionUrl),
      headers: _headers,
      body: jsonEncode({
        'transaction_type': transactionType,
        'amount': amount,
        'network': network,
        'service_type': serviceType,
        'sender_number': senderNumber,
        if (customerId != null) 'customer': customerId,
        if (receiverNumber.isNotEmpty) 'receiver_number': receiverNumber,
        if (momoReference.isNotEmpty) 'momo_reference': momoReference,
        if (description.isNotEmpty) 'description': description,
      }),
    );
    _checkResponse(resp);
    return Transaction.fromJson(jsonDecode(resp.body));
  }

  Future<Transaction> createCashTransaction({
    required String transactionType,
    required double amount,
    String? customerId,
    String description = '',
  }) async {
    final resp = await http.post(
      _uri(ApiConfig.cashTransactionUrl),
      headers: _headers,
      body: jsonEncode({
        'transaction_type': transactionType,
        'amount': amount,
        if (customerId != null) 'customer': customerId,
        if (description.isNotEmpty) 'description': description,
      }),
    );
    _checkResponse(resp);
    return Transaction.fromJson(jsonDecode(resp.body));
  }

  // ---------------------------------------------------------------------------
  // Provider Balances
  // ---------------------------------------------------------------------------
  Future<List<ProviderBalance>> getProviderBalances() async {
    final resp = await http.get(
      _uri(ApiConfig.providerBalancesUrl),
      headers: _headers,
    );
    _checkResponse(resp);
    final list = jsonDecode(resp.body) as List;
    return list.map((j) => ProviderBalance.fromJson(j)).toList();
  }

  Future<ProviderBalance> adjustBalance({
    required String provider,
    required double amount,
    required String operation, // 'add' or 'subtract'
  }) async {
    final resp = await http.post(
      _uri(ApiConfig.adjustBalanceUrl),
      headers: _headers,
      body: jsonEncode({
        'provider': provider,
        'amount': amount,
        'operation': operation,
      }),
    );
    _checkResponse(resp);
    return ProviderBalance.fromJson(jsonDecode(resp.body));
  }

  // ---------------------------------------------------------------------------
  void _checkResponse(http.Response resp) {
    if (resp.statusCode >= 200 && resp.statusCode < 300) return;
    final body = jsonDecode(resp.body);
    final msg = body['error'] ?? body['detail'] ?? 'Request failed (${resp.statusCode})';
    throw ApiException(msg.toString(), resp.statusCode);
  }
}

class ApiException implements Exception {
  final String message;
  final int statusCode;
  ApiException(this.message, this.statusCode);

  @override
  String toString() => message;
}
