"use client";

import { useState, useEffect, useRef } from "react";
import { ProviderBalance } from "@/lib/api";

// Provider branding — adapted for dark theme
const PROVIDER_CONFIG: Record<
  string,
  { color: string; bgColor: string; icon: string }
> = {
  mtn: { color: "text-yellow-400", bgColor: "bg-yellow-900/30 border-yellow-800/30", icon: "M" },
  vodafone: { color: "text-red-400", bgColor: "bg-red-900/30 border-red-800/30", icon: "V" },
  airtel: { color: "text-orange-400", bgColor: "bg-orange-900/30 border-orange-800/30", icon: "A" },
  tigo: { color: "text-blue-400", bgColor: "bg-blue-900/30 border-blue-800/30", icon: "T" },
  ecobank: { color: "text-sky-400", bgColor: "bg-sky-900/30 border-sky-800/30", icon: "E" },
  fidelity: { color: "text-emerald-400", bgColor: "bg-emerald-900/30 border-emerald-800/30", icon: "F" },
  cal_bank: { color: "text-purple-400", bgColor: "bg-purple-900/30 border-purple-800/30", icon: "C" },
};

interface Props {
  balances: ProviderBalance[];
}

export default function ProviderBalanceCards({ balances }: Props) {
  const userBalances: Record<
    string,
    { user_name: string; providers: ProviderBalance[] }
  > = {};

  for (const b of balances) {
    if (!userBalances[b.user]) {
      userBalances[b.user] = { user_name: b.user_name, providers: [] };
    }
    userBalances[b.user].providers.push(b);
  }

  if (balances.length === 0) {
    return (
      <div className="card text-center text-dark-200 py-8">
        <p className="text-lg font-medium">No Provider Balances Set</p>
        <p className="text-sm mt-1">
          Use the API to initialize starting balances for agents
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-dark-50">
        Provider Balances
        <span className="text-sm font-normal text-dark-200 ml-2">
          (live updating)
        </span>
      </h2>

      {Object.entries(userBalances).map(([userId, { user_name, providers }]) => (
        <div key={userId} className="card">
          <h3 className="text-sm font-semibold text-gold mb-3">
            {user_name}
          </h3>
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3">
            {providers.map((b) => (
              <BalanceCard key={`${b.user}-${b.provider}`} balance={b} />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function BalanceCard({ balance }: { balance: ProviderBalance }) {
  const config = PROVIDER_CONFIG[balance.provider] || {
    color: "text-dark-200",
    bgColor: "bg-dark-500 border-dark-400",
    icon: "?",
  };

  const [flash, setFlash] = useState(false);
  const prevBalance = useRef(balance.balance);

  useEffect(() => {
    if (prevBalance.current !== balance.balance) {
      setFlash(true);
      prevBalance.current = balance.balance;
      const timer = setTimeout(() => setFlash(false), 1500);
      return () => clearTimeout(timer);
    }
  }, [balance.balance]);

  const currentBal = parseFloat(balance.balance);
  const startBal = parseFloat(balance.starting_balance);
  const diff = currentBal - startBal;
  const isUp = diff > 0;
  const isDown = diff < 0;

  return (
    <div
      className={`rounded-lg border p-3 transition-all duration-300 ${
        config.bgColor
      } ${flash ? "ring-2 ring-gold scale-105" : ""}`}
    >
      <div className="flex items-center gap-2 mb-2">
        <div
          className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold bg-dark-500 ${config.color}`}
        >
          {config.icon}
        </div>
        <span className={`text-xs font-semibold ${config.color}`}>
          {balance.provider_display || balance.provider.replace("_", " ").toUpperCase()}
        </span>
      </div>
      <p className={`text-lg font-bold ${config.color}`}>
        GHS {currentBal.toLocaleString(undefined, { minimumFractionDigits: 2 })}
      </p>
      <div className="flex items-center justify-between mt-1">
        <span className="text-[10px] text-dark-300">
          Start: {startBal.toLocaleString()}
        </span>
        {diff !== 0 && (
          <span
            className={`text-[10px] font-medium ${
              isUp ? "text-emerald-400" : isDown ? "text-red-400" : ""
            }`}
          >
            {isUp ? "+" : ""}
            {diff.toLocaleString(undefined, { minimumFractionDigits: 2 })}
          </span>
        )}
      </div>
    </div>
  );
}
