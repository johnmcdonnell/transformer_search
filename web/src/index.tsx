import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

import reportWebVitals from './reportWebVitals';
import { createTheme, ThemeProvider } from '@mui/material/styles';



const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

const theme = createTheme({
  palette: { 
    primary: {
      main: 'rgba(139,133,149,1)',
      },
    secondary: {
      main: '#eee',
      },
    error: {  
      main: '#f44336',
    },
    text: {
      primary: '#333',
      secondary: '#fff',
    }
  },

});

root.render(
  <React.StrictMode>
    <ThemeProvider  theme={theme}>
       <App />
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
