import React, { useState, useEffect, useCallback } from 'react';
import './Dashboard.css';

const Dashboard = () => {
  const [botStatus, setBotStatus] = useState({ status: 'OFF', active_strategies: [] });
  const [portfolio, setPortfolio] = useState({ total_value: 0, assets: [], status: 'disconnected' });
  const [marketData, setMarketData] = useState([]);
  const [aiStatus, setAiStatus] = useState(null);
  const [aiRecommendation, setAiRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [tradeHistory, setTradeHistory] = useState([]);
  const [marketSentiment, setMarketSentiment] = useState(null);
  const [performanceChart, setPerformanceChart] = useState([]);

  useEffect(() => {
    fetchData();
    let interval;
    if (autoRefresh) {
      interval = setInterval(fetchData, 15000); // Update every 15 seconds
    }
    return () => clearInterval(interval);
  }, [autoRefresh]);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      
      // Fetch all data in parallel for better performance
      const [statusRes, portfolioRes, marketRes, aiRes] = await Promise.all([
        fetch('/api/status'),
        fetch('/api/portfolio'),
        fetch('/api/market-data'),
        fetch('/api/ai-status')
      ]);

      if (statusRes.ok) {
        const data = await statusRes.json();
        setBotStatus(data);
      }
      
      if (portfolioRes.ok) {
        const portfolioData = await portfolioRes.json();
        setPortfolio(portfolioData || { total_value: 0, assets: [], status: 'disconnected' });
      }
      
      if (marketRes.ok) {
        const marketData = await marketRes.json();
        setMarketData(marketData || []);
        
        // Analyze market sentiment
        if (marketData.market_data && marketData.market_data.length > 0) {
          analyzeMarketSentiment(marketData.market_data);
        }
      }
      
      if (aiRes.ok) {
        const aiData = await aiRes.json();
        setAiStatus(aiData.ai_summary);
        
        // Get AI recommendation for BTC
        if (aiData.success) {
          fetchAIRecommendation('BTC/USD');
        }
      }
      
      setError(null);
    } catch (err) {
      setError('Erreur de connexion au serveur');
      console.error('Fetch error:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  const analyzeMarketSentiment = (data) => {
    const positiveChanges = data.filter(item => item.change_24h > 0).length;
    const totalItems = data.length;
    const bullishRatio = positiveChanges / totalItems;
    
    let sentiment = 'neutral';
    let confidence = 0.5;
    
    if (bullishRatio > 0.7) {
      sentiment = 'bullish';
      confidence = 0.8;
    } else if (bullishRatio < 0.3) {
      sentiment = 'bearish';
      confidence = 0.8;
    } else if (bullishRatio > 0.6) {
      sentiment = 'slightly_bullish';
      confidence = 0.6;
    } else if (bullishRatio < 0.4) {
      sentiment = 'slightly_bearish';
      confidence = 0.6;
    }
    
    setMarketSentiment({ sentiment, confidence, bullishRatio: bullishRatio * 100 });
  };

  const fetchAIRecommendation = async (symbol) => {
    try {
      const response = await fetch('/api/ai-recommendation', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol })
      });
      
      if (response.ok) {
        const data = await response.json();
        setAiRecommendation(data.recommendation);
      }
    } catch (err) {
      console.error('Error fetching AI recommendation:', err);
    }
  };

  const toggleBot = async () => {
    try {
      const response = await fetch('/api/toggle-bot', { method: 'POST' });
      if (response.ok) {
        const data = await response.json();
        setBotStatus(prev => ({ ...prev, bot_status: data }));
      }
    } catch (err) {
      setError('Erreur lors du toggle du bot');
    }
  };

  const executeAITrade = async () => {
    try {
      const response = await fetch('/api/ai-auto-trade', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symbol: 'BTC/USD' })
      });
      
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Add to trade history
          setTradeHistory(prev => [data.order, ...prev.slice(0, 9)]);
          // Refresh data
          fetchData();
        }
        alert(data.message);
      }
    } catch (err) {
      alert('Erreur lors du trade automatique');
    }
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('fr-FR', { 
      style: 'currency', 
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(amount || 0);
  };

  const formatPercentage = (percent) => {
    if (!percent && percent !== 0) return 'N/A';
    const value = parseFloat(percent);
    const formatted = value.toFixed(2);
    return `${value >= 0 ? '+' : ''}${formatted}%`;
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case 'on':
      case 'active':
      case 'connected':
        return '#10b981'; // green
      case 'off':
      case 'paused':
      case 'disconnected':
        return '#ef4444'; // red
      default:
        return '#f59e0b'; // yellow
    }
  };

  const getChangeColor = (change) => {
    if (!change && change !== 0) return '#6b7280';
    return parseFloat(change) >= 0 ? '#10b981' : '#ef4444';
  };

  const getSentimentIcon = (sentiment) => {
    switch (sentiment) {
      case 'bullish': return '🚀';
      case 'slightly_bullish': return '📈';
      case 'neutral': return '➡️';
      case 'slightly_bearish': return '📉';
      case 'bearish': return '🔻';
      default: return '❓';
    }
  };

  const getActionIcon = (action) => {
    switch (action) {
      case 'buy': return '🟢';
      case 'sell': return '🔴';
      case 'hold': return '🟡';
      default: return '⚪';
    }
  };

  if (loading && !botStatus.status) {
    return (
      <div className="dashboard loading">
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Initialisation du Trading Bot IA Ultra-Performant...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard premium">
      {error && (
        <div className="alert alert-error">
          <span>⚠️ {error}</span>
          <button onClick={fetchData}>Réessayer</button>
        </div>
      )}

      {/* Advanced Header Section */}
      <header className="dashboard-header premium-header">
        <div className="header-content">
          <div className="header-left">
            <h1>🤖 TradingBot Pro 2025 Ultra</h1>
            <div className="version-badge">AI Enhanced v2.0</div>
          </div>
          <div className="header-stats">
            <div className="stat-item">
              <span className="stat-label">Bot Status</span>
              <span 
                className="stat-value status-indicator" 
                style={{ color: getStatusColor(botStatus.bot_status?.status) }}
              >
                <span className="status-dot"></span>
                {botStatus.bot_status?.status || 'OFF'}
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Portfolio Value</span>
              <span className="stat-value">{formatCurrency(portfolio.total_value)}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">AI Performance</span>
              <span 
                className="stat-value performance-score"
                style={{ color: (aiStatus?.performance_score || 0) >= 60 ? '#10b981' : '#ef4444' }}
              >
                {(aiStatus?.performance_score || 0).toFixed(0)}/100
              </span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Market Sentiment</span>
              <span className="stat-value sentiment-display">
                {marketSentiment ? getSentimentIcon(marketSentiment.sentiment) : '❓'}
                {marketSentiment ? marketSentiment.sentiment.replace('_', ' ') : 'Loading...'}
              </span>
            </div>
          </div>
          <div className="header-controls">
            <button 
              className={`refresh-btn ${autoRefresh ? 'active' : ''}`}
              onClick={() => setAutoRefresh(!autoRefresh)}
              title="Auto-refresh"
            >
              🔄
            </button>
            <button onClick={fetchData} className="manual-refresh">↻</button>
          </div>
        </div>
      </header>

      {/* Main Content Grid */}
      <div className="dashboard-grid premium-grid">
        
        {/* AI Trading Control Center Ultra */}
        <section className="dashboard-card ai-control-center ultra-enhanced">
          <div className="card-header">
            <h2>🧠 Centre de Contrôle IA Ultra-Performant</h2>
            <div className="ai-mode-badges">
              <div className="ai-mode-badge">{aiStatus?.mode_name || 'Deep Learning'}</div>
              <div className="ai-version-badge">Enhanced AI v2.0</div>
              <div className="multi-timeframe-badge">Multi-TF Active</div>
            </div>
          </div>
          <div className="ai-control-content">
            <div className="ai-metrics">
              <div className="metric-row">
                <div className="metric">
                  <span className="metric-value">{aiStatus?.trades_executed || 0}</span>
                  <span className="metric-label">Trades Aujourd'hui</span>
                  <span className="metric-limit">/{aiStatus?.max_trades_per_day || 0}</span>
                </div>
                <div className="metric">
                  <span 
                    className="metric-value" 
                    style={{ color: (aiStatus?.win_rate || 0) >= 50 ? '#10b981' : '#ef4444' }}
                  >
                    {(aiStatus?.win_rate || 0).toFixed(1)}%
                  </span>
                  <span className="metric-label">Taux de Réussite</span>
                </div>
                <div className="metric">
                  <span 
                    className="metric-value"
                    style={{ color: getChangeColor(aiStatus?.total_profit_loss) }}
                  >
                    {formatCurrency(aiStatus?.total_profit_loss)}
                  </span>
                  <span className="metric-label">P&L Quotidien</span>
                </div>
              </div>
              
              {aiRecommendation && (
                <div className="ai-recommendation">
                  <h3>🎯 Recommandation IA Actuelle</h3>
                  <div className="recommendation-details">
                    <div className="action-display">
                      {getActionIcon(aiRecommendation.action)}
                      <span className="action-text">{aiRecommendation.action.toUpperCase()}</span>
                      <span className="confidence-badge">
                        {(aiRecommendation.confidence * 100).toFixed(0)}% confiance
                      </span>
                    </div>
                    <div className="recommendation-amount">
                      Montant: {formatCurrency(aiRecommendation.recommended_amount)}
                    </div>
                    <div className="recommendation-reasoning">
                      {aiRecommendation.reasoning}
                    </div>
                  </div>
                </div>
              )}
            </div>
            
            <div className="ai-controls">
              <button 
                className={`primary-btn ${botStatus.bot_status?.status === 'ON' ? 'stop-btn' : 'start-btn'}`}
                onClick={toggleBot}
              >
                {botStatus.bot_status?.status === 'ON' ? '⏹️ Arrêter Bot' : '▶️ Démarrer Bot'}
              </button>
              
              <button 
                className="secondary-btn ai-trade-btn"
                onClick={executeAITrade}
                disabled={botStatus.bot_status?.status !== 'ON'}
              >
                🤖 Trade Auto IA
              </button>
              
              <button className="secondary-btn">
                ⚙️ Config IA
              </button>
            </div>
          </div>
        </section>

        {/* Enhanced Portfolio Section */}
        <section className="dashboard-card portfolio-section premium-portfolio">
          <div className="card-header">
            <h2>💼 Portfolio Pro</h2>
            <div className="portfolio-status">
              <span 
                className="status-indicator" 
                style={{ backgroundColor: getStatusColor(portfolio.status) }}
              >
                {portfolio.status}
              </span>
              <span className="last-update">
                Dernière MAJ: {new Date().toLocaleTimeString('fr-FR')}
              </span>
            </div>
          </div>
          <div className="portfolio-content">
            <div className="portfolio-summary">
              <div className="total-value-card">
                <div className="value-main">{formatCurrency(portfolio.total_value)}</div>
                <div className="value-label">Valeur Totale du Portfolio</div>
                <div className="portfolio-metrics">
                  <span className="metric">{portfolio.assets?.length || 0} Actifs</span>
                  <span className="metric">Exchange: {portfolio.exchange || 'N/A'}</span>
                </div>
              </div>
            </div>
            
            {portfolio.assets && portfolio.assets.length > 0 ? (
              <div className="assets-grid">
                {portfolio.assets.slice(0, 6).map((asset, index) => (
                  <div key={index} className="asset-card">
                    <div className="asset-header">
                      <span className="asset-symbol">{asset.symbol}</span>
                      <span className="asset-name">{asset.name}</span>
                    </div>
                    <div className="asset-balance">
                      <span className="balance-amount">{asset.balance?.toFixed(6)}</span>
                      <span className="balance-value">{formatCurrency(asset.value_usd)}</span>
                    </div>
                    <div className="asset-status">
                      <span className="available">Libre: {asset.available?.toFixed(6)}</span>
                      {asset.locked > 0 && (
                        <span className="locked">Bloqué: {asset.locked?.toFixed(6)}</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">
                <div className="no-data-icon">📊</div>
                <h3>Portfolio vide</h3>
                <p>Aucun actif détecté dans votre portfolio</p>
                <small>Vérifiez la connexion à votre exchange</small>
              </div>
            )}
          </div>
        </section>

        {/* Advanced Market Data */}
        <section className="dashboard-card market-section premium-market">
          <div className="card-header">
            <h2>📈 Marché en Temps Réel</h2>
            <div className="market-sentiment">
              {marketSentiment && (
                <>
                  {getSentimentIcon(marketSentiment.sentiment)}
                  <span>Sentiment: {marketSentiment.sentiment.replace('_', ' ')}</span>
                  <span className="sentiment-percentage">
                    ({marketSentiment.bullishRatio.toFixed(0)}% bullish)
                  </span>
                </>
              )}
            </div>
          </div>
          <div className="market-content">
            {marketData && marketData.length > 0 ? (
              <div className="market-table">
                <div className="market-header">
                  <span>Actif</span>
                  <span>Prix</span>
                  <span>24h %</span>
                  <span>Volume 24h</span>
                  <span>Action IA</span>
                </div>
                {marketData.map((item, index) => (
                  <div key={index} className="market-row">
                    <div className="market-asset">
                      <span className="symbol">{item.symbol.replace('/USD', '')}</span>
                      <span className="full-name">{item.symbol}</span>
                    </div>
                    <div className="market-price">
                      {formatCurrency(item.price)}
                    </div>
                    <div 
                      className="market-change"
                      style={{ color: getChangeColor(item.change_24h) }}
                    >
                      {formatPercentage(item.change_24h)}
                    </div>
                    <div className="market-volume">
                      {item.volume ? `${(item.volume / 1000000).toFixed(1)}M` : 'N/A'}
                    </div>
                    <div className="market-action">
                      {Math.abs(item.change_24h) > 5 ? 
                        (item.change_24h > 0 ? '🟢 Buy Signal' : '🔴 Sell Signal') : 
                        '🟡 Hold'
                      }
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">
                <div className="no-data-icon">📡</div>
                <h3>Données de marché indisponibles</h3>
                <p>Impossible de récupérer les données en temps réel</p>
                <button onClick={fetchData} className="retry-btn">Réessayer</button>
              </div>
            )}
          </div>
        </section>

        {/* Trade History */}
        <section className="dashboard-card trade-history-section">
          <div className="card-header">
            <h2>📊 Historique des Trades IA</h2>
            <span className="trade-count">{tradeHistory.length} trades récents</span>
          </div>
          <div className="trade-history-content">
            {tradeHistory.length > 0 ? (
              <div className="trades-list">
                {tradeHistory.map((trade, index) => (
                  <div key={index} className="trade-item">
                    <div className="trade-icon">
                      {getActionIcon(trade.side)}
                    </div>
                    <div className="trade-details">
                      <div className="trade-main">
                        <span className="trade-action">{trade.side.toUpperCase()}</span>
                        <span className="trade-symbol">{trade.symbol}</span>
                        <span className="trade-amount">{trade.amount?.toFixed(6)}</span>
                      </div>
                      <div className="trade-meta">
                        <span className="trade-price">{formatCurrency(trade.price)}</span>
                        <span className="trade-time">
                          {new Date(trade.timestamp).toLocaleTimeString('fr-FR')}
                        </span>
                        <span className="trade-confidence">
                          Confiance: {(trade.ai_confidence * 100).toFixed(0)}%
                        </span>
                      </div>
                    </div>
                    <div className="trade-status">
                      <span className={`status-badge ${trade.status}`}>
                        {trade.simulated ? 'Simulé' : trade.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="no-data">
                <div className="no-data-icon">📈</div>
                <h3>Aucun trade récent</h3>
                <p>L'historique des trades IA apparaîtra ici</p>
              </div>
            )}
          </div>
        </section>

        {/* Performance Analytics */}
        <section className="dashboard-card performance-section">
          <div className="card-header">
            <h2>🎯 Analytiques de Performance</h2>
          </div>
          <div className="performance-content">
            <div className="performance-metrics">
              <div className="perf-metric">
                <span className="perf-value">{aiStatus?.consecutive_wins || 0}</span>
                <span className="perf-label">Wins Consécutifs</span>
                <div className="perf-trend up">↗️</div>
              </div>
              <div className="perf-metric">
                <span className="perf-value">{formatCurrency(aiStatus?.largest_win || 0)}</span>
                <span className="perf-label">Plus Gros Gain</span>
                <div className="perf-trend up">💰</div>
              </div>
              <div className="perf-metric">
                <span className="perf-value">{formatCurrency(aiStatus?.largest_loss || 0)}</span>
                <span className="perf-label">Plus Grosse Perte</span>
                <div className="perf-trend down">⚠️</div>
              </div>
              <div className="perf-metric">
                <span className="perf-value">
                  {aiStatus?.market_conditions?.trend || 'N/A'}
                </span>
                <span className="perf-label">Tendance Marché</span>
                <div className="perf-trend">📈</div>
              </div>
            </div>
            
            <div className="market-conditions">
              <h3>Conditions de Marché Actuelles</h3>
              <div className="conditions-grid">
                <div className="condition">
                  <span className="condition-label">Volatilité</span>
                  <span className="condition-value">
                    {aiStatus?.market_conditions?.volatility || 'normal'}
                  </span>
                </div>
                <div className="condition">
                  <span className="condition-label">Volume</span>
                  <span className="condition-value">
                    {aiStatus?.market_conditions?.volume || 'normal'}
                  </span>
                </div>
                <div className="condition">
                  <span className="condition-label">Index Peur/Avidité</span>
                  <span className="condition-value">
                    {aiStatus?.market_conditions?.fear_greed_index || 50}/100
                  </span>
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>

      {/* Enhanced Footer */}
      <footer className="dashboard-footer premium-footer">
        <div className="footer-content">
          <div className="footer-left">
            <span className="update-time">
              🕒 Dernière mise à jour: {new Date().toLocaleTimeString('fr-FR')}
            </span>
            <span className="refresh-indicator">
              {autoRefresh ? '🔄 Auto-refresh activé' : '⏸️ Auto-refresh désactivé'}
            </span>
          </div>
          <div className="footer-center">
            <span className="app-title">TradingBot Pro 2025 Ultra - IA Trading Professional</span>
          </div>
          <div className="footer-right">
            <span className="connection-status">
              🟢 Connecté | API: {portfolio.status}
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Dashboard;
