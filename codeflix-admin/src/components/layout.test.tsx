import { render } from "@testing-library/react";
import Layout from "./layout";

describe("Layout", () => {
  it("should render correctly", () => {
    const { asFragment } = render(
      <Layout>
        <p>something</p>
      </Layout>
    );
    expect(asFragment()).toMatchSnapshot();
  });
});
