import { vi } from "vitest";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { baseUrl } from "../api/apiSlice";
import { categoryResponse, categoryResponsePage2 } from "../mocks";
import ListCategory from "./listCategory";
import { delay, http, HttpResponse } from "msw";
import { setupServer } from "msw/node";

export const handlers = [
  http.get(`${baseUrl}/categories`, async ({ request }) => {
    await delay(150);
    const url = new URL(request.url);

    if (url.searchParams.get("page") === "2") {
      return HttpResponse.json(categoryResponsePage2);
    }
    return HttpResponse.json(categoryResponse);
  }),
  http.delete(`${baseUrl}/categories/:id`, async () => {
    await delay(150);
    return HttpResponse.json({ message: "success" }, { status: 204 });
  }),
];

const server = setupServer(...handlers);

describe("listCategory", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<ListCategory />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should render loading state", () => {
    renderWithProviders(<ListCategory />);
    const spinner = screen.getByRole("progressbar");

    expect(spinner).toBeInTheDocument();
  });

  it("should render success state", async () => {
    renderWithProviders(<ListCategory />);

    await vi.waitFor(() => {
      const name = screen.getByText("PaleTurquoise");
      const description = screen.getByText(
        "Explicabo nemo voluptate aut nostrum impedit minus."
      );
      expect(name).toBeInTheDocument();
      expect(description).toBeInTheDocument();
    });
  });

  it("should render error state", async () => {
    server.use(
      http.get(`${baseUrl}/categories`, () => {
        return HttpResponse.json(
          { error: "Failed to fetch categories" },
          { status: 500 }
        );
      })
    );

    renderWithProviders(<ListCategory />);
    await vi.waitFor(() => {
      const errorMessage = screen.getByText("Error fetching categories.");
      expect(errorMessage).toBeInTheDocument();
    });
  });

  it("should render page 2", async () => {
    renderWithProviders(<ListCategory />);

    await vi.waitFor(() => {
      const name = screen.getByText("PaleTurquoise");
      expect(name).toBeInTheDocument();
    });

    const nextPageButton = screen.getByTestId("KeyboardArrowRightIcon");
    fireEvent.click(nextPageButton);

    await vi.waitFor(() => {
      const nextPageName = screen.getByText("SeaGreen");
      expect(nextPageName).toBeInTheDocument();
    });
  });

  it("should handle filter change", async () => {
    renderWithProviders(<ListCategory />);

    await vi.waitFor(() => {
      const name = screen.getByText("PaleTurquoise");
      expect(name).toBeInTheDocument();
    });

    const searchInput = screen.getByText("Search...");
    fireEvent.change(searchInput, { target: { value: "PapayaWhip" } });

    await vi.waitFor(() => {
      const spinner = screen.getByRole("progressbar");
      expect(spinner).toBeInTheDocument();
    });
  });

  it("should handle delete category successfully", async () => {
    renderWithProviders(<ListCategory />);

    await vi.waitFor(() => {
      const name = screen.getByText("PaleTurquoise");
      expect(name).toBeInTheDocument();
    });

    const deleteButton = screen.getAllByTestId("deleteButton")[0];
    fireEvent.click(deleteButton);

    await vi.waitFor(() => {
      const deleteMessage = screen.getByText("Category deleted successfully");
      expect(deleteMessage).toBeInTheDocument();
    });
  });

  it("should fail to delete category", async () => {
    server.use(
      http.delete(`${baseUrl}/categories/:id`, () => {
        return HttpResponse.json(
          { error: "Failed to fetch categories" },
          { status: 500 }
        );
      })
    );
    
    renderWithProviders(<ListCategory />);

    await vi.waitFor(() => {
      const name = screen.getByText("PaleTurquoise");
      expect(name).toBeInTheDocument();
    });

    const deleteButton = screen.getAllByTestId("deleteButton")[0];
    fireEvent.click(deleteButton);

    await vi.waitFor(() => {
      const errorMessage = screen.getByText("Error deleting category");
      expect(errorMessage).toBeInTheDocument();
    });
  });
});
