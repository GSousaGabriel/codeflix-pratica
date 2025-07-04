import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { useSnackbar } from "notistack";
import type { Genre } from "../../types/genre";
import {
  initialState,
  useCreateGenreMutation,
  useGetCategoriesQuery,
} from "./genresSlice";
import GenreForm from "./components/genreForm";

const CreateGenre = () => {
  const [createGenre, status] = useCreateGenreMutation();
  const { data: categories } = useGetCategoriesQuery();
  const [genreState, setGenreState] = useState<Genre>(initialState);
  const { enqueueSnackbar } = useSnackbar();

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setGenreState({ ...genreState, [name]: value });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await createGenre({
      id: genreState.id,
      name: genreState.name,
      categories_id: genreState.categories?.map((category) => category.id),
    });
  };

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("Genre create successfully", { variant: "success" });
    } else if (status.isError) {
      enqueueSnackbar("Genre not created", { variant: "error" });
    }
  }, [status.isError, status.isSuccess]);

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Create genre</Typography>
        </Box>
      </Paper>
      <GenreForm
        genre={genreState}
        categories={categories?.data}
        isDisabled={status.isLoading}
        isLoading={status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
      />
    </Box>
  );
};

export default CreateGenre;
