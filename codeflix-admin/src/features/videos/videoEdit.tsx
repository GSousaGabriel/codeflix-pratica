import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { useParams } from "react-router";
import { useSnackbar } from "notistack";
import {
  initialState,
  useGetAllCastMembersQuery,
  useGetAllCategoriesQuery,
  useGetAllGenresQuery,
  useGetVideoQuery,
  useUpdateVideoMutation,
} from "./videoSlice";
import type { Video } from "../../types/videos";
import VideoForm from "./components/videoForm";
import { mapVideoToForm } from "./utils/utils";

const VideosEdit = () => {
  const id = useParams().id || "";
  const { data: video, isFetching } = useGetVideoQuery({ id });
  const { data: categories } = useGetAllCategoriesQuery();
  const { data: castMembers } = useGetAllCastMembersQuery();
  const { data: genres } = useGetAllGenresQuery();
  const [updateVideo, status] = useUpdateVideoMutation();
  const [videoState, setVideoState] = useState<Video>(initialState);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (video) {
      setVideoState(video.data);
    }
  }, [video]);

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
        categories={categories?.data}
        castMembers={castMembers?.data}
        genres={genres?.data}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
      />
    </Box>
  );
};

export default VideosEdit;
