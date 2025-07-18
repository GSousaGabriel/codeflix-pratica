import { vi } from "vitest";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { baseUrl } from "../api/apiSlice";
import { delay, http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import CreateCategory from "./createCategory";

export const handlers = [
  http.post(`${baseUrl}/categories`, async () => {
    await delay(150);
    return HttpResponse.json({ message: "success" }, { status: 201 });
  }),
];

const server = setupServer(...handlers);

describe("createCategory", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<CreateCategory />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle submit", async () => {
    renderWithProviders(<CreateCategory />);

    const nameInput = screen.getByTestId("name");
    const descriptionInput = screen.getByTestId("description");
    const isActiveSwitch = screen.getByTestId("is_active");
    const submitButton = screen.getByRole("button", { name: /save/i });

    fireEvent.change(nameInput, { target: { value: "Test Category" } });
    fireEvent.change(descriptionInput, {
      target: { value: "Test Description" },
    });
    fireEvent.click(isActiveSwitch);
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(
        screen.getByText("Category create successfully")
      ).toBeInTheDocument();
    });
  });

  it("should handle submit error", async () => {
    server.use(
      http.post(`${baseUrl}/categories`, async () => {
        await delay(150);
        return HttpResponse.json({ message: "error" }, { status: 500 });
      })
    );
    renderWithProviders(<CreateCategory />);

    const nameInput = screen.getByTestId("name");
    const descriptionInput = screen.getByTestId("description");
    const isActiveSwitch = screen.getByTestId("is_active");
    const submitButton = screen.getByRole("button", { name: /save/i });

    fireEvent.change(nameInput, { target: { value: "Test Category" } });
    fireEvent.change(descriptionInput, {
      target: { value: "Test Description" },
    });
    fireEvent.click(isActiveSwitch);
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(screen.getByText("Category not created")).toBeInTheDocument();
    });
  });
});
