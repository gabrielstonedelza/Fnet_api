import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/auth_provider.dart';
import '../models/provider_balance.dart';
import '../services/api_service.dart';
import 'customers/customer_list_screen.dart';
import 'transactions/transaction_list_screen.dart';
import 'transactions/deposit_screen.dart';
import 'transactions/withdrawal_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<ProviderBalance> _balances = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _loadBalances();
  }

  Future<void> _loadBalances() async {
    final api = context.read<AuthProvider>().api;
    if (api == null) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final balances = await api.getProviderBalances();
      if (mounted) {
        setState(() {
          _balances = balances;
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
    final auth = context.watch<AuthProvider>();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Merchant+'),
        actions: [
          PopupMenuButton<String>(
            onSelected: (value) {
              if (value == 'logout') {
                auth.logout();
              }
            },
            itemBuilder: (_) => [
              PopupMenuItem(
                enabled: false,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      auth.user?.fullName ?? '',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: MerchantTheme.textPrimary,
                      ),
                    ),
                    Text(
                      '${auth.companyName} · ${auth.role}',
                      style: const TextStyle(fontSize: 12),
                    ),
                  ],
                ),
              ),
              const PopupMenuDivider(),
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout, color: MerchantTheme.danger, size: 20),
                    SizedBox(width: 8),
                    Text('Logout', style: TextStyle(color: MerchantTheme.danger)),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: _loadBalances,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            // Welcome
            Text(
              'Welcome, ${auth.user?.fullName ?? "User"}',
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            Text(
              auth.companyName,
              style: const TextStyle(color: MerchantTheme.textSecondary),
            ),
            const SizedBox(height: 24),

            // Quick Actions
            const Text(
              'QUICK ACTIONS',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: MerchantTheme.textSecondary,
                letterSpacing: 1,
              ),
            ),
            const SizedBox(height: 12),
            Row(
              children: [
                _ActionCard(
                  icon: Icons.arrow_downward,
                  label: 'Deposit',
                  color: MerchantTheme.accent,
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const DepositScreen()),
                  ),
                ),
                const SizedBox(width: 12),
                _ActionCard(
                  icon: Icons.arrow_upward,
                  label: 'Withdraw',
                  color: MerchantTheme.danger,
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const WithdrawalScreen()),
                  ),
                ),
                const SizedBox(width: 12),
                _ActionCard(
                  icon: Icons.people,
                  label: 'Customers',
                  color: MerchantTheme.primary,
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const CustomerListScreen()),
                  ),
                ),
                const SizedBox(width: 12),
                _ActionCard(
                  icon: Icons.receipt_long,
                  label: 'History',
                  color: MerchantTheme.warning,
                  onTap: () => Navigator.push(
                    context,
                    MaterialPageRoute(
                        builder: (_) => const TransactionListScreen()),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 24),

            // Provider Balances
            const Text(
              'MY PROVIDER BALANCES',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: MerchantTheme.textSecondary,
                letterSpacing: 1,
              ),
            ),
            const SizedBox(height: 12),

            if (_loading)
              const Center(child: CircularProgressIndicator())
            else if (_error != null)
              Center(
                child: Column(
                  children: [
                    Text(_error!, style: const TextStyle(color: MerchantTheme.danger)),
                    TextButton(
                      onPressed: _loadBalances,
                      child: const Text('Retry'),
                    ),
                  ],
                ),
              )
            else if (_balances.isEmpty)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(24),
                  child: Center(
                    child: Text(
                      'No balances configured yet.\nAsk your admin to initialize your provider balances.',
                      textAlign: TextAlign.center,
                      style: const TextStyle(color: MerchantTheme.textSecondary),
                    ),
                  ),
                ),
              )
            else
              ..._balances.map((b) => _BalanceTile(balance: b)),
          ],
        ),
      ),
    );
  }
}

class _ActionCard extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _ActionCard({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: GestureDetector(
        onTap: onTap,
        child: Card(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 16),
            child: Column(
              children: [
                Container(
                  width: 40,
                  height: 40,
                  decoration: BoxDecoration(
                    color: color.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(10),
                  ),
                  child: Icon(icon, color: color, size: 22),
                ),
                const SizedBox(height: 8),
                Text(
                  label,
                  style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w600),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class _BalanceTile extends StatelessWidget {
  final ProviderBalance balance;
  const _BalanceTile({required this.balance});

  static const _providerColors = {
    'mtn': Color(0xFFEAB308),
    'vodafone': Color(0xFFEF4444),
    'airtel': Color(0xFFEA580C),
    'tigo': Color(0xFF2563EB),
    'ecobank': Color(0xFF0284C7),
    'fidelity': Color(0xFF16A34A),
    'cal_bank': Color(0xFF7C3AED),
  };

  @override
  Widget build(BuildContext context) {
    final color = _providerColors[balance.provider] ?? Colors.grey;
    final diff = balance.difference;

    return Card(
      margin: const EdgeInsets.only(bottom: 8),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Container(
              width: 40,
              height: 40,
              decoration: BoxDecoration(
                color: color.withOpacity(0.1),
                borderRadius: BorderRadius.circular(10),
              ),
              child: Center(
                child: Text(
                  balance.providerDisplay[0],
                  style: TextStyle(
                    color: color,
                    fontWeight: FontWeight.bold,
                    fontSize: 18,
                  ),
                ),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    balance.providerDisplay,
                    style: const TextStyle(fontWeight: FontWeight.w600),
                  ),
                  Text(
                    'Start: GHS ${balance.startingBalanceNum.toStringAsFixed(2)}',
                    style: TextStyle(fontSize: 12, color: Colors.grey[600]),
                  ),
                ],
              ),
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.end,
              children: [
                Text(
                  'GHS ${balance.balanceNum.toStringAsFixed(2)}',
                  style: TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                    color: color,
                  ),
                ),
                if (diff != 0)
                  Text(
                    '${diff > 0 ? "+" : ""}${diff.toStringAsFixed(2)}',
                    style: TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      color: diff > 0 ? MerchantTheme.accent : MerchantTheme.danger,
                    ),
                  ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
