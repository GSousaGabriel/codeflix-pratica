import {
  Box,
  Divider,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
  Typography,
} from "@mui/material";
import { Link } from "react-router";

export const drawerWidth = 240;

type Props = {
  open: boolean;
  onClose: () => void;
};

const ResponsiveDrawer = ({ open, onClose }: Props) => {
  const routes = [
    {
      path: "/",
      name: "Categories",
    },
    {
      path: "/cast-members",
      name: "Cast Members",
    },
    {
      path: "/genres",
      name: "Genres",
    },
    {
      path: "/videos",
      name: "Videos",
    },
  ];

  return (
    <Box
      sx={{ width: { sm: drawerWidth }, flexShrink: { sm: 0 } }}
      role="presentation"
      onClick={onClose}
      onKeyDown={onClose}
      component="nav"
    >
      <Drawer
        variant="temporary"
        open={open}
        onClose={onClose}
        ModalProps={{
          keepMounted: true,
        }}
        sx={{
          display: { xs: "block", sm: "none" },
          "& .MuiDrawer-paper": {
            width: drawerWidth,
            boxSizing: "border-box",
          },
        }}
      >
        <Drawer
          variant="permanent"
          open
          sx={{
            display: { xs: "none", sm: "block" },
            "& .MuiDrawer-paper": {
              width: drawerWidth,
              boxSizing: "border-box",
            },
          }}
        >
          <Typography variant="h6" noWrap component="div">
            Codeflix
          </Typography>
          <Divider />
          <List>
            {routes.map((route) => (
              <ListItem
                disablePadding
                key={route.path}
                component={Link}
                to={route.path}
                onClick={onClose}
                style={{ textDecoration: "none", color: "inherit" }}
              >
                <ListItemButton>
                  <ListItemText primary={route.name} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Drawer>
      </Drawer>
    </Box>
  );
};

export default ResponsiveDrawer;
