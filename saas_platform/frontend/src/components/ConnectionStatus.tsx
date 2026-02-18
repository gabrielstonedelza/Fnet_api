"use client";

interface Props {
  status: string;
}

export default function ConnectionStatus({ status }: Props) {
  const isConnected = status === "connected";
  const isError = status === "error";

  return (
    <div className="flex items-center gap-2 text-sm">
      <div
        className={`w-2.5 h-2.5 rounded-full ${
          isConnected
            ? "bg-emerald-500 animate-pulse"
            : isError
            ? "bg-red-500"
            : "bg-amber-500 animate-pulse"
        }`}
      />
      <span className="text-dark-200">
        {isConnected
          ? "Live"
          : isError
          ? "Connection Error"
          : status === "disconnected"
          ? "Reconnecting..."
          : "Connecting..."}
      </span>
    </div>
  );
}
