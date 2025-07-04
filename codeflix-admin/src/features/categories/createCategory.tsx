import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { initialState, useCreateCategoryMutation } from "./categorySlice";
import CategoryForm from "./components/categoryForm";
import { useSnackbar } from "notistack";
import type { Category } from "../../types/category";

const CreateCategory = () => {
  const [createCategory, status] = useCreateCategoryMutation();
  const [categoryState, setCategoryState] = useState<Category>(initialState);
  const { enqueueSnackbar } = useSnackbar();

  const changeHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCategoryState({ ...categoryState, [name]: value });
  };
  const toggleHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setCategoryState({ ...categoryState, [name]: checked });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    await createCategory(categoryState);
  };

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("Category create successfully", { variant: "success" });
    } else if (status.isError) {
      enqueueSnackbar("Category not created", { variant: "error" });
    }
  }, [status.isError, status.isSuccess]);

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Create Category</Typography>
        </Box>
      </Paper>
      <CategoryForm
        category={categoryState}
        isDisabled={status.isLoading}
        isLoading={status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
        toggleHandler={toggleHandler}
      />
    </Box>
  );
};

export default CreateCategory;
