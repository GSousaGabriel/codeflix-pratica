import {
  Box,
  Button,
  FormControl,
  FormControlLabel,
  Grid,
  Radio,
  RadioGroup,
  TextField,
} from "@mui/material";
import { Link } from "react-router";
import type { ChangeEvent, FormEvent } from "react";
import type { CastMember } from "../../../types/castMember";

type Props = {
  castMember: CastMember;
  isDisabled: boolean;
  isLoading?: boolean;
  onSubmit: (e: FormEvent<HTMLFormElement>) => void;
  changeHandler: (e: ChangeEvent<HTMLInputElement>) => void;
  RadioChangeHandler: (e: ChangeEvent<HTMLInputElement>) => void;
};

const CastMemberForm = ({
  castMember,
  isDisabled,
  isLoading,
  onSubmit,
  changeHandler,
  RadioChangeHandler,
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
              value={castMember.name}
              disabled={isDisabled}
              onChange={changeHandler}
              data-testid="name"
            />
            <RadioGroup
              aria-labelledby="type"
              defaultValue={1}
              data-testid="type"
              value={castMember.type}
              name="type"
              onChange={RadioChangeHandler}
            >
              <FormControlLabel
                value={1}
                control={<Radio />}
                label="Director"
              />
              <FormControlLabel value={2} control={<Radio />} label="Actor" />
            </RadioGroup>
          </FormControl>
        </Grid>
        <Grid>
          <Box display="flex" gap={2}>
            <Button variant="contained" component={Link} to="/cast-members">
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

export default CastMemberForm;
