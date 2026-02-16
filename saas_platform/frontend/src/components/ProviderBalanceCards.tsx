"use client";

import { useState, useEffect, useRef } from "react";
import { ProviderBalance } from "@/lib/api";

// Provider branding
const PROVIDER_CONFIG: Record<
  string,
  { color: string; bgColor: string; icon: string }
> = {
  mtn: { color: "text-yellow-700", bgColor: "bg-yellow-50 border-yellow-200", icon: "M" },
  vodafone: { color: "text-red-700", bgColor: "bg-red-50 border-red-200", icon: "V" },
  airtel: { color: "text-red-600", bgColor: "bg-orange-50 border-orange-200", icon: "A" },
  tigo: { color: "text-blue-700", bgColor: "bg-blue-50 border-blue-200", icon: "T" },
  ecobank: { color: "text-blue-800", bgColor: "bg-sky-50 border-sky-200", icon: "E" },
  fidelity: { color: "text-green-700", bgColor: "bg-green-50 border-green-200", icon: "F" },
  cal_bank: { color: "text-purple-700", bgColor: "bg-purple-50 border-purple-200", icon: "C" },
};

interface Props {
  balances: ProviderBalance[];
}

export default function ProviderBalanceCards({ balances }: Props) {
  // Group balances by user
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
      <div className="card text-center text-gray-500 py-8">
        <p className="text-lg font-medium">No Provider Balances Set</p>
        <p className="text-sm mt-1">
          Use the API to initialize starting balances for agents
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-semibold text-gray-900">
        Provider Balances
        <span className="text-sm font-normal text-gray-500 ml-2">
          (live updating)
        </span>
      </h2>

      {Object.entries(userBalances).map(([userId, { user_name, providers }]) => (
        <div key={userId} className="card">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">
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
    color: "text-gray-700",
    bgColor: "bg-gray-50 border-gray-200",
    icon: "?",
  };

  const [flash, setFlash] = useState(false);
  const prevBalance = useRef(balance.balance);

  // Flash animation when balance changes
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
      } ${flash ? "ring-2 ring-blue-400 scale-105" : ""}`}
    >
      <div className="flex items-center gap-2 mb-2">
        <div
          className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-bold text-white ${
            config.color.replace("text-", "bg-")
          }`}
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
        <span className="text-[10px] text-gray-500">
          Start: {startBal.toLocaleString()}
        </span>
        {diff !== 0 && (
          <span
            className={`text-[10px] font-medium ${
              isUp ? "text-green-600" : isDown ? "text-red-600" : ""
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
