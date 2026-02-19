import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../models/transaction.dart';
import '../../providers/auth_provider.dart';

class TransactionListScreen extends StatefulWidget {
  const TransactionListScreen({super.key});

  @override
  State<TransactionListScreen> createState() => _TransactionListScreenState();
}

class _TransactionListScreenState extends State<TransactionListScreen> {
  List<Transaction> _transactions = [];
  bool _loading = true;
  String? _error;
  String? _typeFilter;

  @override
  void initState() {
    super.initState();
    _loadTransactions();
  }

  Future<void> _loadTransactions() async {
    final api = context.read<AuthProvider>().api;
    if (api == null) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final txns = await api.getTransactions(type: _typeFilter);
      if (mounted) {
        setState(() {
          _transactions = txns;
          _loading = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() {
          _error = e.toString();
          _loading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Transaction History'),
      ),
      body: Column(
        children: [
          // Filter chips
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: Row(
              children: [
                _FilterChip(
                  label: 'All',
                  selected: _typeFilter == null,
                  onTap: () {
                    setState(() => _typeFilter = null);
                    _loadTransactions();
                  },
                ),
                const SizedBox(width: 8),
                _FilterChip(
                  label: 'Deposits',
                  selected: _typeFilter == 'deposit',
                  onTap: () {
                    setState(() => _typeFilter = 'deposit');
                    _loadTransactions();
                  },
                ),
                const SizedBox(width: 8),
                _FilterChip(
                  label: 'Withdrawals',
                  selected: _typeFilter == 'withdrawal',
                  onTap: () {
                    setState(() => _typeFilter = 'withdrawal');
                    _loadTransactions();
                  },
                ),
              ],
            ),
          ),

          // List
          Expanded(
            child: _loading
                ? const Center(child: CircularProgressIndicator())
                : _error != null
                    ? Center(
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(_error!,
                                style:
                                    const TextStyle(color: MerchantTheme.danger)),
                            TextButton(
                              onPressed: _loadTransactions,
                              child: const Text('Retry'),
                            ),
                          ],
                        ),
                      )
                    : _transactions.isEmpty
                        ? const Center(
                            child: Text('No transactions yet'))
                        : RefreshIndicator(
                            onRefresh: _loadTransactions,
                            child: ListView.separated(
                              itemCount: _transactions.length,
                              separatorBuilder: (_, __) =>
                                  const Divider(height: 1),
                              itemBuilder: (ctx, i) =>
                                  _TransactionTile(txn: _transactions[i]),
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

class _FilterChip extends StatelessWidget {
  final String label;
  final bool selected;
  final VoidCallback onTap;

  const _FilterChip({
    required this.label,
    required this.selected,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: selected
              ? MerchantTheme.primary
              : MerchantTheme.primary.withOpacity(0.08),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Text(
          label,
          style: TextStyle(
            color: selected ? Colors.white : MerchantTheme.primary,
            fontWeight: FontWeight.w600,
            fontSize: 13,
          ),
        ),
      ),
    );
  }
}

class _TransactionTile extends StatelessWidget {
  final Transaction txn;
  const _TransactionTile({required this.txn});

  @override
  Widget build(BuildContext context) {
    final isDeposit = txn.isDeposit;
    final color = isDeposit ? MerchantTheme.accent : MerchantTheme.danger;
    final icon = isDeposit ? Icons.arrow_downward : Icons.arrow_upward;
    final sign = isDeposit ? '+' : '-';

    final statusColor = {
      'completed': MerchantTheme.accent,
      'pending': MerchantTheme.warning,
      'failed': MerchantTheme.danger,
      'reversed': Colors.grey,
    }[txn.status] ?? Colors.grey;

    return ListTile(
      leading: Container(
        width: 40,
        height: 40,
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(10),
        ),
        child: Icon(icon, color: color, size: 20),
      ),
      title: Row(
        children: [
          Expanded(
            child: Text(
              '${txn.transactionType.toUpperCase()} · ${txn.channel}',
              style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 14),
            ),
          ),
          Text(
            '$sign GHS ${txn.amount}',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: color,
              fontSize: 14,
            ),
          ),
        ],
      ),
      subtitle: Row(
        children: [
          Expanded(
            child: Text(
              txn.reference,
              style: TextStyle(fontSize: 12, color: Colors.grey[600]),
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
            decoration: BoxDecoration(
              color: statusColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(4),
            ),
            child: Text(
              txn.status.toUpperCase(),
              style: TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.bold,
                color: statusColor,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
