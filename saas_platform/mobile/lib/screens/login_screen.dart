import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../config/theme.dart';
import '../providers/auth_provider.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailCtrl = TextEditingController();
  final _passwordCtrl = TextEditingController();
  final _formKey = GlobalKey<FormState>();
  bool _obscure = true;

  // 2FA OTP controllers (6 digits)
  final List<TextEditingController> _otpControllers =
      List.generate(6, (_) => TextEditingController());
  final List<FocusNode> _otpFocusNodes =
      List.generate(6, (_) => FocusNode());
  bool _showBackupInput = false;
  final _backupCtrl = TextEditingController();

  @override
  void dispose() {
    _emailCtrl.dispose();
    _passwordCtrl.dispose();
    for (final c in _otpControllers) {
      c.dispose();
    }
    for (final n in _otpFocusNodes) {
      n.dispose();
    }
    _backupCtrl.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    final auth = context.read<AuthProvider>();
    auth.clearError();

    final success = await auth.login(
      _emailCtrl.text.trim(),
      _passwordCtrl.text,
    );

    if (success && mounted) {
      // Navigation is handled by Consumer in main.dart
    }
    // If !success and requires2FA, the UI below will show 2FA input
    // If !success and pendingCompanies != null, the UI below will show company selection
  }

  Future<void> _handleCompanySelect(String companyId) async {
    final auth = context.read<AuthProvider>();
    await auth.selectCompany(companyId);
  }

  Future<void> _handle2FAVerify() async {
    final code = _otpControllers.map((c) => c.text).join();
    if (code.length < 6) return;

    final auth = context.read<AuthProvider>();
    auth.clearError();

    final success = await auth.verify2FA(code);
    if (!success && mounted) {
      // Clear OTP fields on failure
      for (final c in _otpControllers) {
        c.clear();
      }
      _otpFocusNodes[0].requestFocus();
    }
  }

  Future<void> _handleBackupVerify() async {
    final code = _backupCtrl.text.trim();
    if (code.isEmpty) return;

    final auth = context.read<AuthProvider>();
    auth.clearError();

    final success = await auth.verify2FA(code);
    if (!success && mounted) {
      _backupCtrl.clear();
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Consumer<AuthProvider>(
              builder: (context, auth, _) {
                // Show 2FA verification
                if (auth.requires2FA) {
                  return _build2FAVerification(auth);
                }
                // Show company selection
                if (auth.pendingCompanies != null) {
                  return _buildCompanySelection(auth);
                }
                // Show login form
                return _buildLoginForm(auth);
              },
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildLoginForm(AuthProvider auth) {
    return Form(
      key: _formKey,
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Logo / brand
          Container(
            width: 72,
            height: 72,
            decoration: BoxDecoration(
              color: MerchantTheme.primary,
              borderRadius: BorderRadius.circular(16),
            ),
            child: const Center(
              child: Text(
                'M+',
                style: TextStyle(
                  color: MerchantTheme.background,
                  fontSize: 28,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ),
          const SizedBox(height: 24),
          const Text(
            'Merchant+',
            style: TextStyle(fontSize: 28, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          const Text(
            'Sign in to your account',
            style: TextStyle(color: MerchantTheme.textSecondary),
          ),
          const SizedBox(height: 32),

          if (auth.error != null) ...[
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: MerchantTheme.danger.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Text(
                auth.error!,
                style: const TextStyle(color: MerchantTheme.danger, fontSize: 14),
              ),
            ),
            const SizedBox(height: 16),
          ],

          TextFormField(
            controller: _emailCtrl,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
              labelText: 'Email',
              prefixIcon: Icon(Icons.email_outlined),
            ),
            validator: (v) {
              if (v == null || v.isEmpty) return 'Email is required';
              if (!v.contains('@')) return 'Enter a valid email';
              return null;
            },
          ),
          const SizedBox(height: 16),

          TextFormField(
            controller: _passwordCtrl,
            obscureText: _obscure,
            decoration: InputDecoration(
              labelText: 'Password',
              prefixIcon: const Icon(Icons.lock_outline),
              suffixIcon: IconButton(
                icon: Icon(_obscure ? Icons.visibility_off : Icons.visibility),
                onPressed: () => setState(() => _obscure = !_obscure),
              ),
            ),
            validator: (v) {
              if (v == null || v.isEmpty) return 'Password is required';
              return null;
            },
          ),
          const SizedBox(height: 24),

          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: auth.loading ? null : _handleLogin,
              child: auth.loading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Text('Sign In', style: TextStyle(fontSize: 16)),
            ),
          ),
        ],
      ),
    );
  }

  Widget _build2FAVerification(AuthProvider auth) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        // Lock icon
        Container(
          width: 64,
          height: 64,
          decoration: BoxDecoration(
            color: MerchantTheme.primary.withOpacity(0.1),
            shape: BoxShape.circle,
            border: Border.all(
              color: MerchantTheme.primary.withOpacity(0.2),
            ),
          ),
          child: const Icon(
            Icons.lock_outlined,
            size: 32,
            color: MerchantTheme.primary,
          ),
        ),
        const SizedBox(height: 24),
        const Text(
          'Two-Factor Authentication',
          style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        Text(
          _showBackupInput
              ? 'Enter your backup recovery code'
              : 'Enter the 6-digit code from your authenticator app',
          textAlign: TextAlign.center,
          style: const TextStyle(color: MerchantTheme.textSecondary),
        ),
        const SizedBox(height: 24),

        if (auth.error != null) ...[
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: MerchantTheme.danger.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              auth.error!,
              style: const TextStyle(color: MerchantTheme.danger, fontSize: 14),
            ),
          ),
          const SizedBox(height: 16),
        ],

        if (!_showBackupInput) ...[
          // 6-digit OTP input boxes
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(6, (index) {
              return Container(
                width: 48,
                height: 56,
                margin: EdgeInsets.only(
                  right: index < 5 ? 8 : 0,
                  left: index == 3 ? 8 : 0,
                ),
                child: TextField(
                  controller: _otpControllers[index],
                  focusNode: _otpFocusNodes[index],
                  keyboardType: TextInputType.number,
                  textAlign: TextAlign.center,
                  maxLength: 1,
                  style: const TextStyle(
                    fontSize: 22,
                    fontWeight: FontWeight.bold,
                  ),
                  decoration: InputDecoration(
                    counterText: '',
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                    focusedBorder: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(12),
                      borderSide: const BorderSide(
                        color: MerchantTheme.primary,
                        width: 2,
                      ),
                    ),
                  ),
                  inputFormatters: [
                    FilteringTextInputFormatter.digitsOnly,
                  ],
                  onChanged: (value) {
                    if (value.isNotEmpty && index < 5) {
                      _otpFocusNodes[index + 1].requestFocus();
                    }
                    // Auto-submit when all 6 filled
                    final fullCode = _otpControllers
                        .map((c) => c.text)
                        .join();
                    if (fullCode.length == 6) {
                      _handle2FAVerify();
                    }
                  },
                ),
              );
            }),
          ),
          const SizedBox(height: 24),

          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: auth.loading ? null : _handle2FAVerify,
              child: auth.loading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Text('Verify', style: TextStyle(fontSize: 16)),
            ),
          ),
        ] else ...[
          // Backup code input
          TextField(
            controller: _backupCtrl,
            textAlign: TextAlign.center,
            textCapitalization: TextCapitalization.characters,
            maxLength: 8,
            style: const TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              letterSpacing: 4,
            ),
            decoration: InputDecoration(
              counterText: '',
              hintText: 'A1B2C3D4',
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
              ),
              focusedBorder: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: const BorderSide(
                  color: MerchantTheme.primary,
                  width: 2,
                ),
              ),
            ),
          ),
          const SizedBox(height: 24),

          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: auth.loading ? null : _handleBackupVerify,
              child: auth.loading
                  ? const SizedBox(
                      height: 20,
                      width: 20,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Text(
                      'Verify Backup Code',
                      style: TextStyle(fontSize: 16),
                    ),
            ),
          ),
        ],

        const SizedBox(height: 16),

        // Toggle between OTP and backup code
        TextButton(
          onPressed: () {
            setState(() {
              _showBackupInput = !_showBackupInput;
            });
            context.read<AuthProvider>().clearError();
          },
          child: Text(
            _showBackupInput
                ? 'Use authenticator code instead'
                : 'Use a backup code instead',
          ),
        ),

        TextButton(
          onPressed: () {
            context.read<AuthProvider>().cancel2FA();
            setState(() {
              _showBackupInput = false;
              for (final c in _otpControllers) {
                c.clear();
              }
              _backupCtrl.clear();
            });
          },
          child: const Text('Back to login'),
        ),
      ],
    );
  }

  Widget _buildCompanySelection(AuthProvider auth) {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Icon(Icons.business, size: 48, color: MerchantTheme.primary),
        const SizedBox(height: 16),
        const Text(
          'Select Company',
          style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
        ),
        const SizedBox(height: 8),
        Text(
          'You belong to multiple companies.\nChoose which one to sign into:',
          textAlign: TextAlign.center,
          style: const TextStyle(color: MerchantTheme.textSecondary),
        ),
        const SizedBox(height: 24),

        if (auth.error != null) ...[
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: MerchantTheme.danger.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Text(
              auth.error!,
              style: const TextStyle(color: MerchantTheme.danger, fontSize: 14),
            ),
          ),
          const SizedBox(height: 16),
        ],

        ...auth.pendingCompanies!.map(
          (company) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: SizedBox(
              width: double.infinity,
              child: OutlinedButton(
                onPressed: auth.loading
                    ? null
                    : () => _handleCompanySelect(company.id),
                style: OutlinedButton.styleFrom(
                  padding: const EdgeInsets.all(16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.business, size: 20),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            company.name,
                            style: const TextStyle(
                              fontWeight: FontWeight.w600,
                              fontSize: 15,
                            ),
                          ),
                          Text(
                            'Role: ${company.role}',
                            style: const TextStyle(
                              color: MerchantTheme.textMuted,
                              fontSize: 12,
                            ),
                          ),
                        ],
                      ),
                    ),
                    const Icon(Icons.chevron_right),
                  ],
                ),
              ),
            ),
          ),
        ),

        const SizedBox(height: 8),
        TextButton(
          onPressed: auth.cancelCompanySelection,
          child: const Text('Back to login'),
        ),

        if (auth.loading) ...[
          const SizedBox(height: 16),
          const CircularProgressIndicator(),
        ],
      ],
    );
  }
}
