"use client";

import { useState, useEffect, useRef } from "react";
import { Transaction } from "@/lib/api";

interface Props {
  transactions: Transaction[];
}

export default function TransactionFeed({ transactions }: Props) {
  const [filter, setFilter] = useState<string>("all");
  const prevCountRef = useRef(transactions.length);
  const [newIds, setNewIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (transactions.length > prevCountRef.current) {
      const newTxIds = new Set(
        transactions.slice(0, transactions.length - prevCountRef.current).map((t) => t.id)
      );
      setNewIds(newTxIds);
      const timer = setTimeout(() => setNewIds(new Set()), 3000);
      prevCountRef.current = transactions.length;
      return () => clearTimeout(timer);
    }
    prevCountRef.current = transactions.length;
  }, [transactions]);

  const filtered =
    filter === "all"
      ? transactions
      : transactions.filter((t) => t.transaction_type === filter);

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-dark-50">
          Transaction Feed
          <span className="text-sm font-normal text-dark-200 ml-2">
            (live)
          </span>
        </h2>
        <div className="flex gap-2">
          {["all", "deposit", "withdrawal", "transfer"].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`text-xs px-3 py-1 rounded-full transition-colors ${
                filter === f
                  ? "bg-gold text-dark font-semibold"
                  : "bg-dark-500 text-dark-200 hover:bg-dark-400"
              }`}
            >
              {f.charAt(0).toUpperCase() + f.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="space-y-2 max-h-[500px] overflow-y-auto">
        {filtered.length === 0 ? (
          <p className="text-dark-300 text-center py-8">No transactions yet</p>
        ) : (
          filtered.slice(0, 50).map((tx) => (
            <TransactionRow
              key={tx.id}
              transaction={tx}
              isNew={newIds.has(tx.id)}
            />
          ))
        )}
      </div>
    </div>
  );
}

function TransactionRow({
  transaction: tx,
  isNew,
}: {
  transaction: Transaction;
  isNew: boolean;
}) {
  const isDeposit = tx.transaction_type === "deposit";
  const isWithdrawal = tx.transaction_type === "withdrawal";

  const statusBadge = {
    completed: "badge-completed",
    pending: "badge-pending",
    rejected: "bg-red-900/40 text-red-400 text-xs font-medium px-2.5 py-0.5 rounded-full border border-red-800/30",
    reversed: "bg-dark-500 text-dark-200 text-xs font-medium px-2.5 py-0.5 rounded-full border border-dark-400",
    approved: "badge-completed",
    failed: "bg-red-900/40 text-red-400 text-xs font-medium px-2.5 py-0.5 rounded-full border border-red-800/30",
  }[tx.status] || "badge-pending";

  return (
    <div
      className={`flex items-center justify-between p-3 rounded-lg border transition-all ${
        isNew
          ? "animate-slide-in bg-gold/10 border-gold/30"
          : "bg-dark-500/50 border-dark-400 hover:bg-dark-500"
      }`}
    >
      <div className="flex items-center gap-3">
        <div
          className={`w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold ${
            isDeposit
              ? "bg-emerald-900/50 text-emerald-400"
              : isWithdrawal
              ? "bg-red-900/50 text-red-400"
              : "bg-blue-900/50 text-blue-400"
          }`}
        >
          {isDeposit ? "D" : isWithdrawal ? "W" : "T"}
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-dark-50">
              {tx.reference}
            </span>
            <span className={statusBadge}>{tx.status}</span>
          </div>
          <p className="text-xs text-dark-300">
            {tx.customer_name || "Walk-in"} &middot;{" "}
            {tx.initiated_by_name || "System"} &middot;{" "}
            {tx.channel.replace("_", " ")}
          </p>
        </div>
      </div>
      <div className="text-right">
        <p
          className={`text-sm font-bold ${
            isDeposit ? "text-emerald-400" : isWithdrawal ? "text-red-400" : "text-dark-50"
          }`}
        >
          {isDeposit ? "+" : isWithdrawal ? "-" : ""}
          {tx.currency} {Number(tx.amount).toLocaleString(undefined, { minimumFractionDigits: 2 })}
        </p>
        {tx.created_at && (
          <p className="text-[10px] text-dark-300">
            {new Date(tx.created_at).toLocaleTimeString()}
          </p>
        )}
      </div>
    </div>
  );
}
