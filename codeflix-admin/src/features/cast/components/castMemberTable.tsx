import { Delete } from "@mui/icons-material";
import { Box, IconButton, Typography } from "@mui/material";
import type { GridPaginationModel } from "@mui/x-data-grid";
import {
  DataGrid,
  type GridColDef,
  type GridFilterModel,
  type GridRenderCellParams,
  type GridRowsProp,
} from "@mui/x-data-grid";
import { Link } from "react-router";
import type { Results } from "../../../types/castMember";

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

const CastMembersTable = ({
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
    const { data: castMembers } = data;

    return castMembers.map((castMember) => ({
      id: castMember.id,
      name: castMember.name,
      type: castMember.type,
      createdAt: new Date(castMember.created_at).toLocaleDateString(),
    }));
  };

  const rows: GridRowsProp = data ? mapDataToGridRows(data) : [];
  const cols: GridColDef[] = [
    {
      field: "id",
      headerName: "Actions",
      renderCell: (row) => renderActionsCell(row),
    },
    {
      field: "name",
      headerName: "Name",
      renderCell: (row) => renderNameCell(row),
    },
    {
      field: "type",
      headerName: "Type",
      flex: 1,
      renderCell: (row) => renderTypeCell(row),
    },
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

  function renderTypeCell(row: GridRenderCellParams) {
    return (
      <Typography color="primary">
        {row.value === 1 ? "Director" : "Actor"}
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

export default CastMembersTable;
