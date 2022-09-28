import React from 'react'
import AppBar from '@mui/material/AppBar'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import { IconButton, Box, Menu, MenuItem, Button, Container} from '@mui/material'
import MenuIcon from '@mui/icons-material/Menu'

import Search from './components/Search'

const styles = {
  root: {
      flexGrow: 1,
      flexDirection: 'row',
  },
  menuButton: {
      marginRight: 2,
  }, 
  title: {
      flexGrow: 1,
      marginLeft:10
  },
}

const pages = ['MR Search']

function App() {
  const [currentSection, setCurrentSection] = React.useState<string>(pages[0])

  const handleButtonClick = (event: React.MouseEvent<HTMLAnchorElement>, page:string) => {
    event.preventDefault();
    const button: HTMLAnchorElement = event.currentTarget;
    setCurrentSection(page);
  }

  const getSection = (currentSection: string) => {
    switch (currentSection) {
      default:
        return <Search />
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <Box sx={{flexGrow: 1}}>
          <AppBar position="static" >
            <Toolbar>
              <IconButton edge="start" style={styles.menuButton} color='inherit' disabled>
                  <MenuIcon />
              </IconButton>
              <Box sx={{display:'flex', flexDirection:'row', }}>
                  {pages.map((page) => (
                      <Button
                          key={page}
                          href={`/${page}`}
                          variant="contained"
                          disabled={currentSection == page}
                          sx={{display:'flex', alignItems:'center', border:1, m: 1 } }
                          onClick={(e) => handleButtonClick(e, page)}
                      >
                          {page}
                      </Button>
                  ))}
              </Box>

            </Toolbar>
          </AppBar>
        </Box> 
      </header>
      <Container maxWidth="md">
          { getSection(currentSection)}
        </Container>
    </div>
  );
}

export default App;

