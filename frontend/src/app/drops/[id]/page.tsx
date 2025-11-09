"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

export default function DropClaimPage() {
  const params = useParams();
  const dropId = params.id;
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleClaim() {
    setLoading(true);
    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/drops/${dropId}/claim`, {
        method: "POST",
        credentials: "include",
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Claim failed");
      }
      const data = await res.json();
      setMessage(`🎉 Claim successful! Your code: ${data.claim_code}`);
    } catch (e: any) {
      setMessage(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="p-8 flex flex-col gap-4 items-center">
      <h1 className="text-2xl font-bold">Claim Drop</h1>
      <button
        onClick={handleClaim}
        disabled={loading}
        className="bg-green-600 text-white px-4 py-2 rounded disabled:opacity-50"
      >
        {loading ? "Claiming..." : "Claim Now"}
      </button>
      {message && <p className="mt-4 text-lg">{message}</p>}
    </main>
  );
}
