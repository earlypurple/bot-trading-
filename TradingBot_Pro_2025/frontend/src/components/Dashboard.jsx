import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [balance, setBalance] = useState('Chargement...');
  const [dailyGain, setDailyGain] = useState('+0.00 €');
  const [botStatus, setBotStatus] = useState('OFF');
  const [activeStrategies, setActiveStrategies] = useState([]);
  const [dailyCapital, setDailyCapital] = useState(1000);
  const [capitalInput, setCapitalInput] = useState(1000);
  const [portfolioData, setPortfolioData] = useState(null);

  const fetchPortfolio = async () => {
    try {
      const response = await fetch('/api/portfolio');
      const data = await response.json();
      
      if (data.portfolio) {
        const totalValue = data.portfolio.total_value;
        const currency = data.portfolio.currency || 'EUR';
        setBalance(`${totalValue.toFixed(2)} ${currency}`);
        setPortfolioData(data.portfolio);
      }
    } catch (error) {
      console.error("Error fetching portfolio:", error);
      setBalance('Erreur connexion');
    }
  };

  const fetchStatus = async () => {
    try {
      const response = await fetch('/api/status');
      const data = await response.json();
      setBotStatus(data.bot_status.status);
      setActiveStrategies(data.bot_status.active_strategies || []);
      setDailyCapital(data.daily_capital.amount);
      setCapitalInput(data.daily_capital.amount);
    } catch (error) {
      console.error("Error fetching bot status:", error);
    }
  };

  const toggleBotStatus = async () => {
    try {
      await fetch('/api/toggle-bot', { method: 'POST' });
      fetchStatus(); // Refetch status after toggling
    } catch (error) {
      console.error("Error toggling bot status:", error);
    }
  };

  const handleCapitalChange = (e) => {
    setCapitalInput(e.target.value);
  };

  const handleCapitalUpdate = async () => {
    try {
      await fetch('/api/capital', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: parseFloat(capitalInput) })
      });
      fetchStatus(); // Refetch status after updating
    } catch (error) {
      console.error("Error updating daily capital:", error);
    }
  };

  useEffect(() => {
    fetchStatus();
    fetchPortfolio(); // Charger le portefeuille au démarrage
    
    const statusInterval = setInterval(fetchStatus, 5000); // Poll status every 5 seconds
    const portfolioInterval = setInterval(fetchPortfolio, 30000); // Poll portfolio every 30 seconds
    
    return () => {
      clearInterval(statusInterval);
      clearInterval(portfolioInterval);
    };
  }, []);

  const getStatusColor = () => {
    if (botStatus === 'ON') return 'green';
    return 'red';
  };

  const getGainColor = () => {
    if (dailyGain.startsWith('+')) return 'green';
    if (dailyGain.startsWith('-')) return 'orange';
    return 'grey';
  }

  return (
    <div className="dashboard">
      <div className="main-controls">
        <div className="control-item">
          <h2>Solde</h2>
          <p className="balance">{balance}</p>
        </div>
        <div className="control-item">
          <h2>Gain Journalier</h2>
          <p className="daily-gain" style={{ color: getGainColor() }}>{dailyGain}</p>
        </div>
        <div className="control-item">
          <button
            onClick={toggleBotStatus}
            className="bot-toggle-button"
            style={{ backgroundColor: getStatusColor() }}
          >
            BOT {botStatus}
          </button>
        </div>
      </div>
      <div className="capital-management">
        <h3>Capital Journalier</h3>
        <p>{dailyCapital.toFixed(2)} €</p>
        <div>
          <input type="number" value={capitalInput} onChange={handleCapitalChange} />
          <button onClick={handleCapitalUpdate}>Mettre à jour</button>
        </div>
      </div>
      <div className="strategies-overview">
        <h3>Stratégies Actives</h3>
        {activeStrategies.length > 0 ? (
          <ul>
            {activeStrategies.map(s => <li key={s.name}>{s.name} ({s.status})</li>)}
          </ul>
        ) : (
          <p>Aucune stratégie active.</p>
        )}
      </div>
      
      {portfolioData && (
        <div className="portfolio-details">
          <h3>Détails du Portefeuille Coinbase</h3>
          <p className="portfolio-status">
            Status: <span style={{color: portfolioData.status === 'connected' ? 'green' : 'red'}}>
              {portfolioData.status === 'connected' ? '🟢 Connecté' : '🔴 Déconnecté'}
            </span>
          </p>
          <p>Exchange: {portfolioData.exchange}</p>
          <p>Dernière mise à jour: {new Date(portfolioData.last_update).toLocaleString()}</p>
          
          {portfolioData.assets && portfolioData.assets.length > 0 && (
            <div className="assets-list">
              <h4>Actifs ({portfolioData.assets.length})</h4>
              <div className="assets-grid">
                {portfolioData.assets.map((asset, index) => (
                  <div key={index} className="asset-item">
                    <strong>{asset.symbol}</strong>
                    <span>Total: {asset.balance.toFixed(8)}</span>
                    <span>Disponible: {asset.available.toFixed(8)}</span>
                    {asset.locked > 0 && <span>Bloqué: {asset.locked.toFixed(8)}</span>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
