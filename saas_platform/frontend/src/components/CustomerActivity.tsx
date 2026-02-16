"use client";

import { useState, useEffect, useRef } from "react";
import { Customer } from "@/lib/api";

interface Props {
  customers: Customer[];
}

export default function CustomerActivity({ customers }: Props) {
  const prevCountRef = useRef(customers.length);
  const [newIds, setNewIds] = useState<Set<string>>(new Set());

  // Track new customers for highlight animation
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
      <h2 className="text-lg font-semibold text-gray-900 mb-4">
        Customer Activity
        <span className="text-sm font-normal text-gray-500 ml-2">(live)</span>
      </h2>

      <div className="space-y-2 max-h-[500px] overflow-y-auto">
        {customers.length === 0 ? (
          <p className="text-gray-400 text-center py-8">No customers yet</p>
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

      <div className="mt-4 pt-3 border-t border-gray-100">
        <p className="text-xs text-gray-500 text-center">
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
    verified: "bg-green-100 text-green-800",
    pending: "bg-yellow-100 text-yellow-800",
    rejected: "bg-red-100 text-red-800",
  }[cust.kyc_status] || "bg-gray-100 text-gray-800";

  const statusColor = {
    active: "bg-green-500",
    inactive: "bg-gray-400",
    blocked: "bg-red-500",
  }[cust.status] || "bg-gray-400";

  return (
    <div
      className={`flex items-center justify-between p-3 rounded-lg border transition-all ${
        isNew
          ? "animate-slide-in bg-green-50 border-green-200"
          : "bg-white border-gray-100 hover:bg-gray-50"
      }`}
    >
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-full bg-gray-200 flex items-center justify-center text-sm font-bold text-gray-600">
          {cust.full_name
            .split(" ")
            .map((n) => n[0])
            .join("")
            .slice(0, 2)
            .toUpperCase()}
        </div>
        <div>
          <div className="flex items-center gap-2">
            <span className="text-sm font-medium text-gray-900">
              {cust.full_name}
            </span>
            <div className={`w-2 h-2 rounded-full ${statusColor}`} />
          </div>
          <p className="text-xs text-gray-500">{cust.phone}</p>
        </div>
      </div>
      <div className="text-right">
        <span
          className={`text-[10px] font-medium px-2 py-0.5 rounded-full ${kycBadge}`}
        >
          KYC: {cust.kyc_status}
        </span>
        {cust.created_at && (
          <p className="text-[10px] text-gray-400 mt-1">
            {new Date(cust.created_at).toLocaleDateString()}
          </p>
        )}
      </div>
    </div>
  );
}
