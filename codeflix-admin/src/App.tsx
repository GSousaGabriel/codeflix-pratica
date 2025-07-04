import "./App.css";
import { Box, ThemeProvider } from "@mui/material";
import Layout from "./components/layout";
import appTheme from "./config/theme";
import { Route, Routes } from "react-router";
import ListCategory from "./features/categories/listCategory";
import EditCategory from "./features/categories/editCategory";
import CreateCategory from "./features/categories/createCategory";
import { SnackbarProvider } from "notistack";
import ListCastMembers from "./features/cast/listCastMembers";
import EditCastMember from "./features/cast/editCastMember";
import CreateCastMember from "./features/cast/createCastMember";
import ListGenres from "./features/genres/listGenres";
import CreateGenres from "./features/genres/editGenre";
import EditGenres from "./features/genres/createGenre";

function App() {
  return (
    <ThemeProvider theme={appTheme}>
      <SnackbarProvider
        maxSnack={3}
        anchorOrigin={{ vertical: "top", horizontal: "right" }}
        autoHideDuration={2000}
      >
        <Box
          component="div"
          sx={{
            height: "100vh",
            backgroundColor: (theme) => theme.palette.grey[900],
          }}
        >
          <Layout>
            <Routes>
              <Route path="/categories" element={<ListCategory />} />
              <Route path="/categories/create" element={<CreateCategory />} />
              <Route path="/categories/edit/:id" element={<EditCategory />} />
              <Route path="/cast-members" element={<ListCastMembers />} />
              <Route path="/cast-members/create" element={<CreateCastMember />} />
              <Route path="/cast-members/edit/:id" element={<EditCastMember />} />
              <Route path="/genres" element={<ListGenres />} />
              <Route path="/genres/create" element={<CreateGenres />} />
              <Route path="/genres/edit/:id" element={<EditGenres />} />
              <Route path="*" element={<p>das</p>} />
            </Routes>
          </Layout>
        </Box>
      </SnackbarProvider>
    </ThemeProvider>
  );
}

export default App;
