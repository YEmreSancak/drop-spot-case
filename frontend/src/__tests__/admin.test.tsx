import { render, screen, waitFor } from "@testing-library/react";
import AdminPage from "@/app/admin/page";
import "@testing-library/jest-dom";

// API çağrılarını mocklayalım
jest.mock("@/lib/api", () => ({
  getAdminDrops: jest.fn().mockResolvedValue([
    { id: 1, title: "Test Drop", description: "Mock desc", stock: 5, claim_start: "2025-11-09T10:00:00" },
  ]),
  createDrop: jest.fn(),
  deleteDrop: jest.fn(),
  updateDrop: jest.fn(),
}));

describe("AdminPage", () => {
  it("renders admin panel title and drop list", async () => {
    render(<AdminPage />);
    expect(screen.getByText(/Admin Panel/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText("Test Drop")).toBeInTheDocument();
    });
  });

  it("has add drop form inputs", () => {
    render(<AdminPage />);
    expect(screen.getByPlaceholderText(/Title/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Stock/i)).toBeInTheDocument();
  });
});
