import { mapGenreToForm } from "./util";

describe("utils", () => {
  it("should map genre to form correctly", () => {
    const mappedData = mapGenreToForm({
      id: "1",
      name: "test",
      is_active: true,
      deleted_at: null,
      created_at: "2021-09-01T00:00:00.000000Z",
      updated_at: "2021-09-01T00:00:00.000000Z",
      categories: [
        {
          id: "1",
          name: "test",
          deleted_at: "",
          is_active: true,
          created_at: "2021-09-01T00:00:00.000000Z",
          updated_at: "2021-09-01T00:00:00.000000Z",
          description: "test",
        },
      ],
      description: "test",
      pivot: {
        genre_id: "1",
        category_id: "1",
      },
    });
    expect(mappedData).toEqual({
      id: mappedData.id,
      name: mappedData.name,
      categories_id: ["1"],
    });
  });
});
