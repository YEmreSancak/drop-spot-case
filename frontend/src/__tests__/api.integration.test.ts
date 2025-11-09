describe("Backend API Integration", () => {
  it("should connect to backend health endpoint", async () => {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/health`);
    expect(response.ok).toBe(true);
  });
});
