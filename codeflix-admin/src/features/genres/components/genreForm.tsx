import {
  Autocomplete,
  Box,
  Button,
  FormControl,
  Grid,
  TextField,
} from "@mui/material";
import type { ChangeEvent, FormEvent } from "react";
import { Link } from "react-router";
import type { Genre } from "../../../types/genre";
import type { Category } from "../../../types/category";

type Props = {
  genre: Genre;
  categories?: Category[];
  isDisabled?: boolean;
  isLoading?: boolean;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  changeHandler: (e: ChangeEvent<HTMLInputElement>) => void;
};

const GenreForm = ({
  genre,
  categories,
  isDisabled,
  isLoading,
  onSubmit,
  changeHandler,
}: Props) => {
  return (
    <Box p={2}>
      <form onSubmit={onSubmit}>
        <Grid container spacing={3}>
          <FormControl fullWidth>
            <TextField
              required
              name="name"
              label="Name"
              data-testid="name"
              value={genre.name}
              disabled={isDisabled}
              onChange={changeHandler}
            />
            <Autocomplete
              disablePortal
              id="categories"
              options={[]}
              sx={{ width: 300 }}
              value={genre.categories}
              disabled={isDisabled || !categories}
              multiple
              renderOption={(props, option) => (
                <li {...props} key={option.id}>
                  {option.name}
                </li>
              )}
              getOptionLabel={option=>option.name}
              onChange={(_, value) =>
                changeHandler({
                  target: {
                    name: "categories",
                    value,
                  },
                } as any)
              }
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="categories"
                  data-testid="categories"
                ></TextField>
              )}
            />
          </FormControl>
        </Grid>
        <Grid>
          <Box display="flex" gap={2}>
            <Button variant="contained" component={Link} to="/categories">
              Back
            </Button>
            <Button
              variant="contained"
              type="submit"
              color="secondary"
              disabled={isDisabled || isLoading}
            >
              {isLoading ? "Loading..." : "Save"}
            </Button>
          </Box>
        </Grid>
      </form>
    </Box>
  );
};

export default GenreForm;
