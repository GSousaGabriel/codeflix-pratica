import { Box, Button } from "@mui/material";
import { Link } from "react-router";
import VideosTable from "./components/videosTable";
import { useEffect, useState } from "react";
import type { GridPaginationModel, GridFilterModel } from "@mui/x-data-grid";
import { useDeleteVideoMutation, useGetVideosQuery } from "./videoSlice";
import { useSnackbar } from "notistack";

const VideosList = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [options, setOptions] = useState({
    perPage: 10,
    search: "",
    page: 1,
    rowsPerPage: [10, 20, 30],
  });
  const { data, isFetching, error } = useGetVideosQuery(options);
  const [deleteVideo, deleteVideoStatus] = useDeleteVideoMutation();

  if (error) {
    return <Box>Error fetching videos</Box>;
  }

  const deleteVideoHandler = (id: string) => {
    deleteVideo({ id });
  };

  const onPageChangeHandler = (paginationModel: GridPaginationModel) => {
    setOptions((prev) => ({
      ...prev,
      page: paginationModel.page + 1,
    }));
  };

  const onPageSizeChangeHandler = (paginationModel: GridPaginationModel) => {
    setOptions((prev) => ({
      ...prev,
      perPage: paginationModel.pageSize,
    }));
  };

  const FilterChangeHandler = (filterModel: GridFilterModel) => {
    if (!filterModel.quickFilterValues?.length) {
      setOptions((prev) => ({
        ...prev,
        search: "",
      }));
      return;
    }
    const search = filterModel.quickFilterValues.join("");
    setOptions((prev) => ({
      ...prev,
      search,
    }));
  };

  useEffect(() => {
    if (deleteVideoStatus.isSuccess) {
      enqueueSnackbar("Category deleted successfully", { variant: "success" });
    } else if (deleteVideoStatus.error) {
      enqueueSnackbar("Error deleting category", { variant: "error" });
    }
  }, [deleteVideoStatus.isSuccess]);

  return (
    <Box maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="flex-end">
        <Button
          variant="contained"
          color="secondary"
          component={Link}
          to="/videos/create"
          style={{ marginBottom: "1rem" }}
        >
          New video
        </Button>
      </Box>

      <VideosTable
        data={data}
        isFetching={isFetching}
        perPage={options.perPage}
        rowsPerPage={options.rowsPerPage}
        deleteHandler={deleteVideoHandler}
        OnPageChangeHandler={onPageChangeHandler}
        OnPageSizeChangeHandler={onPageSizeChangeHandler}
        FilterChangeHandler={FilterChangeHandler}
      />
    </Box>
  );
};

export default VideosList;
