import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { useParams } from "react-router";
import { useSnackbar } from "notistack";
import type { Genre } from "../../types/genre";
import {
  initialState,
  useGetCategoriesQuery,
  useGetGenreQuery,
  useUpdateGenreMutation,
} from "./genresSlice";
import GenreForm from "./components/genreForm";
import { mapGenreToForm } from "./utils/util";

const EditGenre = () => {
  const id = useParams().id || "";
  const { data: genre, isFetching } = useGetGenreQuery({ id });
  const { data: categories } = useGetCategoriesQuery();
  const [updateGenre, status] = useUpdateGenreMutation();
  const [genreState, setGenreState] = useState<Genre>(initialState);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (genre) {
      setGenreState(genre.data);
    }
  }, [genre]);

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("Genre updated successfully", { variant: "success" });
    } else {
      enqueueSnackbar("Genre not updated", { variant: "error" });
    }
  }, [status]);

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setGenreState({ ...genreState, [name]: value });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    await updateGenre(mapGenreToForm(genreState));
  };

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Edit genre</Typography>
        </Box>
      </Paper>
      <GenreForm
        genre={genreState}
        categories={categories?.data}
        isDisabled={status.isLoading}
        isLoading={isFetching || status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
      />
    </Box>
  );
};

export default EditGenre;
