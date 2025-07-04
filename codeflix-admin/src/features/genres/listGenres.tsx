import { Box, Button, Typography } from "@mui/material";
import type { GridFilterModel, GridPaginationModel } from "@mui/x-data-grid";
import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import { useDeleteGenreMutation, useGetGenresQuery } from "./genresSlice";
import GenresTable from "./components/genreTable";

const ListGenres = () => {
  const initialOptions = {
    perPage: 10,
    search: "",
    page: 1,
    rowsPerPage: [10, 20, 30],
  };
  const [options, setOptions] = useState(initialOptions);
  const { enqueueSnackbar } = useSnackbar();
  const { data, isFetching, error } = useGetGenresQuery(options);
  const [deleteGenre, deleteGenreStatus] = useDeleteGenreMutation();

  const deleteGenreHandler = async (id: string) => {
    await deleteGenre({ id });
  };

  const OnPageChangeHandler = (paginationModel: GridPaginationModel) => {
    setOptions((prev) => {
      return { ...prev, page: paginationModel.page + 1 };
    });
  };

  const OnPageSizeChangeHandler = (paginationModel: GridPaginationModel) => {
    setOptions((prev) => {
      return { ...prev, page: paginationModel.pageSize };
    });
  };

  const FilterChangeHandler = (filterModel: GridFilterModel) => {
    if (!filterModel.quickFilterValues?.length) {
      setOptions((prev) => {
        return { ...prev, search: "" };
      });
      return;
    }
    const search = filterModel.quickFilterValues.join("");
    setOptions((prev) => {
      return { ...prev, search };
    });
  };

  useEffect(() => {
    if (deleteGenreStatus.isSuccess) {
      enqueueSnackbar("Genre deleted successfully", {
        variant: "success",
      });
    } else if (deleteGenreStatus.error) {
      enqueueSnackbar("Error deleting genre", { variant: "error" });
    }
  }, [deleteGenreStatus, error]);

  if (error) {
    return <Typography>Error fetching genres</Typography>;
  }

  return (
    <Box maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="flex-end">
        <Button
          variant="contained"
          color="secondary"
          component={Link}
          to="/genres/create"
          style={{ marginBottom: "1rem" }}
        >
          New genre
        </Button>
      </Box>

      <GenresTable
        data={data}
        isFetching={isFetching}
        perPage={options.perPage}
        rowsPerPage={options.rowsPerPage}
        deleteHandler={deleteGenreHandler}
        OnPageChangeHandler={OnPageChangeHandler}
        OnPageSizeChangeHandler={OnPageSizeChangeHandler}
        FilterChangeHandler={FilterChangeHandler}
      />
    </Box>
  );
};

export default ListGenres;
