import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/auth_provider.dart';
import '../../config/theme.dart';

class DepositScreen extends StatefulWidget {
  const DepositScreen({super.key});

  @override
  State<DepositScreen> createState() => _DepositScreenState();
}

class _DepositScreenState extends State<DepositScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabCtrl;
  final _formKey = GlobalKey<FormState>();
  bool _loading = false;

  // Common
  final _amountCtrl = TextEditingController();
  final _descCtrl = TextEditingController();

  // Bank fields
  final _bankNameCtrl = TextEditingController();
  final _accountNumCtrl = TextEditingController();
  final _accountNameCtrl = TextEditingController();
  final _depositorCtrl = TextEditingController();
  final _slipCtrl = TextEditingController();

  // MoMo fields
  String _momoNetwork = 'mtn';
  final _senderCtrl = TextEditingController();
  final _momoRefCtrl = TextEditingController();

  @override
  void initState() {
    super.initState();
    _tabCtrl = TabController(length: 3, vsync: this);
  }

  @override
  void dispose() {
    _tabCtrl.dispose();
    _amountCtrl.dispose();
    _descCtrl.dispose();
    _bankNameCtrl.dispose();
    _accountNumCtrl.dispose();
    _accountNameCtrl.dispose();
    _depositorCtrl.dispose();
    _slipCtrl.dispose();
    _senderCtrl.dispose();
    _momoRefCtrl.dispose();
    super.dispose();
  }

  Future<void> _submitBankDeposit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      await context.read<AuthProvider>().api!.createBankDeposit(
            amount: double.parse(_amountCtrl.text.trim()),
            bankName: _bankNameCtrl.text.trim(),
            accountNumber: _accountNumCtrl.text.trim(),
            accountName: _accountNameCtrl.text.trim(),
            depositorName: _depositorCtrl.text.trim(),
            slipNumber: _slipCtrl.text.trim(),
            description: _descCtrl.text.trim(),
          );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Bank deposit recorded')),
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

  Future<void> _submitMomoDeposit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      await context.read<AuthProvider>().api!.createMomoTransaction(
            transactionType: 'deposit',
            amount: double.parse(_amountCtrl.text.trim()),
            network: _momoNetwork,
            serviceType: 'cash_in',
            senderNumber: _senderCtrl.text.trim(),
            momoReference: _momoRefCtrl.text.trim(),
            description: _descCtrl.text.trim(),
          );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Mobile Money deposit recorded')),
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

  Future<void> _submitCashDeposit() async {
    if (!_formKey.currentState!.validate()) return;
    setState(() => _loading = true);
    try {
      await context.read<AuthProvider>().api!.createCashTransaction(
            transactionType: 'deposit',
            amount: double.parse(_amountCtrl.text.trim()),
            description: _descCtrl.text.trim(),
          );
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Cash deposit recorded')),
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
        title: const Text('New Deposit'),
        bottom: TabBar(
          controller: _tabCtrl,
          tabs: const [
            Tab(icon: Icon(Icons.account_balance), text: 'Bank'),
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
            _buildBankForm(),
            _buildMomoForm(),
            _buildCashForm(),
          ],
        ),
      ),
    );
  }

  Widget _buildBankForm() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          _amountField(),
          const SizedBox(height: 16),
          TextFormField(
            controller: _bankNameCtrl,
            decoration: const InputDecoration(
              labelText: 'Bank Name *',
              prefixIcon: Icon(Icons.account_balance),
            ),
            validator: (v) => v == null || v.isEmpty ? 'Required' : null,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _accountNumCtrl,
            decoration: const InputDecoration(
              labelText: 'Account Number *',
              prefixIcon: Icon(Icons.tag),
            ),
            keyboardType: TextInputType.number,
            validator: (v) => v == null || v.isEmpty ? 'Required' : null,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _accountNameCtrl,
            decoration: const InputDecoration(
              labelText: 'Account Name *',
              prefixIcon: Icon(Icons.person),
            ),
            textCapitalization: TextCapitalization.words,
            validator: (v) => v == null || v.isEmpty ? 'Required' : null,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _depositorCtrl,
            decoration: const InputDecoration(
              labelText: 'Depositor Name *',
              prefixIcon: Icon(Icons.person_outline),
            ),
            textCapitalization: TextCapitalization.words,
            validator: (v) => v == null || v.isEmpty ? 'Required' : null,
          ),
          const SizedBox(height: 16),
          TextFormField(
            controller: _slipCtrl,
            decoration: const InputDecoration(
              labelText: 'Slip Number (optional)',
              prefixIcon: Icon(Icons.receipt),
            ),
          ),
          const SizedBox(height: 16),
          _descriptionField(),
          const SizedBox(height: 24),
          _submitButton('Record Bank Deposit', _submitBankDeposit),
        ],
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
            controller: _senderCtrl,
            decoration: const InputDecoration(
              labelText: 'Sender Number *',
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
          _submitButton('Record MoMo Deposit', _submitMomoDeposit),
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
          _submitButton('Record Cash Deposit', _submitCashDeposit),
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
