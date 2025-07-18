import { render } from "@testing-library/react";
import { BrowserRouter } from "react-router";
import { vi } from "vitest";
import CategoryForm from "./categoryForm";

const Props = {
  category: {
    id: "1",
    name: "Teste",
    description: "teste description",
    is_active: true,
    deleted_at: null,
    created_at: "2021-10-01T00:00:00.000000Z",
    updated_at: "2021-10-01T00:00:00.000000Z",
  },
  isDisabled: false,
  isLoading: false,
  onSubmit: vi.fn(),
  changeHandler: vi.fn(),
  toggleHandler: vi.fn(),
};

describe("categoriesForm", () => {
  it("should render category form  correctly", () => {
    const { asFragment } = render(<CategoryForm {...Props} />, {
      wrapper: BrowserRouter,
    });

    expect(asFragment()).toMatchSnapshot();
  });

  it("should render category form with loading state", () => {
    const { asFragment } = render(<CategoryForm {...Props} isLoading isDisabled />, {
      wrapper: BrowserRouter,
    });

    expect(asFragment()).toMatchSnapshot();
  });
});