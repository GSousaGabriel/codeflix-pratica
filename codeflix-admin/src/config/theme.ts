import { createTheme, type PaletteOptions } from "@mui/material";
import { green, red } from "@mui/material/colors";

const palette: PaletteOptions = {
    primary: {
        main: '#79aec8',
        contrastText: '#fff'
    },
    secondary: {
        main: '#4db5ab',
        contrastText: '#fff',
        dark: "#055a52"
    },
    background: {
        default: '#fafafa'
    },
    success: {
        main: green["500"],
        contrastText: '#fff'
    },
    error: {
        main: red["500"]
    },
};

const appTheme = createTheme({
    palette,
});

export default appTheme;