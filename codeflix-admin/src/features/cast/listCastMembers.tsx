import { Box, Button, Typography } from "@mui/material";
import type { GridFilterModel, GridPaginationModel } from "@mui/x-data-grid";
import { useSnackbar } from "notistack";
import { useEffect, useState } from "react";
import { Link } from "react-router";
import {
  useDeleteCastMemberMutation,
  useGetCastMembersQuery,
} from "./castMembersSlice";
import CastMembersTable from "./components/castMemberTable";

const ListCastMembers = () => {
  const initialOptions = {
    perPage: 10,
    search: "",
    page: 1,
    rowsPerPage: [10, 20, 30],
  };
  const [options, setOptions] = useState(initialOptions);
  const { enqueueSnackbar } = useSnackbar();
  const { data, isFetching, error } = useGetCastMembersQuery(options);
  const [deleteCastMember, deleteCastMemberStatus] =
    useDeleteCastMemberMutation();

  const deleteCastMemberHandler = async (id: string) => {
    await deleteCastMember({ id });
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
    if (deleteCastMemberStatus.isSuccess) {
      enqueueSnackbar("CastMember deleted successfully", {
        variant: "success",
      });
    } else if (deleteCastMemberStatus.error) {
      enqueueSnackbar("Error deleting castMember", { variant: "error" });
    }
  }, [deleteCastMemberStatus, error]);

  if (error) {
    return <Typography>Error fetching castMembers</Typography>;
  }

  return (
    <Box maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="flex-end">
        <Button
          variant="contained"
          color="secondary"
          component={Link}
          to="/castMembers/create"
          style={{ marginBottom: "1rem" }}
        >
          New cast rember
        </Button>
      </Box>

      <CastMembersTable
        data={data}
        isFetching={isFetching}
        perPage={options.perPage}
        rowsPerPage={options.rowsPerPage}
        deleteHandler={deleteCastMemberHandler}
        OnPageChangeHandler={OnPageChangeHandler}
        OnPageSizeChangeHandler={OnPageSizeChangeHandler}
        FilterChangeHandler={FilterChangeHandler}
      />
    </Box>
  );
};

export default ListCastMembers;
