"use client";

import { useState, useEffect, useRef } from "react";
import { Customer } from "@/lib/api";

interface Props {
  customers: Customer[];
}

export default function CustomerActivity({ customers }: Props) {
  const prevCountRef = useRef(customers.length);
  const [newIds, setNewIds] = useState<Set<string>>(new Set());

  useEffect(() => {
    if (customers.length > prevCountRef.current) {
      const newCustIds = new Set(
        customers
          .slice(0, customers.length - prevCountRef.current)
          .map((c) => c.id)
      );
      setNewIds(newCustIds);
      const timer = setTimeout(() => setNewIds(new Set()), 3000);
      prevCountRef.current = customers.length;
      return () => clearTimeout(timer);
    }
    prevCountRef.current = customers.length;
  }, [customers]);

  return (
    <div className="card">
      <h2 className="text-lg font-semibold text-dark-50 mb-4">
        Customer Activity
        <span className="text-sm font-normal text-dark-200 ml-2">(live)</span>
      </h2>

      <div className="space-y-2 max-h-[500px] overflow-y-auto">
        {customers.length === 0 ? (
          <p className="text-dark-300 text-center py-8">No customers yet</p>
        ) : (
          customers.slice(0, 30).map((cust) => (
            <CustomerRow
              key={cust.id}
              customer={cust}
              isNew={newIds.has(cust.id)}
            />
          ))
        )}
      </div>

      <div className="mt-4 pt-3 border-t border-dark-400">
        <p className="text-xs text-dark-300 text-center">
          {customers.length} total customer{customers.length !== 1 ? "s" : ""}
        </p>
      </div>
    </div>
  );
}

function CustomerRow({
  customer: cust,
  isNew,
}: {
  customer: Customer;
  isNew: boolean;
}) {
  const kycBadge = {
    verified: "bg-emerald-900/40 text-emerald-400 border border-emerald-800/30",
    pending: "bg-amber-900/40 text-amber-400 border border-amber-800/30",
    rejected: "bg-red-900/40 text-red-400 border border-red-800/30",
  }[cust.kyc_status] || "bg-dark-500 text-dark-200 border border-dark-400";

  const statusColor = {
    active: "bg-emerald-500",
    inactive: "bg-dark-300",
    blocked: "bg-red-500",
  }[cust.status] || "bg-dark-300";

  return (
    <div
      className={`flex items-center justify-between p-3 rounded-lg border transition-all ${
        isNew
          ? "animate-slide-in bg-gold/10 border-gold/30"
          : "bg-dark-500/50 border-dark-400 hover:bg-dark-500"
      }`}
    >
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-full bg-dark-500 flex items-center justify-center text-sm font-bold text-gold">
          {cust.full_name
            .split(" ")
            .map((n) => n[0])
            .join("")
            .slice(0, 2)
            .toUpperCase()}
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-dark-50">
              {cust.full_name}
            </span>
            <div className={`w-2 h-2 rounded-full ${statusColor}`} />
          </div>
          <p className="text-xs text-dark-300">{cust.phone}</p>
        </div>
      </div>
      <div className="text-right">
        <span
          className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${kycBadge}`}
        >
          KYC: {cust.kyc_status}
        </span>
        {cust.created_at && (
          <p className="text-[10px] text-dark-300 mt-1">
            {new Date(cust.created_at).toLocaleDateString()}
          </p>
        )}
      </div>
    </div>
  );
}
