import {
  Box,
  Button,
  FormControl,
  FormControlLabel,
  Grid,
  Switch,
  TextField,
} from "@mui/material";
import { Link } from "react-router";
import type { ChangeEvent, FormEvent } from "react";
import type { Category } from "../../../types/category";

type Props = {
  category: Category;
  isDisabled: boolean;
  isLoading?: boolean;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  changeHandler: (e: ChangeEvent<HTMLInputElement>) => void;
  toggleHandler: (e: ChangeEvent<HTMLInputElement>) => void;
};

const CategoryForm = ({
  category,
  isDisabled,
  isLoading,
  onSubmit,
  changeHandler,
  toggleHandler,
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
              value={category.name}
              disabled={isDisabled}
              onChange={changeHandler}
            />
            <TextField
              required
              name="description"
              label="Description"
              value={category.description}
              disabled={isDisabled}
              onChange={changeHandler}
            />
            <FormControlLabel
              label="Active"
              control={
                <Switch
                  name="is_active"
                  color="secondary"
                  onChange={toggleHandler}
                  checked={category.is_active}
                  slotProps={{ input: { "aria-label": "controlled" } }}
                />
              }
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

export default CategoryForm;
