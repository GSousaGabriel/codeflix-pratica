import { Box, Button } from "@mui/material"
import { DataGrid } from '@mui/x-data-grid';
import { Link } from "react-router";

const ListCategory = ()=>{
    const categories = useAppSelector(selectCategories)

    return (
    <Box maxWidth="lg" sx={{mt: 4, mb: 4}}>
        <Box display="flex" justifyContent="flex-end">
            <Button variant="contained" color="secondary" component={Link} to="/categories/create" style={{marginBottom:"1rem"}}>
            New Category</Button>
        </Box>

        <div style={{height: 300, width: "100%"}}>
            <DataGrid rows={} columns={}></DataGrid>
        </div>
    </Box>
    )
}

export default ListCategory;