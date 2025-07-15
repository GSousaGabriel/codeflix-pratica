import { createAsyncThunk } from "@reduxjs/toolkit";
import { setUploadProgress, type UploadState } from "./uploadSlice";
import type { AxiosProgressEvent } from "axios";
import uploadService, { uploadProgress } from "./uploadAPI";

const updateVideo = createAsyncThunk(
  "uploads/uploadVideo",
  async ({ videoId, id, file, field }: UploadState, thunkAPI) => {
    const onUploadProgress = (progressEvent: AxiosProgressEvent) => {
      const progress = uploadProgress(progressEvent);
      thunkAPI.dispatch(setUploadProgress({ id, progress }));
    };

    try {
      const params = { videoId, id, file, field, onUploadProgress };
      const response = await uploadService(params);
      return response;
    } catch (e) {
      return thunkAPI.rejectWithValue(e);
    }
  }
);

export default updateVideo;
