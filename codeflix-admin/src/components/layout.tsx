import {
  AppBar,
  Box,
  Container,
  CssBaseline,
  ThemeProvider,
} from "@mui/material";
import { useState, type ReactNode } from "react";
import { useAppTheme } from "../hooks/useAppTheme";
import ResponsiveDrawer, { drawerWidth } from "./responsiveDrawer";
import { Header } from "./Header";
import { SnackbarProvider } from "notistack";

const Layout = ({ children }: { children: ReactNode }) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const [currentTheme, toggleCurrentTheme] = useAppTheme();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  return (
    <ThemeProvider theme={currentTheme}>
      <CssBaseline />
      <Box sx={{ display: "flex" }}>
        <AppBar
          position="fixed"
          sx={{
            width: {
              sm: `calc(100% - ${drawerWidth})px`,
              ml: { sm: `${drawerWidth}px` },
            },
          }}
        >
          <Header
            handleDrawerToggle={handleDrawerToggle}
            toggle={toggleCurrentTheme}
            theme={currentTheme.palette.mode === "dark" ? "dark" : "light"}
          />
          <ResponsiveDrawer open={mobileOpen} onClose={handleDrawerToggle} />

          <SnackbarProvider
            maxSnack={3}
            anchorOrigin={{ vertical: "top", horizontal: "right" }}
            autoHideDuration={2000}
          >
            <Container maxWidth="lg" sx={{ color: "white", my: 12 }}>
              {children}
            </Container>
          </SnackbarProvider>
        </AppBar>
      </Box>
    </ThemeProvider>
  );
};

export default Layout;
