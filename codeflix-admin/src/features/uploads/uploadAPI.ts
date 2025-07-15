import { baseUrl } from "../api/apiSlice";
import axios, { type AxiosProgressEvent } from "axios";

export const API_ENDPOINT = `${baseUrl}/videos`;

export const getEndpount = (id: string) => `${API_ENDPOINT}/${id}`;

export const formData = (field: string, file: File) => {
  const data = new FormData();
  data.append("_method", "PATCH");
  data.append("Content-Type", "multipart/form-data");
  data.append(field, file);
  return data;
};

export const uploadProgress = (progressEvent: AxiosProgressEvent) => {
  if (progressEvent.total) {
    const progress = (progressEvent.loaded * 100) / progressEvent.total;
    return Math.round(progress * 100) / 100;
  }
  return 0;
};

const uploadService = (params: {
  videoId: string;
  file: File;
  field: string;
  onUploadProgress: (progressEvent: AxiosProgressEvent) => void;
}) => {
  const { videoId, file, field, onUploadProgress } = params;
  const endpoint = getEndpount(videoId);
  const data = formData(field, file);

  return axios.post(endpoint, data, { onUploadProgress });
};

export default uploadService;
