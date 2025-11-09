"use client";

import { useEffect, useState } from "react";
import { getAdminDrops, createDrop, deleteDrop, updateDrop } from "@/lib/api";

export default function AdminPage() {
  const [drops, setDrops] = useState<any[]>([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [stock, setStock] = useState(0);
  const [claimStart, setClaimStart] = useState("");
  const [error, setError] = useState("");
  const [editingDrop, setEditingDrop] = useState<any | null>(null);

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

  async function handleEdit(e: React.FormEvent) {
    e.preventDefault();
    if (!editingDrop) return;
    try {
      await updateDrop(editingDrop.id, {
        title: editingDrop.title,
        description: editingDrop.description,
        stock: editingDrop.stock,
        claim_start: editingDrop.claim_start,
      });
      const updated = await getAdminDrops();
      setDrops(updated);
      setEditingDrop(null);
    } catch {
      setError("Failed to update drop");
    }
  }

  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold mb-4">Admin Panel</h1>

      {/* Create Form */}
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

      {/* Drop List */}
      <ul>
        {drops.map((drop) => (
          <li key={drop.id} className="border-b py-2 flex justify-between items-center">
            <span>{drop.title}</span>
            <div className="flex gap-2">
              <button
                onClick={() => setEditingDrop(drop)}
                className="bg-yellow-500 text-white px-3 py-1 rounded"
              >
                Edit
              </button>
              <button
                onClick={() => handleDelete(drop.id)}
                className="bg-red-500 text-white px-3 py-1 rounded"
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>

      {/* Edit Modal */}
      {editingDrop && (
        <div className="fixed inset-0 bg-black bg-opacity-30 flex justify-center items-center">
          <div className="bg-white p-6 rounded shadow-md w-full max-w-md">
            <h2 className="text-xl mb-4">Edit Drop</h2>
            <form onSubmit={handleEdit} className="flex flex-col gap-2">
              <input
                type="text"
                value={editingDrop.title}
                onChange={(e) =>
                  setEditingDrop({ ...editingDrop, title: e.target.value })
                }
                className="border p-2 rounded"
              />
              <textarea
                value={editingDrop.description}
                onChange={(e) =>
                  setEditingDrop({ ...editingDrop, description: e.target.value })
                }
                className="border p-2 rounded"
              />
              <input
                type="number"
                value={editingDrop.stock}
                onChange={(e) =>
                  setEditingDrop({ ...editingDrop, stock: Number(e.target.value) })
                }
                className="border p-2 rounded"
              />
              <input
                type="datetime-local"
                value={editingDrop.claim_start}
                onChange={(e) =>
                  setEditingDrop({ ...editingDrop, claim_start: e.target.value })
                }
                className="border p-2 rounded"
              />
              <div className="flex justify-end gap-2 mt-4">
                <button
                  type="button"
                  onClick={() => setEditingDrop(null)}
                  className="bg-gray-300 px-4 py-2 rounded"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-green-600 text-white px-4 py-2 rounded"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </main>
  );
}
