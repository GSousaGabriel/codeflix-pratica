import { Box, IconButton, Typography } from "@mui/material";
import {
  DataGrid,
  type GridColDef,
  type GridFilterModel,
  type GridRenderCellParams,
  type GridRowsProp,
} from "@mui/x-data-grid";
import { Link } from "react-router";
import type { Results } from "../../../types/category";
import { Delete } from "@mui/icons-material";
import type { GridPaginationModel } from "@mui/x-data-grid";

type Props = {
  data: Results | undefined;
  perPage: number;
  isFetching: boolean;
  rowsPerPage?: number[];
  OnPageChangeHandler: (paginationModel: GridPaginationModel) => void;
  FilterChangeHandler: (filterModel: GridFilterModel) => void;
  OnPageSizeChangeHandler: (paginationModel: GridPaginationModel) => void;
  deleteHandler: (id: string) => void;
};

const CategoriesTable = ({
  data,
  perPage,
  isFetching,
  rowsPerPage,
  OnPageChangeHandler,
  FilterChangeHandler,
  OnPageSizeChangeHandler,
  deleteHandler,
}: Props) => {
  const mapDataToGridRows = (data: Results) => {
    const { data: categories } = data;

    return categories.map((category) => ({
      id: category.id,
      name: category.name,
      description: category.description,
      isActive: category.is_active,
      createdAt: new Date(category.created_at).toLocaleDateString(""),
    }));
  };

  const rows: GridRowsProp = data ? mapDataToGridRows(data) : [];
  const cols: GridColDef[] = [
    {
      field: "id",
      headerName: "Actions",
      flex: 1,
      renderCell: (row) => renderActionsCell(row),
    },
    {
      field: "name",
      headerName: "Name",
      flex: 1,
      renderCell: (row) => renderNameCell(row),
    },
    { field: "description", headerName: "Description", flex: 1 },
    {
      field: "isActive",
      headerName: "Active",
      type: "boolean",
      flex: 1,
      renderCell: (row) => renderIsActiveCell(row),
    },
    { field: "createdAt", headerName: "Created at", type: "boolean", flex: 1 },
  ];

  function renderNameCell(rowData: GridRenderCellParams) {
    return (
      <Link
        style={{ textDecoration: "none" }}
        to={`/categories/edit/${rowData.id}`}
      >
        <Typography color="primary">{rowData.value}</Typography>
      </Link>
    );
  }

  function renderActionsCell(row: GridRenderCellParams) {
    return (
      <IconButton
        color="secondary"
        aria-label="delete"
        onClick={() => deleteHandler(row.value)}
      >
        <Delete />
      </IconButton>
    );
  }

  function renderIsActiveCell(row: GridRenderCellParams) {
    return (
      <Typography color={row.value ? "primary" : "secondary"}>
        {row.value ? "Active" : "Inactive"}
      </Typography>
    );
  }

  const rowCount = data?.meta.total || 0;

  return (
    <Box display="flex" height={600}>
      <DataGrid
        rows={rows}
        columns={cols}
        pagination
        showToolbar={true}
        filterDebounceMs={500}
        disableColumnSelector={true}
        disableColumnFilter={true}
        disableDensitySelector={true}
        checkboxSelection={true}
        paginationMode="server"
        filterMode="server"
        loading={isFetching}
        rowCount={rowCount}
        initialState={{
          pagination: { paginationModel: { pageSize: perPage } },
        }}
        pageSizeOptions={rowsPerPage}
        onPaginationModelChange={(paginationModel) => {
          OnPageChangeHandler(paginationModel);
          OnPageSizeChangeHandler(paginationModel);
        }}
        onFilterModelChange={FilterChangeHandler}
      />
    </Box>
  );
};

export default CategoriesTable;
