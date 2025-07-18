import { vi } from "vitest";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { baseUrl } from "../api/apiSlice";
import { delay, http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import EditCategory from "./editCategory";

const category = {
  id: 1,
  name: "Test Category",
  description: "This is a test category",
  is_active: true,
  deleted_at: null,
  created_at: "2023-10-01T00:00:00Z",
  updated_at: "2023-10-01T00:00:00Z",
};

export const handlers = [
  http.get(`${baseUrl}/categories/undefined`, async () => {
    await delay(150);
    return HttpResponse.json(category);
  }),
  http.put(`${baseUrl}/categories/:id`, async () => {
    await delay(150);
    return HttpResponse.json({ message: "success" }, { status: 204 });
  }),
];

const server = setupServer(...handlers);

describe("editCategory", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<EditCategory />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle submit", async () => {
    renderWithProviders(<EditCategory />);

    const nameInput = screen.getByLabelText("Name");
    const descriptionInput = screen.getByLabelText("Description");
    const submitButton = screen.getByRole("button", { name: "Save" });

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue("Test Category");
      expect(descriptionInput).toHaveValue("This is a test category");
    });

    fireEvent.change(nameInput, { target: { value: "Test Category changed" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue("Test Category changed");
      expect(
        screen.getByText("Category updated successfully")
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
    renderWithProviders(<EditCategory />);

    const nameInput = screen.getByLabelText("Name");
    const descriptionInput = screen.getByLabelText("Description");
    const submitButton = screen.getByRole("button", { name: "Save" });

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue("Test Category");
      expect(descriptionInput).toHaveValue("This is a test category");
    });

    fireEvent.change(nameInput, { target: { value: "Test Category changed" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(screen.getByText("Category not updated")).toBeInTheDocument();
    });
  });
});
