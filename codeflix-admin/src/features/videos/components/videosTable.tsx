import { Delete } from "@mui/icons-material";
import { Box, Chip, IconButton, Tooltip, Typography } from "@mui/material";
import type { GridPaginationModel } from "@mui/x-data-grid";
import {
  DataGrid,
  type GridColDef,
  type GridFilterModel,
  type GridRenderCellParams,
  type GridRowsProp,
} from "@mui/x-data-grid";
import { Link } from "react-router";
import type { Results, Video } from "../../../types/videos";
import type { Genre } from "../../../types/genre";

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

const VideosTable = ({
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
    const { data: videos } = data;

    return videos.map((video: Video) => ({
      id: video.id,
      name: video.title,
      genres: video.genres,
      categories: video.categories,
    }));
  };

  const rows: GridRowsProp = data ? mapDataToGridRows(data) : [];
  const cols: GridColDef[] = [
    {
      field: "title",
      headerName: "Title",
      flex: 1,
      renderCell: renderNameCell,
    },
    {
      field: "genres",
      headerName: "Genres",
      flex: 1,
      renderCell: renderGenresCell,
    },
    {
      field: "categories",
      headerName: "Categories",
      flex: 1,
      renderCell: renderCategoriesCell,
    },
    {
      field: "id",
      headerName: "Actions",
      type: "string",
      flex: 1,
      renderCell: renderActionsCell,
    },
  ];

  function renderNameCell(rowData: GridRenderCellParams) {
    return (
      <Link
        style={{ textDecoration: "none" }}
        to={`/videos/edit/${rowData.id}`}
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

  function renderCategoriesCell(row: GridRenderCellParams) {
    return <Typography color="primary">{row.value.join(",")}</Typography>;
  }

  function renderGenresCell(params: GridRenderCellParams) {
    const genres = params.value as Genre[];
    const twoFirstGenres = genres.slice(0, 2);
    const remainingGenres = genres.length - twoFirstGenres.length;

    return (
      <Box style={{ overflowX: "scroll" }}>
        {twoFirstGenres.map((genre, index) => (
          <Chip
            key={index}
            sx={{
              fontSize: "0.6rem",
              marginRight: 1,
            }}
            label={genre.name}
          />
        ))}

        {remainingGenres > 0 && (
          <Tooltip title={genres.map((genre) => genre.name).join(", ")}>
            <Chip
              sx={{
                fontSize: "0.6rem",
                marginRight: 1,
              }}
              label={`+${remainingGenres}`}
            />
          </Tooltip>
        )}
      </Box>
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

export default VideosTable;
