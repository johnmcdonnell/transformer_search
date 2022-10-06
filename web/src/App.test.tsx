import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

import { Button, Input, Paper, Container, List, ListItem, Link } from '@mui/material';


test('renders search link', () => {
  render(<App />);
  const linkElements = screen.getAllByText(/Search/i);
  expect(linkElements[0]).toBeInTheDocument();
});

