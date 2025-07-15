import { vi } from "vitest";
import { renderWithProviders } from "../../../utils/test-utils";
import GenreForm from "./genreForm";

const props = {
  genre: {
    id: "1",
    name: "Action",
    categories: [],
    description: "Action movies",
    is_active: true,
    deleted_at: null,
    created_at: "2023-01-01T00:00:00Z",
    updated_at: "2023-01-01T00:00:00Z",
    pivot: {
      genre_id: "1",
      category_id: "1",
    },
  },
  isLoading: false,
  isDisabled: false,
  onSubmit: vi.fn(),
  changeHandler: vi.fn(),
};

describe("GenreForm", () => {
  test("should render correctly", () => {
    const { asFragment } = renderWithProviders(<GenreForm {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });

  test("should render loading correctly", () => {
    const { asFragment } = renderWithProviders(<GenreForm {...props} isLoading={true} />);
    expect(asFragment()).toMatchSnapshot();
  });
});
