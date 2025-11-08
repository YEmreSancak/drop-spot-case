"use client";

import { useEffect, useState } from "react";
import { fetchDropDetail } from "@/lib/api";

interface DropDetailProps {
  params: { id: string };
}

export default function DropDetailPage({ params }: DropDetailProps) {
  const [drop, setDrop] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchDropDetail(params.id)
      .then(setDrop)
      .catch(() => setError("Drop not found"));
  }, [params.id]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!drop) return <p>Loading...</p>;

  return (
    <main className="p-8">
      <h1 className="text-3xl font-bold">{drop.title}</h1>
      <p className="mt-2">{drop.description}</p>
    </main>
  );
}
