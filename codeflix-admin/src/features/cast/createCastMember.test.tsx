import { vi } from "vitest";
import { fireEvent, renderWithProviders, screen } from "../../utils/test-utils";
import { baseUrl } from "../api/apiSlice";
import { delay, http, HttpResponse } from "msw";
import { setupServer } from "msw/node";
import CreateCastMember from "./createCastMember";
import '@testing-library/jest-dom';

export const handlers = [
  http.post(`${baseUrl}/cast_members`, async () => {
    await delay(150);
    return HttpResponse.json({ message: "success" }, { status: 201 });
  }),
];

const server = setupServer(...handlers);

describe("CreateCastMember", () => {
  afterAll(() => server.close());
  beforeAll(() => server.listen());
  afterEach(() => server.resetHandlers());

  it("should render correctly", () => {
    const { asFragment } = renderWithProviders(<CreateCastMember />);
    expect(asFragment()).toMatchSnapshot();
  });

  it("should handle submit", async () => {
    renderWithProviders(<CreateCastMember />);

    const nameInput = screen.getByTestId("name");
    const submitButton = screen.getByRole("button", { name: /Save/i });

    fireEvent.change(nameInput, { target: { value: "Test Category" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(
        screen.getByText("Cast member created successfully")
      ).toBeInTheDocument();
    });
  });

  it("should handle submit error", async () => {
    server.use(
      http.post(`${baseUrl}/cast_members`, async () => {
        await delay(150);
        return HttpResponse.json({ message: "error" }, { status: 500 });
      })
    );
    renderWithProviders(<CreateCastMember />);

    const nameInput = screen.getByTestId("name");
    const submitButton = screen.getByRole("button", { name: /Save/i });

    fireEvent.change(nameInput, { target: { value: "Test Category" } });
    fireEvent.click(submitButton);

    await vi.waitFor(() => {
      expect(screen.getByText("Cast member not created")).toBeInTheDocument();
    });
  });
});
