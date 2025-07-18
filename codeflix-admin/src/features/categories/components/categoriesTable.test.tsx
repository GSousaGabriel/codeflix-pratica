import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router";
import { vi } from "vitest";
import CategoriesTable from "./categoryTable";

const props = {
  data: {
    data: [
      {
        id: "123",
        is_active: true,
        name: "test",
        description: "test description",
        deleted_at: null,
        created_at: "2021-03-01T00:00:00.000000Z",
        updated_at: "2021-03-01T00:00:00.000000Z",
      },
    ],
    meta: {
      current_page: 1,
      from: 1,
      last_page: 1,
      path: "http://localhost:8000/api/cast_members",
      per_page: 1,
      to: 1,
      total: 1,
    },
    links: {
      first: "http://localhost:8000/api/cast_members?page=1",
      last: "http://localhost:8000/api/cast_members?page=1",
      prev: "",
      next: "",
    },
  },
  perPage: 10,
  isFetching: false,
  rowsPerPage: [10, 20, 30],
  OnPageChangeHandler: vi.fn(),
  FilterChangeHandler: vi.fn(),
  OnPageSizeChangeHandler: vi.fn(),
  deleteHandler: vi.fn(),
};

describe("categoriesTable", () => {
  it("should render category table  correctly", () => {
    const { asFragment } = render(<CategoriesTable {...props} />, {
      wrapper: BrowserRouter,
    });

    expect(asFragment()).toMatchSnapshot();
  });

  it("should render category table with loading state", () => {
    const { asFragment } = render(<CategoriesTable {...props} isFetching />, {
      wrapper: BrowserRouter,
    });

    expect(asFragment()).toMatchSnapshot();
  });

  it("should render category table without data", () => {
    const { asFragment } = render(
      <CategoriesTable {...props} data={{ data: [], meta: {} } as any} />,
      {
        wrapper: BrowserRouter,
      }
    );

    expect(asFragment()).toMatchSnapshot();
  });

  it("should render category table with data", () => {
    const { asFragment } = render(
      <CategoriesTable
        {...props}
        data={{
          data: [{ ...props.data.data[0], is_active: false }],
          links: props.data.links,
          meta: props.data.meta,
        }}
      />,
      {
        wrapper: BrowserRouter,
      }
    );

    expect(asFragment()).toMatchSnapshot();
  });
});
