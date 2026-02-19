const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface RequestOptions {
  method?: string;
  body?: unknown;
  token?: string;
  companyId?: string;
}

export async function apiRequest<T = unknown>(
  endpoint: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = "GET", body, token, companyId } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Token ${token}`;
  }
  if (companyId) {
    headers["X-Company-ID"] = companyId;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || error.detail || `Request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

// ---------------------------------------------------------------------------
// Auth
// ---------------------------------------------------------------------------

/**
 * Login response can be one of two shapes:
 * 1. Success: { token, user, membership, companies }
 * 2. Company selection required: { requires_company_selection, message, companies }
 */
export interface LoginSuccessResponse {
  token: string;
  user: User;
  membership: Membership;
  companies: Company[];
}

export interface CompanySelectionResponse {
  requires_company_selection: true;
  message: string;
  companies: Company[];
}

export interface TwoFactorRequiredResponse {
  requires_2fa: true;
  temp_token: string;
  message: string;
}

export type LoginResponse =
  | LoginSuccessResponse
  | CompanySelectionResponse
  | TwoFactorRequiredResponse;

export function isCompanySelection(
  resp: LoginResponse
): resp is CompanySelectionResponse {
  return "requires_company_selection" in resp && resp.requires_company_selection === true;
}

export function isTwoFactorRequired(
  resp: LoginResponse
): resp is TwoFactorRequiredResponse {
  return "requires_2fa" in resp && resp.requires_2fa === true;
}

export async function login(
  email: string,
  password: string,
  companyId?: string
): Promise<LoginResponse> {
  return apiRequest<LoginResponse>("/api/v1/auth/login/", {
    method: "POST",
    body: { email, password, ...(companyId && { company_id: companyId }) },
  });
}

export async function verify2FA(
  tempToken: string,
  code: string
): Promise<LoginSuccessResponse> {
  return apiRequest<LoginSuccessResponse>("/api/v1/auth/2fa/verify/", {
    method: "POST",
    body: { temp_token: tempToken, code },
  });
}

export async function logout(token: string) {
  return apiRequest("/api/v1/auth/logout/", { method: "POST", token });
}

export async function getMe(token: string, companyId: string) {
  return apiRequest<{ user: User; memberships: Membership[] }>("/api/v1/auth/me/", {
    token,
    companyId,
  });
}

// ---------------------------------------------------------------------------
// Transactions
// ---------------------------------------------------------------------------
export async function getTransactions(token: string, companyId: string) {
  return apiRequest<Transaction[]>("/api/v1/transactions/", {
    token,
    companyId,
  });
}

// ---------------------------------------------------------------------------
// Provider Balances
// ---------------------------------------------------------------------------
export async function getProviderBalances(token: string, companyId: string) {
  return apiRequest<ProviderBalance[]>("/api/v1/transactions/balances/", {
    token,
    companyId,
  });
}

export async function initializeBalances(
  token: string,
  companyId: string,
  userId: string,
  balances: Record<string, number>
) {
  return apiRequest<ProviderBalance[]>(
    "/api/v1/transactions/balances/initialize/",
    {
      method: "POST",
      token,
      companyId,
      body: { user: userId, balances },
    }
  );
}

// ---------------------------------------------------------------------------
// Customers
// ---------------------------------------------------------------------------
export async function getCustomers(token: string, companyId: string) {
  return apiRequest<Customer[]>("/api/v1/customers/", {
    token,
    companyId,
  });
}

// ---------------------------------------------------------------------------
// Reports
// ---------------------------------------------------------------------------
export async function getDashboard(token: string, companyId: string) {
  return apiRequest<DashboardData>("/api/v1/reports/dashboard/", {
    token,
    companyId,
  });
}

// ---------------------------------------------------------------------------
// Types — match actual Django backend responses
// ---------------------------------------------------------------------------
export interface User {
  id: string;
  email: string;
  full_name: string;
  phone: string;
  avatar: string | null;
  preferred_language: string;
  timezone: string;
  is_active: boolean;
  created_at: string;
  last_login_ip: string | null;
}

export interface Company {
  id: string;
  name: string;
  role: string;
}

export interface Membership {
  id: string;
  user: string;
  user_email: string;
  user_full_name: string;
  user_phone: string;
  user_avatar: string | null;
  company: string;
  company_name: string;
  role: string;
  branch: string | null;
  branch_name: string | null;
  is_active: boolean;
  joined_at: string;
  deactivated_at: string | null;
}

export interface Transaction {
  id: string;
  reference: string;
  transaction_type: string;
  channel: string;
  status: string;
  amount: string;
  fee: string;
  net_amount: string;
  currency: string;
  customer_name: string | null;
  initiated_by_name: string | null;
  created_at: string;
}

export interface ProviderBalance {
  id: string;
  company: string;
  user: string;
  user_name: string;
  provider: string;
  provider_display: string;
  starting_balance: string;
  balance: string;
  last_updated: string;
}

export interface Customer {
  id: string;
  full_name: string;
  phone: string;
  status: string;
  kyc_status: string;
  registered_by: string | null;
  created_at: string;
}

/** Matches the actual response from /api/v1/reports/dashboard/ */
export interface DashboardData {
  total_transactions_today: number;
  total_deposits_today: string;
  total_withdrawals_today: string;
  total_fees_today: string;
  pending_approvals: number;
  total_customers: number;
  total_active_users: number;
  transactions_by_channel: Record<string, number>;
  transactions_by_status: Record<string, number>;
  recent_transactions: Transaction[];
  top_agents: Array<{
    user_id: string;
    name: string;
    transaction_count: number;
    total_volume: string;
  }>;
}
