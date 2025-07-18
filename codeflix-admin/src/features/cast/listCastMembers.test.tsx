import { vi } from "vitest";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { baseUrl } from "../api/apiSlice";
import { delay, http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import ListCastMembers from "./listCastMembers";
import { castMemberResponse, castMemberResponsePage2 } from "../mocks";

export const handlers = [
  http.get(`${baseUrl}/cast_members`, async ({ request }) => {
    await delay(150);
    const url = new URL(request.url);

    if (url.searchParams.get("page") === "2") {
      return HttpResponse.json(castMemberResponsePage2);
    }
    return HttpResponse.json(castMemberResponse);
  }),
  http.delete(`${baseUrl}/cast_members/:id`, async () => {
    await delay(150);
    return HttpResponse.json({ message: "success" }, { status: 204 });
  }),
];

const server = setupServer(...handlers);

describe("ListCastMembers", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<ListCastMembers />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should render loading state", () => {
    renderWithProviders(<ListCastMembers />);
    const spinner = screen.getByRole("progressbar");

    expect(spinner).toBeInTheDocument();
  });

  it("should render success state", async () => {
    renderWithProviders(<ListCastMembers />);

    await vi.waitFor(() => {
      const name = screen.getByText("Teste");
      expect(name).toBeInTheDocument();
    });
  });

  it("should render error state", async () => {
    server.use(
      http.get(`${baseUrl}/cast_members`, () => {
        return HttpResponse.json(
          { error: "Error fetching cast members." },
          { status: 500 }
        );
      })
    );

    renderWithProviders(<ListCastMembers />);
    await vi.waitFor(() => {
      const errorMessage = screen.getByText("Error fetching cast members.");
      expect(errorMessage).toBeInTheDocument();
    });
  });

  it("should render page 2", async () => {
    renderWithProviders(<ListCastMembers />);

    await vi.waitFor(() => {
      const name = screen.getByText("Teste");
      expect(name).toBeInTheDocument();
    });

    const nextPageButton = screen.getByTestId("KeyboardArrowRightIcon");
    fireEvent.click(nextPageButton);

    await vi.waitFor(() => {
      const nextPageName = screen.getByText("Teste 2");
      expect(nextPageName).toBeInTheDocument();
    });
  });

  it("should handle filter change", async () => {
    renderWithProviders(<ListCastMembers />);

    await vi.waitFor(() => {
      const name = screen.getByText("Teste");
      expect(name).toBeInTheDocument();
    });

    const searchInput = screen.getByText("Search...");
    fireEvent.change(searchInput, { target: { value: "Teste 2" } });

    await vi.waitFor(() => {
      const spinner = screen.getByRole("progressbar");
      expect(spinner).toBeInTheDocument();
    });
  });

  it("should handle delete category successfully", async () => {
    renderWithProviders(<ListCastMembers />);

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
    
    renderWithProviders(<ListCastMembers />);

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
