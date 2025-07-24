import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { useParams } from "react-router";
import { useSnackbar } from "notistack";
import {
  initialState,
  useGetAllCastMembersQuery,
  useGetAllGenresQuery,
  useGetVideoQuery,
  useUpdateVideoMutation,
} from "./videoSlice";
import type { FileObject, Video } from "../../types/videos";
import VideoForm from "./components/videoForm";
import { mapVideoToForm } from "./utils/utils";
import { useUniqueCategories } from "../../hooks/useUniqueCategories";

const VideosEdit = () => {
  const id = useParams().id || "";
  const { data: video, isFetching } = useGetVideoQuery({ id });
  const { data: castMembers } = useGetAllCastMembersQuery();
  const { data: genres } = useGetAllGenresQuery();
  const [updateVideo, status] = useUpdateVideoMutation();
  const [videoState, setVideoState] = useState<Video>(initialState);
  const { enqueueSnackbar } = useSnackbar();
  const [categories, setCategories] = useUniqueCategories(
    videoState,
    setVideoState
  );
  const [selectedFiles, setSelectedFiles] = useState<FileObject[]>([]);

  useEffect(() => {
    if (video) {
      setVideoState(video.data);
      setCategories(video.data.categories || []);
    }
  }, [video, setCategories]);

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("Video updated successfully", { variant: "success" });
    } else {
      enqueueSnackbar("Video not updated", { variant: "error" });
    }
  }, [status]);

  const changeHandler = async (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setVideoState({ ...videoState, [name]: value });
    await updateVideo(videoState);
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await updateVideo(mapVideoToForm(videoState));

    enqueueSnackbar("Update was successful", { variant: "success" });
  };

  const addFileHandler = ({ name, file }: FileObject) => {
    setSelectedFiles([...selectedFiles, { name, file }]);
  };

  const deleteFileHandler = (name: string) => {
    setSelectedFiles(selectedFiles.filter((file) => file.name !== name));
  };

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Edit video</Typography>
        </Box>
      </Paper>
      <VideoForm
        video={videoState}
        isDisabled={status.isLoading}
        isLoading={isFetching || status.isLoading}
        categories={categories}
        castMembers={castMembers?.data}
        genres={genres?.data}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
        addFileHandler={addFileHandler}
        deleteFileHandler={deleteFileHandler}
      />
    </Box>
  );
};

export default VideosEdit;
