import { createSlice, type PayloadAction } from "@reduxjs/toolkit";
import updateVideo from "./uploadThunk";
import type { RootState } from "../../app/store";

export const STATUS = {
  IDDLE: "idle",
  LOADING: "loading",
  SUCCESS: "success",
  FAILED: "failed",
} as const;

export type Status = (typeof STATUS)[keyof typeof STATUS];

export interface UploadState {
  id: string;
  videoId: string;
  field: string;
  file: File;
  progress?: number;
  status?: "idle" | "loading" | "success" | "fail";
}

type UploadProgress = {
  id: string;
  progress: number;
};

export const initialState: UploadState[] = [];

const UploadSlice = createSlice({
  name: "uploads",
  initialState,
  reducers: {
    addUpload(state, action: PayloadAction<UploadState>) {
      state.push({ ...action.payload, status: "idle", progress: 0 });
    },
    removeUpload(state, action: PayloadAction<string>) {
      const index = state.findIndex((upload) => upload.id === action.payload);
      if (index !== -1) {
        state.splice(index, 1);
      }
    },
    cleanAllUploads() {
      return [];
    },
    cleanFinishedUploads(state) {
      const uploads = state.filter(
        (upload) => upload.status !== "success" && upload.status !== "fail"
      );
      state.splice(0, state.length);
      state.push(...uploads);
    },
    setUploadProgress(state, action: PayloadAction<UploadProgress>) {
      const { id, progress } = action.payload;
      const upload = state.find((upload) => upload.id === id);
      if (upload) {
        upload.progress = progress;
      }
    },
  },
  extraReducers: (builder) => {
    builder.addCase(updateVideo.pending, (state, action) => {
      const upload = state.find((upload) => upload.id === action.meta.arg.id);
      if (upload) {
        upload.status = "loading";
      }
    });
    builder.addCase(updateVideo.fulfilled, (state, action) => {
      const upload = state.find((upload) => upload.id === action.meta.arg.id);
      if (upload) {
        upload.status = "success";
      }
    });
    builder.addCase(updateVideo.rejected, (state, action) => {
      const upload = state.find((upload) => upload.id === action.meta.arg.id);
      if (upload) {
        upload.status = "fail";
      }
    });
  },
});

export const {
  addUpload,
  removeUpload,
  cleanFinishedUploads,
  cleanAllUploads,
  setUploadProgress,
} = UploadSlice.actions;

export const selectUploads = (state: RootState) => state.uploadSlice;
export const uploadReducer = UploadSlice.reducer;
