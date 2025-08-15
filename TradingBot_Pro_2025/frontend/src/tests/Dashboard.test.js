import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from '../components/Dashboard';

describe('Dashboard', () => {
  test('renders the main heading', () => {
    render(<Dashboard />);
    const headingElement = screen.getByRole('heading', { name: /tableau de bord/i });
    expect(headingElement).toBeInTheDocument();
  });
});
