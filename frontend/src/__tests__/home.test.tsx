import { render, screen, waitFor } from "@testing-library/react";
import HomePage from "../app/page";
import * as api from "../lib/api"; // fetchDrops burada tanımlı olmalı

jest.mock("../lib/api");

describe("HomePage", () => {
  it("renders header", async () => {
    (api.fetchDrops as jest.Mock).mockResolvedValueOnce([
      { id: 1, title: "DropSpot Limited Edition" },
    ]);

    render(<HomePage />);

    await waitFor(() => {
      expect(screen.getByText(/DropSpot/i)).toBeInTheDocument();
    });
  });
});
