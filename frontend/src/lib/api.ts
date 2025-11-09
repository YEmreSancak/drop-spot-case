export const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchDrops() {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/drops`);
  if (!res.ok) throw new Error("Failed to fetch drops");
  return res.json();
}

export async function signup(email: string, password: string) {
  const res = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) throw new Error("Signup failed");
  return res.json();
}

export async function fetchDropDetail(id: string) {
  const res = await fetch(`${API_URL}/drops/${id}`);
  if (!res.ok) throw new Error("Drop not found");
  return res.json();
}

export async function joinWaitlist(dropId: number) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/drops/${dropId}/join`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to join");
}

export async function leaveWaitlist(dropId: number) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/drops/${dropId}/leave`, {
    method: "POST",
    credentials: "include",
  });
  if (!res.ok) throw new Error("Failed to leave");
}
