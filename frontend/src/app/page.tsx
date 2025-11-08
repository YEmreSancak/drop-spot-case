"use client";

import { useEffect, useState } from "react";
import { fetchDrops } from "@/lib/api";

export default function HomePage() {
  const [drops, setDrops] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDrops()
      .then(setDrops)
      .catch(() => setError("Failed to load drops"));
  }, []);

  if (error) return <p className="text-red-500">{error}</p>;

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Active Drops</h1>
      <ul>
        {drops.length === 0 && <li>No active drops found.</li>}
        {drops.map((drop) => (
          <li key={drop.id} className="border p-4 rounded mb-2">
            <a href={`/drops/${drop.id}`} className="text-blue-600 hover:underline">
              {drop.title}
            </a>
            <p>{drop.description}</p>
          </li>
        ))}
      </ul>
    </main>
  );
}
