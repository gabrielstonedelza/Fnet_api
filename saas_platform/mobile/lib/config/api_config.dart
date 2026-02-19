class ApiConfig {
  // Change this to your backend URL
  static const String baseUrl = 'http://10.0.2.2:8000'; // Android emulator → localhost
  // static const String baseUrl = 'http://localhost:8000'; // iOS simulator
  // static const String baseUrl = 'https://merchantplusgh.com'; // Production

  static const String apiPrefix = '/api/v1';

  // Auth
  static const String loginUrl = '$apiPrefix/auth/login/';
  static const String logoutUrl = '$apiPrefix/auth/logout/';
  static const String meUrl = '$apiPrefix/auth/me/';
  static const String twoFAVerifyUrl = '$apiPrefix/auth/2fa/verify/';

  // Customers
  static const String customersUrl = '$apiPrefix/customers/';
  static String customerDetailUrl(String id) => '$apiPrefix/customers/$id/';

  // Transactions
  static const String transactionsUrl = '$apiPrefix/transactions/';
  static const String bankDepositUrl = '$apiPrefix/transactions/bank-deposit/';
  static const String momoTransactionUrl = '$apiPrefix/transactions/mobile-money/';
  static const String cashTransactionUrl = '$apiPrefix/transactions/cash/';

  // Provider Balances
  static const String providerBalancesUrl = '$apiPrefix/transactions/balances/';
  static const String adjustBalanceUrl = '$apiPrefix/transactions/balances/adjust/';
}
