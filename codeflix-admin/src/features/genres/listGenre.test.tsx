import { delay, http, HttpResponse } from "msw";
import { baseUrl } from "../api/apiSlice";
import { setupServer } from "msw/node";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { vi } from "vitest";
import ListGenres from "./listGenres";
import { genreResponse, genreResponsePage2 } from "../mocks/genre";
import { categoryResponse } from "../mocks";

const handlers = [
  http.get(`${baseUrl}/genres`, async ({ request }) => {
    const url = new URL(request.url);
    const page = url.searchParams.get("page") || "1";
    await delay(150);

    if (page === "2") {
      return HttpResponse.json(genreResponsePage2, { status: 200 });
    }

    return HttpResponse.json(genreResponse, { status: 200 });
  }),
  http.get(`${baseUrl}/categories`, async () => {
    await delay(150);
    return HttpResponse.json(categoryResponse, { status: 200 });
  }),
  http.delete(`${baseUrl}/genres/1`, async () => {
    await delay(150);
    return HttpResponse.json({ success: true }, { status: 200 });
  }),
];

const server = setupServer(...handlers);

describe("ListGenres", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<ListGenres />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should render loading state", async () => {
    renderWithProviders(<ListGenres />);
    const loading = screen.getByRole("progressbar");
    expect(loading).toBeInTheDocument();
  });

  it("should render error state", async () => {
    server.use(
      http.get(`${baseUrl}/genres`, async () => {
        await delay(150);
        return HttpResponse.json({ message: "error" }, { status: 500 });
      })
    );
    renderWithProviders(<ListGenres />);

    await vi.waitFor(() => {
      const error = screen.getByText("Error fetching genres");
      expect(error).toBeInTheDocument();
    });
  });

  it("should handle changing pages", async () => {
    renderWithProviders(<ListGenres />);

    await vi.waitFor(() => {
      const name = screen.getByText("Norfolk Island");

      expect(name).toBeInTheDocument();
    });
    const nextPageButton = screen.getByRole("button", {
      name: "KeyboardArrowRightIcon",
    });
    fireEvent.click(nextPageButton);

    await vi.waitFor(() => {
      const message = screen.getByText("Norfolk Island 2");
      expect(message).toBeInTheDocument();
    });
  });

  it("should handle filter change", async () => {
    renderWithProviders(<ListGenres />);

    await vi.waitFor(() => {
      const name = screen.getByText("Norfolk Island");
      expect(name).toBeInTheDocument();
    });

    const searchInput = screen.getByText("Search...");
    fireEvent.change(searchInput, { target: { value: "Norfolk Island" } });

    await vi.waitFor(() => {
      const spinner = screen.getByRole("progressbar");
      expect(spinner).toBeInTheDocument();
    });
  });

  it("should handle delete category successfully", async () => {
    renderWithProviders(<ListGenres />);

    await vi.waitFor(() => {
      const name = screen.getByText("Norfolk Island");
      expect(name).toBeInTheDocument();
    });

    const deleteButton = screen.getAllByTestId("deleteButton")[0];
    fireEvent.click(deleteButton);

    await vi.waitFor(() => {
      const deleteMessage = screen.getByText("Genre deleted successfully");
      expect(deleteMessage).toBeInTheDocument();
    });
  });

  it("should fail to delete category", async () => {
    server.use(
      http.delete(`${baseUrl}/genres/:id`, () => {
        return HttpResponse.json(
          { error: "Failed to delete genre" },
          { status: 500 }
        );
      })
    );

    renderWithProviders(<ListGenres />);

    await vi.waitFor(() => {
      const name = screen.getByText("Norfolk Island");
      expect(name).toBeInTheDocument();
    });

    const deleteButton = screen.getAllByTestId("deleteButton")[0];
    fireEvent.click(deleteButton);

    await vi.waitFor(() => {
      const errorMessage = screen.getByText("Error deleting genre");
      expect(errorMessage).toBeInTheDocument();
    });
  });
});
