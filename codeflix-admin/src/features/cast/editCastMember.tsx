import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { useParams } from "react-router";
import { useSnackbar } from "notistack";
import type { CastMember } from "../../types/castMember";
import {
  useGetCastMemberQuery,
  useUpdateCastMemberMutation,
} from "./castMembersSlice";
import CastMemberForm from "./components/castMemberForm";

const EditCastMember = () => {
  const id = useParams().id || "";
  const { data: castMember, isFetching } = useGetCastMemberQuery({ id });
  const [updateCastMember, status] = useUpdateCastMemberMutation();
  const [castMemberState, setCastMemberState] = useState<CastMember>({
    id: "",
    name: "",
    type: 1,
    created_at: "",
    updated_at: "",
    deleted_at: null,
  });
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (castMember) {
      setCastMemberState(castMember.data);
    }
  }, [castMember]);

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("CastMember updated successfully", {
        variant: "success",
      });
    } else {
      enqueueSnackbar("CastMember not updated", { variant: "error" });
    }
  }, [status]);

  const changeHandler = async (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCastMemberState({ ...castMemberState, [name]: value });
    await updateCastMember(castMemberState);
  };

  const RadioChangeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCastMemberState({ ...castMemberState, [name]: value });
    enqueueSnackbar("Update was successful", { variant: "success" });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  };

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Edit cast member</Typography>
        </Box>
      </Paper>
      <CastMemberForm
        castMember={castMemberState}
        isDisabled={status.isLoading}
        isLoading={isFetching || status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
        RadioChangeHandler={RadioChangeHandler}
      />
    </Box>
  );
};

export default EditCastMember;
