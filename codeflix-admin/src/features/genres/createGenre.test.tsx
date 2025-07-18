import { delay, http, HttpResponse } from "msw";
import { baseUrl } from "../api/apiSlice";
import { setupServer } from "msw/node";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { vi } from "vitest";
import { categoryResponse } from "../mocks";
import CreateGenre from "./createGenre";

const mockData = {
  id: "1",
  name: "test",
  created_at: "2023-01-01T00:00:00Z",
  updated_at: "2023-01-01T00:00:00Z",
  deleted_at: null,
  is_active: true,
  categories: [],
  description: "",
  pivot: { genre_id: "1", category_id: "1" },
};

const handlers = [
  http.get(`${baseUrl}/categories`, async () => {
    await delay(150)
    return HttpResponse.json(categoryResponse, { status: 200 });
  }),
  http.post(`${baseUrl}/genres`, async () => {
    await delay(150)
    return HttpResponse.json({ success: true }, { status: 201 });
  }),
];

const server = setupServer(...handlers);

describe("createGenre", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<CreateGenre />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should validate and save on submit", async () => {
    renderWithProviders(<CreateGenre />);

    const nameInput = screen.getByTestId("Name");
    const submitButton = screen.getByRole("button", { name: "Save" });

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue(mockData.name);
    });

    fireEvent.change(nameInput, { target: { value: "New Genre" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      const message = screen.getByText("Genre create successfully");
      expect(message).toBeInTheDocument();
    });
  });

  it("should give error on submit", async () => {
    server.use(
      http.post(`${baseUrl}/genres/:id`, () => {
        return HttpResponse.json({ success: false }, { status: 400 });
      })
    );
    renderWithProviders(<CreateGenre />);

    const nameInput = screen.getByTestId("Name");
    const submitButton = screen.getByRole("button", { name: "Save" });

    await vi.waitFor(() => {
      expect(nameInput).toHaveValue(mockData.name);
    });

    fireEvent.change(nameInput, { target: { value: "New Genre" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      const message = screen.getByText("Genre not created");
      expect(message).toBeInTheDocument();
    });
  });
});
