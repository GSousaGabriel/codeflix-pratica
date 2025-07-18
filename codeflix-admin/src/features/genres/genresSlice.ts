import type { Results as CategoryResults } from "../../types/category";
import type { GenreParams, Result, Genres, GenrePayload } from "../../types/genre";
import { apiSlice } from "../api/apiSlice";

const endpointUrl = "/genres";

export const initialState = {
  id: "",
  name: "",
  created_at: "",
  updated_at: "",
  deleted_at: null,
  is_active: false,
  categories: [],
  description: "",
  pivot: { genre_id: "", category_id: "" },
};

function parseQueryParams(params: GenreParams) {
  const query = new URLSearchParams();

  if (params.page) {
    query.append("page", params.page.toString());
  }

  if (params.perPage) {
    query.append("per_page", params.perPage.toString());
  }

  if (params.search) {
    query.append("search", params.search);
  }

  if (params.isActive) {
    query.append("is_active", params.isActive.toString());
  }

  return query.toString();
}

function getGenres({ page = 1, perPage = 10, search = "" }) {
  const params = { page, perPage, search, isActive: true };

  return `${endpointUrl}?${parseQueryParams(params)}`;
}

function getCategories(){
  return "categories?all=true"
}

function deleteGenreMutation({id}: {id: string}) {
  return {
    url: `${endpointUrl}/${id}`,
    method: "DELETE",
  };
}

function createGenreMutation(Genre: GenrePayload) {
  return { url: endpointUrl, method: "POST", body: Genre };
}

function updateGenreMutation(Genre: GenrePayload) {
  return {
    url: `${endpointUrl}/${Genre.id}`,
    method: "PUT",
    body: Genre,
  };
}

function getGenre({ id }: { id: string }) {
  return `${endpointUrl}/${id}`;
}

export const genresApiSlice = apiSlice.injectEndpoints({
  endpoints: ({ query, mutation }) => ({
    getGenres: query<Genres, GenreParams>({
      query: getGenres,
      providesTags: ["Genres"],
    }),
    getCategories: query<CategoryResults, void>({
      query: getCategories,
      providesTags: ["Genres"],
    }),
    getGenre: query<Result, { id: string }>({
      query: getGenre,
      providesTags: ["Genres"],
    }),
    createGenre: mutation<Result, GenrePayload>({
      query: createGenreMutation,
      invalidatesTags: ["Genres"],
    }),
    deleteGenre: mutation<Result, { id: string }>({
      query: deleteGenreMutation,
      invalidatesTags: ["Genres"],
    }),
    updateGenre: mutation<Result, GenrePayload>({
      query: updateGenreMutation,
      invalidatesTags: ["Genres"],
    }),
  }),
});

export const {
  useGetGenresQuery,
  useGetCategoriesQuery,
  useDeleteGenreMutation,
  useCreateGenreMutation,
  useUpdateGenreMutation,
  useGetGenreQuery,
} = genresApiSlice;
