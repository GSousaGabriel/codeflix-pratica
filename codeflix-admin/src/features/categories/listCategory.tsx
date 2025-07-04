import { Box, Button, Typography } from "@mui/material";
import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import {
  useDeleteCategoryMutation,
  useGetCategoriesQuery,
} from "./categorySlice";
import CategoriesTable from "./components/categoryTable";
import type { GridFilterModel, GridPaginationModel } from "@mui/x-data-grid";

const ListCategory = () => {
  const [page, setPage] = useState(1);
  const [rowsPerPage] = useState([10, 20, 30]);
  const [perPage, setPerPage] = useState(10);
  const [search, setSearch] = useState("");

  const options = {
    perPage,
    search,
    page,
  };

  const { enqueueSnackbar } = useSnackbar();
  const { data, isFetching, error } = useGetCategoriesQuery(options);
  const [deleteCategory, deleteCategoryStatus] = useDeleteCategoryMutation();

  const deleteCategoryHandler = async (id: string) => {
    await deleteCategory({ id });
  };

  const OnPageChangeHandler = (paginationModel: GridPaginationModel) => {
    setPage(paginationModel.page + 1);
  };

  const OnPageSizeChangeHandler = (paginationModel: GridPaginationModel) => {
    setPerPage(paginationModel.pageSize);
  };

  const FilterChangeHandler = (filterModel: GridFilterModel) => {
    if (!filterModel.quickFilterValues?.length) {
      setSearch("");
      return;
    }
    const search = filterModel.quickFilterValues.join("");
    setSearch(search);
  };

  useEffect(() => {
    if (deleteCategoryStatus.isSuccess) {
      enqueueSnackbar("Category deleted successfully", { variant: "success" });
    } else if (deleteCategoryStatus.error) {
      enqueueSnackbar("Error deleting category", { variant: "error" });
    }
  }, [deleteCategoryStatus, error]);

  if (error) {
    return <Typography>Error fetching categories</Typography>;
  }

  return (
    <Box maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="flex-end">
        <Button
          variant="contained"
          color="secondary"
          component={Link}
          to="/categories/create"
          style={{ marginBottom: "1rem" }}
        >
          New Category
        </Button>
      </Box>

      <CategoriesTable
        data={data}
        isFetching={isFetching}
        perPage={perPage}
        rowsPerPage={rowsPerPage}
        deleteHandler={deleteCategoryHandler}
        OnPageChangeHandler={OnPageChangeHandler}
        OnPageSizeChangeHandler={OnPageSizeChangeHandler}
        FilterChangeHandler={FilterChangeHandler}
      />
    </Box>
  );
};

export default ListCategory;
