import {
  type Action,
  combineReducers,
  configureStore,
  type ThunkAction,
} from "@reduxjs/toolkit";
import { apiSlice } from "../features/api/apiSlice";
import { castMembersApiSlice } from "../features/cast/castMembersSlice";
import { categoriesApiSlice } from "../features/categories/categorySlice";
import { genresApiSlice } from "../features/genres/genresSlice";
// import { videosSlice } from "../features/videos/VideoSlice";
// import { uploadReducer } from "../features/uploads/UploadSlice";
// import { authSlice } from "../features/auth/authSlice";
// import { uploadQueue } from "../middleware/uploadQueue";

const rootReducer = combineReducers({
  [apiSlice.reducerPath]: apiSlice.reducer,
  categories: categoriesApiSlice.reducer,
  castMembers: castMembersApiSlice.reducer,
//   [videosSlice.reducerPath]: videosSlice.reducer,
  genres: genresApiSlice.reducer,
//   auth: authSlice.reducer,
//   uploadSlice: uploadReducer,
});

export const setupStore = (preloadedState?: Partial<RootState>) => {
  return configureStore({
    reducer: rootReducer,
    preloadedState,
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware({
        serializableCheck: {
          ignoredActions: ["uploads/addUpload, uploads/updateUpload"],
          ignoredPaths: ["uploadSlice.file"],
        },
      })
        // .prepend(uploadQueue.middleware)
        .concat(apiSlice.middleware),
  });
};

export type AppStore = ReturnType<typeof setupStore>;
export type AppDispatch = AppStore["dispatch"];
export type RootState = ReturnType<typeof rootReducer>;
export type AppThunk<ReturnType = void> = ThunkAction<
  ReturnType,
  RootState,
  unknown,
  Action<string>
>;