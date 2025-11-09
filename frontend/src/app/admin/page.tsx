"use client";

import { useEffect, useState } from "react";
import { getAdminDrops, createDrop, deleteDrop } from "@/lib/api";

export default function AdminPage() {
  const [drops, setDrops] = useState<any[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [stock, setStock] = useState(0);
  const [claimStart, setClaimStart] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    getAdminDrops()
      .then(setDrops)
      .catch(() => setError("Failed to fetch drops"));
  }, []);

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    try {
      await createDrop({ title, description, stock, claim_start: claimStart });
      const updated = await getAdminDrops();
      setDrops(updated);
      setTitle("");
      setDescription("");
      setStock(0);
      setClaimStart("");
    } catch {
      setError("Failed to create drop");
    }
  }

  async function handleDelete(id: number) {
    try {
      await deleteDrop(id);
      setDrops((prev) => prev.filter((d) => d.id !== id));
    } catch {
      setError("Failed to delete drop");
    }
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Admin Panel</h1>

      <form onSubmit={handleCreate} className="flex flex-col gap-2 max-w-md mb-8">
        <input
          type="text"
          placeholder="Title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border p-2 rounded"
          required
        />
        <textarea
          placeholder="Description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="border p-2 rounded"
        />
        <input
          type="number"
          placeholder="Stock"
          value={stock}
          onChange={(e) => setStock(Number(e.target.value))}
          className="border p-2 rounded"
        />
        <input
          type="datetime-local"
          value={claimStart}
          onChange={(e) => setClaimStart(e.target.value)}
          className="border p-2 rounded"
        />
        <button type="submit" className="bg-blue-600 text-white p-2 rounded">
          Add Drop
        </button>
      </form>

      {error && <p className="text-red-500 mb-4">{error}</p>}

      <ul>
        {drops.map((drop) => (
          <li key={drop.id} className="border-b py-2 flex justify-between items-center">
            <span>{drop.title}</span>
            <button
              onClick={() => handleDelete(drop.id)}
              className="bg-red-500 text-white px-3 py-1 rounded"
            >
              Delete
            </button>
          </li>
        ))}
      </ul>
    </main>
  );
}
