import React from 'react'
import './App.css';

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
    <div className="App" >
      <Container maxWidth="md" >
          { getSection(currentSection)}
          <Typography
            color="text.secondary"
            sx={{'m': '2em'}}
            >
                        The Greek word ἐπιστήμη (epistēmē) was used by ancient philosophers to refer to a principle system of understanding. It is the root of the word epistemology.
          </Typography>     

        </Container>

    </div>
  );
}

export default App;

