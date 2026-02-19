import 'package:flutter/material.dart';

/// Merchant+ Dark + Gold theme
/// ─────────────────────────────
/// Background:  #0F1117  (near-black)
/// Surface:     #1A1D27  (dark card)
/// Elevated:    #242836  (raised elements)
/// Gold:        #D4A843  (primary accent)
/// Gold Light:  #F5D778  (highlights)
/// Gold Dark:   #A68425  (pressed states)
/// Text:        #F1F1F4  (primary text)
/// Text Muted:  #8B8FA3  (secondary text)
/// Success:     #34D399  (green)
/// Danger:      #F87171  (red)
/// Warning:     #FBBF24  (amber)
/// Border:      #2A2E3B
class MerchantTheme {
  // Primary gold
  static const Color primary = Color(0xFFD4A843);
  static const Color primaryLight = Color(0xFFF5D778);
  static const Color primaryDark = Color(0xFFA68425);

  // Backgrounds
  static const Color background = Color(0xFF0F1117);
  static const Color surface = Color(0xFF1A1D27);
  static const Color surfaceElevated = Color(0xFF242836);
  static const Color border = Color(0xFF2A2E3B);

  // Text
  static const Color textPrimary = Color(0xFFF1F1F4);
  static const Color textSecondary = Color(0xFF8B8FA3);
  static const Color textMuted = Color(0xFF5C6070);

  // Semantic
  static const Color accent = Color(0xFF34D399);
  static const Color danger = Color(0xFFF87171);
  static const Color warning = Color(0xFFFBBF24);
  static const Color info = Color(0xFF60A5FA);

  static ThemeData get darkTheme => ThemeData(
        useMaterial3: true,
        brightness: Brightness.dark,
        scaffoldBackgroundColor: background,
        colorScheme: const ColorScheme.dark(
          primary: primary,
          secondary: primaryLight,
          surface: surface,
          error: danger,
          onPrimary: Color(0xFF1A1D27),
          onSecondary: Color(0xFF1A1D27),
          onSurface: textPrimary,
          onError: Colors.white,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: surface,
          foregroundColor: textPrimary,
          elevation: 0,
          centerTitle: false,
          titleTextStyle: TextStyle(
            color: primary,
            fontSize: 20,
            fontWeight: FontWeight.bold,
          ),
          iconTheme: IconThemeData(color: primary),
        ),
        elevatedButtonTheme: ElevatedButtonThemeData(
          style: ElevatedButton.styleFrom(
            backgroundColor: primary,
            foregroundColor: background,
            minimumSize: const Size(double.infinity, 48),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
            textStyle: const TextStyle(
              fontWeight: FontWeight.w700,
              fontSize: 15,
            ),
          ),
        ),
        outlinedButtonTheme: OutlinedButtonThemeData(
          style: OutlinedButton.styleFrom(
            foregroundColor: primary,
            side: const BorderSide(color: border),
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(12),
            ),
          ),
        ),
        inputDecorationTheme: InputDecorationTheme(
          filled: true,
          fillColor: surfaceElevated,
          border: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: border),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: border),
          ),
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: primary, width: 2),
          ),
          errorBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(12),
            borderSide: const BorderSide(color: danger),
          ),
          labelStyle: const TextStyle(color: textSecondary),
          hintStyle: const TextStyle(color: textMuted),
          prefixIconColor: textSecondary,
          suffixIconColor: textSecondary,
          contentPadding:
              const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        ),
        cardTheme: CardTheme(
          elevation: 0,
          color: surface,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
            side: const BorderSide(color: border),
          ),
        ),
        dividerTheme: const DividerThemeData(
          color: border,
          thickness: 1,
        ),
        listTileTheme: const ListTileThemeData(
          textColor: textPrimary,
          iconColor: textSecondary,
        ),
        popupMenuTheme: PopupMenuThemeData(
          color: surfaceElevated,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(12),
            side: const BorderSide(color: border),
          ),
        ),
        tabBarTheme: TabBarTheme(
          labelColor: primary,
          unselectedLabelColor: textSecondary,
          indicatorColor: primary,
          dividerColor: border,
        ),
        snackBarTheme: SnackBarThemeData(
          backgroundColor: surfaceElevated,
          contentTextStyle: const TextStyle(color: textPrimary),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          behavior: SnackBarBehavior.floating,
        ),
        progressIndicatorTheme: const ProgressIndicatorThemeData(
          color: primary,
        ),
        floatingActionButtonTheme: const FloatingActionButtonThemeData(
          backgroundColor: primary,
          foregroundColor: background,
        ),
        textTheme: const TextTheme(
          bodyLarge: TextStyle(color: textPrimary),
          bodyMedium: TextStyle(color: textPrimary),
          bodySmall: TextStyle(color: textSecondary),
          titleLarge: TextStyle(color: textPrimary, fontWeight: FontWeight.bold),
          titleMedium: TextStyle(color: textPrimary),
          labelLarge: TextStyle(color: textPrimary),
        ),
      );
}
