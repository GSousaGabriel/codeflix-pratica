import type { CastMemberParams, Results, Result, CastMember } from "../../types/castMember";
import { apiSlice } from "../api/apiSlice";

const endpointUrl = "/cast_members";

export const initialState: CastMember = {
  id: "",
  name: "",
  type: 1,
  created_at: "",
  updated_at: "",
  deleted_at: null,
};

function parseQueryParams(params: CastMemberParams) {
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

function getCastMembers({ page = 1, perPage = 10, search = "" }) {
  const params = { page, perPage, search, isActive: true };

  return `${endpointUrl}?${parseQueryParams(params)}`;
}

function deleteCastMemberMutation({id}:{id: string}) {
  return {
    url: `${endpointUrl}/${id}`,
    method: "DELETE",
  };
}

function createCastMemberMutation(CastMember: CastMember) {
  return { url: endpointUrl, method: "POST", body: CastMember };
}

function updateCastMemberMutation(CastMember: CastMember) {
  return {
    url: `${endpointUrl}/${CastMember.id}`,
    method: "PUT",
    body: CastMember,
  };
}

function getCastMember({ id }: { id: string }) {
  return `${endpointUrl}/${id}`;
}

export const castMembersApiSlice = apiSlice.injectEndpoints({
  endpoints: ({ query, mutation }) => ({
    getCastMembers: query<Results, CastMemberParams>({
      query: getCastMembers,
      providesTags: ["CastMembers"],
    }),
    getCastMember: query<Result, { id: string }>({
      query: getCastMember,
      providesTags: ["CastMembers"],
    }),
    createCastMember: mutation<Result, CastMember>({
      query: createCastMemberMutation,
      invalidatesTags: ["CastMembers"],
    }),
    deleteCastMember: mutation<Result, { id: string }>({
      query: deleteCastMemberMutation,
      invalidatesTags: ["CastMembers"],
    }),
    updateCastMember: mutation<Result, CastMember>({
      query: updateCastMemberMutation,
      invalidatesTags: ["CastMembers"],
    }),
  }),
});

export const {
  useGetCastMembersQuery,
  useDeleteCastMemberMutation,
  useCreateCastMemberMutation,
  useUpdateCastMemberMutation,
  useGetCastMemberQuery,
} = castMembersApiSlice;
