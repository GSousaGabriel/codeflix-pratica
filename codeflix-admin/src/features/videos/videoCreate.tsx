import { Box, Paper, Typography } from "@mui/material";
import { useSnackbar } from "notistack";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import type { Video } from "../../types/videos";
import VideoForm from "./components/videoForm";
import { mapVideoToForm } from "./utils/utils";
import {
  initialState,
  useCreateVideoMutation,
  useGetAllCastMembersQuery,
  useGetAllCategoriesQuery,
  useGetAllGenresQuery,
} from "./videoSlice";

const VideoCreate = () => {
  const [createVideo, status] = useCreateVideoMutation();
  const { data: categories } = useGetAllCategoriesQuery();
  const { data: castMembers } = useGetAllCastMembersQuery();
  const { data: genres } = useGetAllGenresQuery();
  const [videoState, setVideoState] = useState<Video>(initialState);
  const { enqueueSnackbar } = useSnackbar();

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setVideoState({ ...videoState, [name]: value });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await createVideo(mapVideoToForm(videoState));
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
        categories={categories?.data}
        castMembers={castMembers?.data}
        genres={genres?.data}
        isDisabled={status.isLoading}
        isLoading={status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
      />
    </Box>
  );
};

export default VideoCreate;
