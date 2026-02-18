"use client";

import { useEffect, useState, useRef, useCallback } from "react";
import { DashboardWebSocket, WebSocketMessage } from "@/lib/websocket";
import {
  getTransactions,
  getProviderBalances,
  getCustomers,
  getDashboard,
  Transaction,
  ProviderBalance,
  Customer,
  DashboardData,
} from "@/lib/api";
import ProviderBalanceCards from "@/components/ProviderBalanceCards";
import TransactionFeed from "@/components/TransactionFeed";
import CustomerActivity from "@/components/CustomerActivity";
import ConnectionStatus from "@/components/ConnectionStatus";

export default function DashboardPage() {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [balances, setBalances] = useState<ProviderBalance[]>([]);
  const [customers, setCustomers] = useState<Customer[]>([]);
  const [dashboard, setDashboard] = useState<DashboardData | null>(null);
  const [wsStatus, setWsStatus] = useState<string>("connecting");
  const [loading, setLoading] = useState(true);
  const wsRef = useRef<DashboardWebSocket | null>(null);

  const token = typeof window !== "undefined" ? localStorage.getItem("token") || "" : "";
  const companyId = typeof window !== "undefined" ? localStorage.getItem("companyId") || "" : "";

  const fetchInitialData = useCallback(async () => {
    if (!token || !companyId) return;

    try {
      const [txData, balData, custData, dashData] = await Promise.all([
        getTransactions(token, companyId),
        getProviderBalances(token, companyId),
        getCustomers(token, companyId),
        getDashboard(token, companyId),
      ]);
      setTransactions(txData);
      setBalances(balData);
      setCustomers(custData);
      setDashboard(dashData);
    } catch (err) {
      console.error("Failed to fetch initial data:", err);
    } finally {
      setLoading(false);
    }
  }, [token, companyId]);

  const handleTransactionUpdate = useCallback((data: WebSocketMessage) => {
    const tx = data.transaction as Transaction;
    setTransactions((prev) => {
      const existing = prev.findIndex((t) => t.id === tx.id);
      if (existing >= 0) {
        const updated = [...prev];
        updated[existing] = tx;
        return updated;
      }
      return [tx, ...prev];
    });
  }, []);

  const handleCustomerUpdate = useCallback((data: WebSocketMessage) => {
    const cust = data.customer as Customer & { action: string };
    setCustomers((prev) => {
      if (cust.action === "deleted") {
        return prev.filter((c) => c.id !== cust.id);
      }
      const existing = prev.findIndex((c) => c.id === cust.id);
      if (existing >= 0) {
        const updated = [...prev];
        updated[existing] = cust;
        return updated;
      }
      return [cust, ...prev];
    });
  }, []);

  const handleBalanceChange = useCallback((data: WebSocketMessage) => {
    const bal = data.balance as {
      user_id: string;
      user_name: string;
      provider: string;
      balance: string;
      starting_balance: string;
    };
    setBalances((prev) => {
      const existing = prev.findIndex(
        (b) => b.user === bal.user_id && b.provider === bal.provider
      );
      if (existing >= 0) {
        const updated = [...prev];
        updated[existing] = {
          ...updated[existing],
          balance: bal.balance,
          starting_balance: bal.starting_balance,
        };
        return updated;
      }
      return [
        ...prev,
        {
          id: "",
          company: companyId,
          user: bal.user_id,
          user_name: bal.user_name,
          provider: bal.provider,
          provider_display: bal.provider.toUpperCase(),
          starting_balance: bal.starting_balance,
          balance: bal.balance,
          last_updated: new Date().toISOString(),
        },
      ];
    });
  }, [companyId]);

  const handleInitialState = useCallback(
    (data: WebSocketMessage) => {
      const serverBalances = data.balances as Array<{
        user_id: string;
        user_name: string;
        providers: Record<string, { balance: string; starting_balance: string }>;
      }>;

      const flatBalances: ProviderBalance[] = [];
      for (const user of serverBalances) {
        for (const [provider, vals] of Object.entries(user.providers)) {
          flatBalances.push({
            id: `${user.user_id}-${provider}`,
            company: companyId,
            user: user.user_id,
            user_name: user.user_name,
            provider,
            provider_display: provider.replace("_", " ").toUpperCase(),
            starting_balance: vals.starting_balance,
            balance: vals.balance,
            last_updated: new Date().toISOString(),
          });
        }
      }
      if (flatBalances.length > 0) {
        setBalances(flatBalances);
      }
    },
    [companyId]
  );

  useEffect(() => {
    if (!token || !companyId) return;

    fetchInitialData();

    const ws = new DashboardWebSocket(companyId, token);
    wsRef.current = ws;

    ws.on("connection", (data) => {
      setWsStatus(data.status as string);
    });

    ws.on("initial_state", handleInitialState);
    ws.on("transaction_update", handleTransactionUpdate);
    ws.on("customer_update", handleCustomerUpdate);
    ws.on("balance_change", handleBalanceChange);

    ws.connect();

    return () => {
      ws.disconnect();
    };
  }, [
    token,
    companyId,
    fetchInitialData,
    handleInitialState,
    handleTransactionUpdate,
    handleCustomerUpdate,
    handleBalanceChange,
  ]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gold" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-dark-50">Admin Dashboard</h1>
          <p className="text-dark-200 text-sm mt-1">
            Real-time overview of all operations
          </p>
        </div>
        <ConnectionStatus status={wsStatus} />
      </div>

      {/* KPI Summary Cards */}
      {dashboard && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <KPICard
            label="Today's Transactions"
            value={dashboard.total_transactions_today}
          />
          <KPICard
            label="Deposits Today"
            value={`GHS ${Number(dashboard.total_deposits_today || 0).toLocaleString()}`}
          />
          <KPICard
            label="Withdrawals Today"
            value={`GHS ${Number(dashboard.total_withdrawals_today || 0).toLocaleString()}`}
          />
          <KPICard
            label="Fees Today"
            value={`GHS ${Number(dashboard.total_fees_today || 0).toLocaleString()}`}
          />
          <KPICard label="Total Customers" value={dashboard.total_customers} />
          <KPICard
            label="Pending Approvals"
            value={dashboard.pending_approvals}
            highlight={dashboard.pending_approvals > 0}
          />
        </div>
      )}

      <ProviderBalanceCards balances={balances} />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <TransactionFeed transactions={transactions} />
        </div>
        <div>
          <CustomerActivity customers={customers} />
        </div>
      </div>
    </div>
  );
}

function KPICard({
  label,
  value,
  highlight = false,
}: {
  label: string;
  value: string | number;
  highlight?: boolean;
}) {
  return (
    <div className={`card ${highlight ? "border-gold/50 glow-gold" : ""}`}>
      <p className="text-xs text-dark-200 uppercase tracking-wide">{label}</p>
      <p className={`text-2xl font-bold mt-1 ${highlight ? "text-gold" : "text-dark-50"}`}>
        {value}
      </p>
    </div>
  );
}
