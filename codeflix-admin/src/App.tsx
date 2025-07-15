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
import { UploadList } from "./features/uploads/uploadList";
import ProtectedRoute from "./components/protectedRoute";
import Login from "./components/login";

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
            <UploadList />
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route
                path="/categories"
                element={
                  <ProtectedRoute>
                    <ListCategory />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/categories/create"
                element={
                  <ProtectedRoute>
                    <CreateCategory />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/categories/edit/:id"
                element={
                  <ProtectedRoute>
                    <EditCategory />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/cast-members"
                element={
                  <ProtectedRoute>
                    <ListCastMembers />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/cast-members/create"
                element={
                  <ProtectedRoute>
                    <CreateCastMember />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/cast-members/edit/:id"
                element={
                  <ProtectedRoute>
                    <EditCastMember />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/genres"
                element={
                  <ProtectedRoute>
                    <ListGenres />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/genres/create"
                element={
                  <ProtectedRoute>
                    <CreateGenres />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/genres/edit/:id"
                element={
                  <ProtectedRoute>
                    <EditGenres />
                  </ProtectedRoute>
                }
              />
              <Route
                path="*"
                element={
                  <ProtectedRoute>
                    <p>das</p>
                  </ProtectedRoute>
                }
              />
            </Routes>
          </Layout>
        </Box>
      </SnackbarProvider>
    </ThemeProvider>
  );
}

export default App;
