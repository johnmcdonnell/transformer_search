import React, { useEffect }  from 'react'
import './App.css';

import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import { Box, Button, Container} from '@mui/material'

import Search from './components/Search'
import About from './components/About'

const pages = ['Search',
  'About']


function App() {
  const [currentSection, setCurrentSection] = React.useState<string>(pages[0])

  const handleButtonClick = (event: React.MouseEvent<HTMLButtonElement>, page:string) => {
    event.preventDefault();
    setCurrentSection(page);
  }

  function getSection(currentSection: string) {
    switch (currentSection) {
      case 'Search':
        return <Search />;
      case 'About':
        return <About />;
      default:
        return <Search />;
    }
  }
  
  useEffect(() => {
    document.title = 'VibeCheck';
  });

  return (
    <div className="App" >
      <AppBar
          position="static"
          color="transparent"
          sx={{boxShadow: "none"}}>
        <Toolbar>
          <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
            {pages.map((item) => (
              <Button
                  key={item}
                  onClick={(event) => handleButtonClick(event, item)}
                  sx={{ color: '#fff' }}>
                {item}
              </Button>
            ))}
          </Box>
        </Toolbar>
      </AppBar>
      <Container maxWidth="md" >
          <Typography
                    variant="h1"
                    color="text.secondary"
                    sx = {{ fontFamily: 'Roboto Slab'}} >
                    VibeCheck
          </Typography>   
          <Typography variant="subtitle1" color="text.secondary">
              AI-powered semantic search, currently indexing the Marginal Revolution blog. 
          </Typography>   

          { getSection(currentSection)}

        </Container>

    </div>
  );
}

export default App;

