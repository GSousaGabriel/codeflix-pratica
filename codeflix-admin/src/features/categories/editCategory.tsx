import { Box, Paper, Typography } from "@mui/material";
import { useEffect, useState, type ChangeEvent, type FormEvent } from "react";
import { useParams } from "react-router";
import CategoryForm from "./components/categoryForm";
import {
  initialState,
  useGetCategoryQuery,
  useUpdateCategoryMutation,
} from "./categorySlice";
import { useSnackbar } from "notistack";
import type { Category } from "../../types/category";

const EditCategory = () => {
  const id = useParams().id || "";
  const { data: category, isFetching } = useGetCategoryQuery({ id });
  const [updateCategory, status] = useUpdateCategoryMutation();
  const [categoryState, setCategoryState] = useState<Category>(initialState);
  const { enqueueSnackbar } = useSnackbar();

  useEffect(() => {
    if (category) {
      setCategoryState(category.data);
    }
  }, [category]);

  useEffect(() => {
    if (status.isSuccess) {
      enqueueSnackbar("Category updated successfully", { variant: "success" });
    } else {
      enqueueSnackbar("Category not updated", { variant: "error" });
    }
  }, [status]);

  const changeHandler = async (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCategoryState({ ...categoryState, [name]: value });
    await updateCategory(categoryState);
  };

  const toggleHandler = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, checked } = e.target;
    setCategoryState({ ...categoryState, [name]: checked });
    enqueueSnackbar("Update was successful", { variant: "success" });
  };

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
  };

  return (
    <Box>
      <Paper>
        <Box mb={2}>
          <Typography variant="h4">Edit Category</Typography>
        </Box>
      </Paper>
      <CategoryForm
        category={category}
        isDisabled={status.isLoading}
        isLoading={isFetching || status.isLoading}
        onSubmit={handleSubmit}
        changeHandler={changeHandler}
        toggleHandler={toggleHandler}
      />
    </Box>
  );
};

export default EditCategory;
