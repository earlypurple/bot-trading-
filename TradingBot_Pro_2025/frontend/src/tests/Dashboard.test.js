import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Dashboard from '../components/Dashboard';

describe('Dashboard', () => {
  beforeEach(() => {
    fetch.resetMocks();
  });

  test('renders the balance heading', async () => {
    fetch.mockResponseOnce(JSON.stringify({
      bot_status: { status: 'OFF', active_strategies: [] },
      daily_capital: { amount: 1000 }
    }));
    render(<Dashboard />);
    const headingElement = await screen.findByRole('heading', { name: /solde/i });
    expect(headingElement).toBeInTheDocument();
  });

  test('displays the bot status from the API', async () => {
    fetch.mockResponseOnce(JSON.stringify({
      bot_status: { status: 'ON', active_strategies: [] },
      daily_capital: { amount: 1000 }
    }));
    render(<Dashboard />);
    const botStatusButton = await screen.findByRole('button', { name: /bot on/i });
    expect(botStatusButton).toBeInTheDocument();
  });

  test('updates daily capital on button click', async () => {
    // Initial render
    fetch.mockResponseOnce(JSON.stringify({
      bot_status: { status: 'OFF', active_strategies: [] },
      daily_capital: { amount: 1000 }
    }));
    render(<Dashboard />);

    const input = screen.getByRole('spinbutton');
    const button = screen.getByRole('button', { name: /mettre à jour/i });

    // Mock the fetch call for the update and the subsequent refetch
    fetch.mockResponses(
      JSON.stringify({ amount: 2000 }), // Response for the POST
      JSON.stringify({                // Response for the refetch GET
        bot_status: { status: 'OFF', active_strategies: [] },
        daily_capital: { amount: 2000 }
      })
    );

    fireEvent.change(input, { target: { value: '2000' } });
    fireEvent.click(button);

    await waitFor(() => {
      expect(screen.getByText(/2000.00 €/i)).toBeInTheDocument();
    });
  });
});
