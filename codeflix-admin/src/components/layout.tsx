import { Box, Container } from "@mui/material";
import type { ReactNode } from "react";

const Layout = ({children}: {children: ReactNode})=>{
    return (
        <Box>
            <Container maxWidth="lg" sx={{mt: 4, mb: 4}}>
                {children}
            </Container>
        </Box>
    )
}

export default Layout;