"use client";

import { useEffect, useState } from "react";
import { joinWaitlist, leaveWaitlist, fetchDrops } from "@/lib/api";

interface Drop {
  id: number;
  name: string;
  description: string;
  start_time: string;
  end_time: string;
  joined: boolean;
}

export default function DropListPage() {
  const [drops, setDrops] = useState<Drop[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDrops()
      .then((data) => {
        setDrops(data);
      })
      .catch(() => setError("Failed to load drops"))
      .finally(() => setLoading(false));
  }, []);

  async function handleJoin(dropId: number) {
    try {
      await joinWaitlist(dropId);
      setDrops((prev) =>
        prev.map((d) =>
          d.id === dropId ? { ...d, joined: true } : d
        )
      );
    } catch {
      alert("Failed to join waitlist");
    }
  }

  async function handleLeave(dropId: number) {
    try {
      await leaveWaitlist(dropId);
      setDrops((prev) =>
        prev.map((d) =>
          d.id === dropId ? { ...d, joined: false } : d
        )
      );
    } catch {
      alert("Failed to leave waitlist");
    }
  }

  if (loading) return <p className="p-8">Loading drops...</p>;
  if (error) return <p className="p-8 text-red-500">{error}</p>;

  return (
    <main className="p-8 space-y-4">
      <h1 className="text-3xl font-bold mb-4">Available Drops</h1>
      {drops.length === 0 ? (
        <p>No drops available.</p>
      ) : (
        <div className="grid gap-4">
          {drops.map((drop) => (
            <div
              key={drop.id}
              className="border rounded-lg p-4 shadow-sm flex justify-between items-center"
            >
              <div>
                <h2 className="text-xl font-semibold">{drop.name}</h2>
                <p className="text-gray-600">{drop.description}</p>
              </div>
              <div>
                {drop.joined ? (
                  <button
                    onClick={() => handleLeave(drop.id)}
                    className="bg-red-500 text-white px-3 py-1 rounded"
                  >
                    Leave Waitlist
                  </button>
                ) : (
                  <button
                    onClick={() => handleJoin(drop.id)}
                    className="bg-blue-600 text-white px-3 py-1 rounded"
                  >
                    Join Waitlist
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}
