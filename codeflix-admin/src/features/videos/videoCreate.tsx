import { Box, Paper, Typography } from "@mui/material";
import { useSnackbar } from "notistack";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import type { FileObject, Video } from "../../types/videos";
import VideoForm from "./components/videoForm";
import { mapVideoToForm } from "./utils/utils";
import {
  initialState,
  useCreateVideoMutation,
  useGetAllCastMembersQuery,
  useGetAllGenresQuery,
} from "./videoSlice";
import { useUniqueCategories } from "../../hooks/useUniqueCategories";
import { useAppDispatch } from "../../app/hooks";
import { addUpload } from "../uploads/uploadSlice";
import { nanoid } from "@reduxjs/toolkit";

const VideoCreate = () => {
  const [createVideo, status] = useCreateVideoMutation();
  const { data: castMembers } = useGetAllCastMembersQuery();
  const { data: genres } = useGetAllGenresQuery();
  const [videoState, setVideoState] = useState<Video>(initialState);
  const [categories] = useUniqueCategories(videoState, setVideoState);
  const [selectedFiles, setSelectedFiles] = useState<FileObject[]>([]);
  const { enqueueSnackbar } = useSnackbar();
  const dispatch = useAppDispatch();

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setVideoState({ ...videoState, [name]: value });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const { id, ...payload } = mapVideoToForm(videoState);

    try {
      const { data } = await createVideo(payload).unwrap();
      handleSubmitUploads(data.id);
    } catch (e) {
      enqueueSnackbar("Video not created", { variant: "error" });
    }
  };

  const handleSubmitUploads = (videoId: string) => {
    for (const file of selectedFiles) {
      const payload = {
        id: nanoid(),
        videoId,
        field: file.name,
        file: file.file,
      };
      dispatch(addUpload(payload));
    }
  };

  const addFileHandler = ({ name, file }: FileObject) => {
    setSelectedFiles([...selectedFiles, { name, file }]);
  };

  const deleteFileHandler = (name: string) => {
    setSelectedFiles(selectedFiles.filter((file) => file.name !== name));
  };

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("Video create successfully", { variant: "success" });
    } else if (status.isError) {
      enqueueSnackbar("Video not created", { variant: "error" });
    }
  }, [status.isError, status.isSuccess]);

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Create video</Typography>
        </Box>
      </Paper>
      <VideoForm
        video={videoState}
        categories={categories}
        castMembers={castMembers?.data}
        genres={genres?.data}
        isDisabled={status.isLoading}
        isLoading={status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
        addFileHandler={addFileHandler}
        deleteFileHandler={deleteFileHandler}
      />
    </Box>
  );
};

export default VideoCreate;
