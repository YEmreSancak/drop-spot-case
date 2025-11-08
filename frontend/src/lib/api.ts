export const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function fetchDrops() {
  const res = await fetch(`${API_URL}/drops`);
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
