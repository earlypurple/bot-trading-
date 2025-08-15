import React, { useState, useEffect } from 'react';

const Dashboard = () => {
  const [balance, setBalance] = useState('1,000.00 €');
  const [dailyGain, setDailyGain] = useState('+50.25 €');
  const [botStatus, setBotStatus] = useState('OFF');
  const [statusColor, setStatusColor] = useState('orange');

  const toggleBotStatus = () => {
    setBotStatus(prevStatus => {
      const newStatus = prevStatus === 'OFF' ? 'ON' : 'OFF';
      // Fetch new status from API, for now we mock it
      // fetch('/api/status').then(res => res.json()).then(data => setBotStatus(data.status));
      return newStatus;
    });
  };

  useEffect(() => {
    // Set color based on bot status
    setStatusColor(botStatus === 'ON' ? 'green' : 'red');
  }, [botStatus]);

  return (
    <div>
      <h1>Tableau de Bord</h1>
      <div>
        <h2>Solde</h2>
        <p>{balance}</p>
      </div>
      <div>
        <h2>Gain Journalier</h2>
        <p>{dailyGain}</p>
      </div>
      <button onClick={toggleBotStatus} style={{ backgroundColor: statusColor, color: 'white' }}>
        BOT {botStatus}
      </button>
    </div>
  );
};

export default Dashboard;
