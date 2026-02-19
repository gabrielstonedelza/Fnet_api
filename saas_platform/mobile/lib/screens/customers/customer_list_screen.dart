import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../config/theme.dart';
import '../../models/customer.dart';
import '../../providers/auth_provider.dart';
import 'customer_create_screen.dart';

class CustomerListScreen extends StatefulWidget {
  const CustomerListScreen({super.key});

  @override
  State<CustomerListScreen> createState() => _CustomerListScreenState();
}

class _CustomerListScreenState extends State<CustomerListScreen> {
  List<Customer> _customers = [];
  bool _loading = true;
  String? _error;
  final _searchCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _loadCustomers();
  }

  @override
  void dispose() {
    _searchCtrl.dispose();
    super.dispose();
  }

  Future<void> _loadCustomers({String? search}) async {
    final api = context.read<AuthProvider>().api;
    if (api == null) return;

    setState(() {
      _loading = true;
      _error = null;
    });

    try {
      final customers = await api.getCustomers(search: search);
      if (mounted) setState(() { _customers = customers; _loading = false; });
    } catch (e) {
      if (mounted) setState(() { _error = e.toString(); _loading = false; });
    }
  }

  Future<void> _deleteCustomer(Customer customer) async {
    final confirm = await showDialog<bool>(
      context: context,
      builder: (ctx) => AlertDialog(
        title: const Text('Deactivate Customer'),
        content: Text('Deactivate ${customer.fullName}? This can be reversed by an admin.'),
        actions: [
          TextButton(onPressed: () => Navigator.pop(ctx, false), child: const Text('Cancel')),
          TextButton(
            onPressed: () => Navigator.pop(ctx, true),
            child: const Text('Deactivate', style: TextStyle(color: MerchantTheme.danger)),
          ),
        ],
      ),
    );

    if (confirm != true) return;

    try {
      await context.read<AuthProvider>().api!.deleteCustomer(customer.id);
      _loadCustomers();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('${customer.fullName} deactivated')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString()), backgroundColor: MerchantTheme.danger),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Customers'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final created = await Navigator.push<bool>(
            context,
            MaterialPageRoute(builder: (_) => const CustomerCreateScreen()),
          );
          if (created == true) _loadCustomers();
        },
        backgroundColor: MerchantTheme.primary,
        child: const Icon(Icons.person_add, color: Colors.white),
      ),
      body: Column(
        children: [
          // Search bar
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              controller: _searchCtrl,
              decoration: InputDecoration(
                hintText: 'Search by name or phone...',
                prefixIcon: const Icon(Icons.search),
                suffixIcon: _searchCtrl.text.isNotEmpty
                    ? IconButton(
                        icon: const Icon(Icons.clear),
                        onPressed: () {
                          _searchCtrl.clear();
                          _loadCustomers();
                        },
                      )
                    : null,
              ),
              onSubmitted: (v) => _loadCustomers(search: v),
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
                            Text(_error!, style: const TextStyle(color: MerchantTheme.danger)),
                            TextButton(onPressed: () => _loadCustomers(), child: const Text('Retry')),
                          ],
                        ),
                      )
                    : _customers.isEmpty
                        ? const Center(child: Text('No customers found'))
                        : RefreshIndicator(
                            onRefresh: () => _loadCustomers(),
                            child: ListView.builder(
                              itemCount: _customers.length,
                              itemBuilder: (ctx, i) {
                                final c = _customers[i];
                                return _CustomerTile(
                                  customer: c,
                                  onDelete: () => _deleteCustomer(c),
                                );
                              },
                            ),
                          ),
          ),
        ],
      ),
    );
  }
}

class _CustomerTile extends StatelessWidget {
  final Customer customer;
  final VoidCallback onDelete;

  const _CustomerTile({required this.customer, required this.onDelete});

  @override
  Widget build(BuildContext context) {
    final statusColor = {
      'active': MerchantTheme.accent,
      'inactive': Colors.grey,
      'blocked': MerchantTheme.danger,
    }[customer.status] ?? Colors.grey;

    return ListTile(
      leading: CircleAvatar(
        backgroundColor: MerchantTheme.primary.withOpacity(0.1),
        child: Text(
          customer.initials,
          style: const TextStyle(
            color: MerchantTheme.primary,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      title: Row(
        children: [
          Expanded(child: Text(customer.fullName, style: const TextStyle(fontWeight: FontWeight.w600))),
          Container(
            width: 8,
            height: 8,
            decoration: BoxDecoration(color: statusColor, shape: BoxShape.circle),
          ),
        ],
      ),
      subtitle: Text(customer.phone),
      trailing: IconButton(
        icon: const Icon(Icons.delete_outline, color: MerchantTheme.danger, size: 20),
        onPressed: onDelete,
      ),
    );
  }
}
