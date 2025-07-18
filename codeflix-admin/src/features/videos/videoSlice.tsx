import type { Result, Results, Video, VideoPayload } from "../../types/videos";
import type { Results as CategoriesResults } from "../../types/category";
import type { Genres as GenresResults } from "../../types/genre";
import type { Results as CastMembersResults } from "../../types/castMember";
import { apiSlice, baseUrl } from "../api/apiSlice";

const endPoint = "/videos";
type Params = {
  perPage: number;
  search: string;
  page: number;
  rowsPerPage: number[];
};

export const initialState: Video = {
  id: "",
  title: "",
  description: "",
  year_launched: "",
  opened: false,
  rating: "",
  duration: "",
  deleted_at: "",
  created_at: "",
  updated_at: "",
  genres: [],
  categories: [],
  cast_members: [],
  thumb_file_url: "",
  banner_file_url: "",
  trailer_file_url: "",
  video_file_url: "",
};

const parseQueryParams = (params: Params) => {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null) {
      query.append(key, value.toString());
    }
  });
  return query.toString();
};

const getVideos = (params: Params) => {
  return {
    url: `${baseUrl}${endPoint}?${parseQueryParams(params)}`,
    method: "GET",
  };
};

const getAllCategories = () => {
  return {
    url: `${baseUrl}/categories?all`,
    method: "GET",
  };
};

const getAllGenres = () => {
  return {
    url: `${baseUrl}/genres?all`,
    method: "GET",
  };
};

const getAllCastMembers = () => {
  return {
    url: `${baseUrl}/cast_members?all`,
    method: "GET",
  };
};

const getVideo = (id: string) => {
  return {
    url: `${baseUrl}/${endPoint}/${id}`,
    method: "GET",
  };
};

const updateVideo = (video: VideoPayload) => {
  return {
    url: `${baseUrl}/${endPoint}/${video.id}`,
    body: video,
    method: "PUT",
  };
};

const createVideo = (video: VideoPayload) => {
  return {
    url: `${baseUrl}/${endPoint}/`,
    body: video,
    method: "POST",
  };
};

const deleteVideo = (id: string) => {
  return {
    url: `${baseUrl}/${endPoint}/${id}`,
    method: "DELETE",
  };
};

export const videoApiSlice = apiSlice.injectEndpoints({
  endpoints: (builder) => ({
    getVideos: builder.query<Results, Params>({
      query: (params) => getVideos(params),
      providesTags: ["Videos"],
    }),
    getAllCategories: builder.query<CategoriesResults, void>({
      query: getAllCategories,
      providesTags: ["Videos"],
    }),
    getAllGenres: builder.query<GenresResults, void>({
      query: getAllGenres,
      providesTags: ["Genres"],
    }),
    getAllCastMembers: builder.query<CastMembersResults, void>({
      query: getAllCastMembers,
      providesTags: ["CastMembers"],
    }),
    getVideo: builder.query<Result, { id: string }>({
      query: ({ id }) => getVideo(id),
      providesTags: ["Categories"],
    }),
    updateVideo: builder.mutation<void, VideoPayload>({
      query: (video) => updateVideo(video),
      invalidatesTags: ["Videos"],
    }),
    createVideo: builder.mutation<void, VideoPayload>({
      query: (video) => createVideo(video),
      invalidatesTags: ["Videos"],
    }),
    deleteVideo: builder.mutation<void, { id: string }>({
      query: ({ id }) => deleteVideo(id),
      invalidatesTags: ["Videos"],
    }),
  }),
});

export const {
  useGetVideosQuery,
  useGetAllCategoriesQuery,
  useGetAllCastMembersQuery,
  useGetAllGenresQuery,
  useGetVideoQuery,
  useUpdateVideoMutation,
  useCreateVideoMutation,
  useDeleteVideoMutation,
} = videoApiSlice;
