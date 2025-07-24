import { render } from "@testing-library/react";
import Layout from "./layout";
import { MemoryRouter } from "react-router";

describe("Layout", () => {
  it("should render correctly", () => {
    const { asFragment } = render(
      <MemoryRouter>
        <Layout>
          <p>something</p>
        </Layout>
      </MemoryRouter>
    );
    expect(asFragment()).toMatchSnapshot();
  });
});
