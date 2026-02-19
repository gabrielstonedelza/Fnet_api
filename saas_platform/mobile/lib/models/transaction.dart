class Transaction {
  final String id;
  final String reference;
  final String transactionType;
  final String channel;
  final String status;
  final String amount;
  final String fee;
  final String netAmount;
  final String currency;
  final String? customerName;
  final String? initiatedByName;
  final String createdAt;

  Transaction({
    required this.id,
    required this.reference,
    required this.transactionType,
    required this.channel,
    required this.status,
    required this.amount,
    required this.fee,
    required this.netAmount,
    this.currency = 'GHS',
    this.customerName,
    this.initiatedByName,
    required this.createdAt,
  });

  factory Transaction.fromJson(Map<String, dynamic> json) => Transaction(
        id: json['id'],
        reference: json['reference'] ?? '',
        transactionType: json['transaction_type'] ?? '',
        channel: json['channel'] ?? '',
        status: json['status'] ?? '',
        amount: json['amount']?.toString() ?? '0',
        fee: json['fee']?.toString() ?? '0',
        netAmount: json['net_amount']?.toString() ?? '0',
        currency: json['currency'] ?? 'GHS',
        customerName: json['customer_name'],
        initiatedByName: json['initiated_by_name'],
        createdAt: json['created_at'] ?? '',
      );

  bool get isDeposit => transactionType == 'deposit';
  bool get isWithdrawal => transactionType == 'withdrawal';
}
