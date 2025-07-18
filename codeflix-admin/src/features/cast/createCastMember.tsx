import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { useSnackbar } from "notistack";
import type { CastMember } from "../../types/castMember";
import { useCreateCastMemberMutation } from "./castMembersSlice";
import CastMemberForm from "./components/castMemberForm";

const CreateCastMember = () => {
  const [createCastMember, status] = useCreateCastMemberMutation();
  const [castMemberState, setCastMemberState] = useState<CastMember>({
    id: "",
    name: "",
    type: 1,
    created_at: "",
    updated_at: "",
    deleted_at: null,
  });
  const { enqueueSnackbar } = useSnackbar();

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCastMemberState({ ...castMemberState, [name]: value });
  };
  const RadioChangeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCastMemberState({ ...castMemberState, [name]: value });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    await createCastMember(castMemberState);
  };

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("Cast member created successfully", {
        variant: "success",
      });
    } else if (status.isError) {
      enqueueSnackbar("Cast member not created", { variant: "error" });
    }
  }, [status.isError, status.isSuccess]);

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Create cast member</Typography>
        </Box>
      </Paper>
      <CastMemberForm
        castMember={castMemberState}
        isDisabled={status.isLoading}
        isLoading={status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
        RadioChangeHandler={RadioChangeHandler}
      />
    </Box>
  );
};

export default CreateCastMember;
