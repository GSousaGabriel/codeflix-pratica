import './App.css'
import { Box, ThemeProvider } from '@mui/material'
import Header from './components/header'
import Layout from './components/layout'
import appTheme from './config/theme'
import { Route, Routes } from 'react-router'
import ListCategory from './features/categories/listCategory'
import EditCategory from './features/categories/editCategory'
import CreateCategory from './features/categories/createCategory'

function App() {
  return (
    <ThemeProvider theme={appTheme}>
      <Box component="div" sx={{
        height: "100vh",
        backgroundColor: (theme)=> theme.palette.grey[900]
      }}>
        <Layout>
          <Routes>
            <Route path='/categories' element={<ListCategory/>} />
            <Route path='/categories/create' element={<CreateCategory/>} />
            <Route path='/categories/edit/:id' element={<EditCategory/>} />
            <Route path='*' element={<p>das</p>} />
          </Routes>
        <Header/>
        </Layout>
      </Box>*
      </ThemeProvider>
  )
}

export default App
