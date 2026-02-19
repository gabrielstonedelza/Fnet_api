import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../config/theme.dart';

class WithdrawalScreen extends StatefulWidget {
  const WithdrawalScreen({super.key});

  @override
  State<WithdrawalScreen> createState() => _WithdrawalScreenState();
}

class _WithdrawalScreenState extends State<WithdrawalScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  final _formKey = GlobalKey<FormState>();
  bool _loading = false;

  final _amountCtrl = TextEditingController();
  final _descCtrl = TextEditingController();

  // MoMo fields
  String _momoNetwork = 'mtn';
  final _receiverCtrl = TextEditingController();
  final _momoRefCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    _amountCtrl.dispose();
    _descCtrl.dispose();
    _receiverCtrl.dispose();
    _momoRefCtrl.dispose();
    super.dispose();
  }

  Future<void> _submitMomoWithdrawal() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      await context.read<AuthProvider>().api!.createMomoTransaction(
            transactionType: 'withdrawal',
            amount: double.parse(_amountCtrl.text.trim()),
            network: _momoNetwork,
            serviceType: 'cash_out',
            senderNumber: _receiverCtrl.text.trim(),
            description: _descCtrl.text.trim(),
          );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('MoMo withdrawal recorded')),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString()), backgroundColor: MerchantTheme.danger),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _submitCashWithdrawal() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      await context.read<AuthProvider>().api!.createCashTransaction(
            transactionType: 'withdrawal',
            amount: double.parse(_amountCtrl.text.trim()),
            description: _descCtrl.text.trim(),
          );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Cash withdrawal recorded')),
        );
        Navigator.pop(context, true);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text(e.toString()), backgroundColor: MerchantTheme.danger),
        );
      }
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('New Withdrawal'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: const [
            Tab(icon: Icon(Icons.phone_android), text: 'MoMo'),
            Tab(icon: Icon(Icons.payments), text: 'Cash'),
          ],
        ),
      ),
      body: Form(
        key: _formKey,
        child: TabBarView(
          controller: _tabCtrl,
          children: [
            _buildMomoForm(),
            _buildCashForm(),
          ],
        ),
      ),
    );
  }

  Widget _buildMomoForm() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _amountField(),
          const SizedBox(height: 16),
          DropdownButtonFormField<String>(
            value: _momoNetwork,
            decoration: const InputDecoration(
              labelText: 'Network *',
              prefixIcon: Icon(Icons.cell_tower),
            ),
            items: const [
              DropdownMenuItem(value: 'mtn', child: Text('MTN')),
              DropdownMenuItem(value: 'vodafone', child: Text('Vodafone')),
              DropdownMenuItem(value: 'airteltigo', child: Text('AirtelTigo')),
            ],
            onChanged: (v) => setState(() => _momoNetwork = v ?? 'mtn'),
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _receiverCtrl,
            decoration: const InputDecoration(
              labelText: 'Receiver Number *',
              prefixIcon: Icon(Icons.phone),
              hintText: '0XX XXX XXXX',
            ),
            keyboardType: TextInputType.phone,
            validator: (v) => v == null || v.isEmpty ? 'Required' : null,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _momoRefCtrl,
            decoration: const InputDecoration(
              labelText: 'MoMo Reference (optional)',
              prefixIcon: Icon(Icons.tag),
            ),
          ),
          const SizedBox(height: 16),
          _descriptionField(),
          const SizedBox(height: 24),
          _submitButton('Record MoMo Withdrawal', _submitMomoWithdrawal),
        ],
      ),
    );
  }

  Widget _buildCashForm() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _amountField(),
          const SizedBox(height: 16),
          _descriptionField(),
          const SizedBox(height: 24),
          _submitButton('Record Cash Withdrawal', _submitCashWithdrawal),
        ],
      ),
    );
  }

  Widget _amountField() => TextFormField(
        controller: _amountCtrl,
        decoration: const InputDecoration(
          labelText: 'Amount (GHS) *',
          prefixIcon: Icon(Icons.attach_money),
        ),
        keyboardType: const TextInputType.numberWithOptions(decimal: true),
        validator: (v) {
          if (v == null || v.isEmpty) return 'Amount is required';
          final num = double.tryParse(v);
          if (num == null || num <= 0) return 'Enter a valid positive amount';
          return null;
        },
      );

  Widget _descriptionField() => TextFormField(
        controller: _descCtrl,
        decoration: const InputDecoration(
          labelText: 'Description (optional)',
          prefixIcon: Icon(Icons.notes),
        ),
        maxLines: 2,
      );

  Widget _submitButton(String label, VoidCallback onPressed) =>
      ElevatedButton(
        onPressed: _loading ? null : onPressed,
        child: _loading
            ? const SizedBox(
                height: 20,
                width: 20,
                child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
              )
            : Text(label),
      );
}
