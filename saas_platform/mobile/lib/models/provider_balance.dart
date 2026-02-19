class ProviderBalance {
  final String id;
  final String provider;
  final String providerDisplay;
  final String balance;
  final String startingBalance;
  final String userName;

  ProviderBalance({
    required this.id,
    required this.provider,
    required this.providerDisplay,
    required this.balance,
    required this.startingBalance,
    required this.userName,
  });

  factory ProviderBalance.fromJson(Map<String, dynamic> json) =>
      ProviderBalance(
        id: json['id'] ?? '',
        provider: json['provider'] ?? '',
        providerDisplay: json['provider_display'] ?? json['provider'] ?? '',
        balance: json['balance']?.toString() ?? '0',
        startingBalance: json['starting_balance']?.toString() ?? '0',
        userName: json['user_name'] ?? '',
      );

  double get balanceNum => double.tryParse(balance) ?? 0;
  double get startingBalanceNum => double.tryParse(startingBalance) ?? 0;
  double get difference => balanceNum - startingBalanceNum;
}
