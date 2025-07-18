import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router";
import { vi } from "vitest";
import CastMembersTable from "./castMemberTable";

const props = {
  data: {
    data: [
      {
        id: "123",
        type: 1,
        name: "test",
        deleted_at: null,
        created_at: "2021-03-01T00:00:00.000000Z",
        updated_at: "2021-03-01T00:00:00.000000Z",
      },
    ],
    meta: {
      currentPage: 1,
      from: 1,
      lastPage: 1,
      path: "http://localhost:8000/api/cast_members",
      perPage: 1,
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

describe("CastMemberForm", () => {
  it("should render castMember table  correctly", () => {
    const { asFragment } = render(<CastMembersTable {...props} />, {
      wrapper: BrowserRouter,
    });

    expect(asFragment()).toMatchSnapshot();
  });

  it("should render castMember table with loading state", () => {
    const { asFragment } = render(<CastMembersTable {...props} isFetching />, {
      wrapper: BrowserRouter,
    });

    expect(asFragment()).toMatchSnapshot();
  });

  it("should render castMember table without data", () => {
    const { asFragment } = render(
      <CastMembersTable {...props} data={{ data: [], meta: {} } as any} />,
      {
        wrapper: BrowserRouter,
      }
    );

    expect(asFragment()).toMatchSnapshot();
  });

  it("should render castMember table with data", () => {
    const { asFragment } = render(
      <CastMembersTable
        {...props}
        data={{
          data: [{ ...props.data.data[0], type: 2 }],
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
