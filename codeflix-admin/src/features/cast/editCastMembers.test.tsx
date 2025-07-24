import { vi } from "vitest";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { baseUrl } from "../api/apiSlice";
import { delay, http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import EditCastMember from "./editCastMember";

const cast_member = {
  id: 1,
  name: "Test cast member",
  type: 1,
  deleted_at: null,
  created_at: "2023-10-01T00:00:00Z",
  updated_at: "2023-10-01T00:00:00Z",
};

export const handlers = [
  http.get(`${baseUrl}/cast_members/`, async () => {
    await delay(150);
    return HttpResponse.json({data: cast_member}, { status: 200 });
  }),
  http.put(`${baseUrl}/cast_members/:id`, async () => {
    await delay(150);
    return HttpResponse.json({ message: "success" }, { status: 204 });
  }),
];

const server = setupServer(...handlers);

describe("EditCastMember", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<EditCastMember />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle submit", async () => {
    renderWithProviders(<EditCastMember />);

    const nameInput = screen.getByLabelText("Name");
    const submitButton = screen.getByRole("button", { name: "Save" });

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue("Test cast member");
    });

    fireEvent.change(nameInput, { target: { value: "Test cast member changed" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue("Test cast member changed");
      expect(
        screen.getByText("Cast member updated successfully")
      ).toBeInTheDocument();
    });
  });

  it("should handle submit error", async () => {
    server.use(
      http.put(`${baseUrl}/categories/1`, async () => {
        await delay(150);
        return HttpResponse.json({ message: "error" }, { status: 400 });
      })
    );
    renderWithProviders(<EditCastMember />);

    const nameInput = screen.getByLabelText("Name");
    const submitButton = screen.getByRole("button", { name: "Save" });

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue("Test cast member");
    });

    fireEvent.change(nameInput, { target: { value: "Test cast member changed" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(screen.getByText("Cast member not updated")).toBeInTheDocument();
    });
  });
});
