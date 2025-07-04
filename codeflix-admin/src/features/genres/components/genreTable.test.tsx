import { renderWithProviders } from "../../../utils/test-utils";
import { genreResponse } from "../../mocks/genre";
import GenresTable from "./genreTable";
import { vi } from "vitest";

const props = {
  data: undefined,
  perPage: 10,
  isFetching: false,
  rowsPerPage: [10, 25, 50],
  OnPageChangeHandler: vi.fn(),
  FilterChangeHandler: vi.fn(),
  OnPageSizeChangeHandler: vi.fn(),
  deleteHandler: vi.fn(),
};

describe("GenreTable", () => {
  test("should render correctly", () => {
    const { asFragment } = renderWithProviders(<GenresTable {...props} />);
    expect(asFragment()).toMatchSnapshot();
  });

  test("should handle loading state", () => {
    const { asFragment } = renderWithProviders(
      <GenresTable {...props} isFetching={true} />
    );
    expect(asFragment()).toMatchSnapshot();
  });

  test("should handle genres table with data", () => {
    const { asFragment } = renderWithProviders(
      <GenresTable {...props} data={genreResponse} />
    );
    expect(asFragment()).toMatchSnapshot();
  });

  test("should handle genres table with delete button", () => {
    const { asFragment } = renderWithProviders(
      <GenresTable {...props} data={genreResponse} deleteHandler={vi.fn()} />
    );
    expect(asFragment()).toMatchSnapshot();
  });
});
