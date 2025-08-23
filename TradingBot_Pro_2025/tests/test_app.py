import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Mock the external dependencies that might not be available during testing
class MockLimiter:
    def __init__(self, *args, **kwargs):
        pass
    
    def limit(self, *args, **kwargs):
        def decorator(f):
            return f
        return decorator

# Configure mocks before importing the app
mock_modules = {
    'flask_cors': MagicMock(),
    'flask_limiter': MagicMock(),
    'flask_limiter.util': MagicMock(),
    'structlog': MagicMock(),
    'utils.logging_system': MagicMock(),
    'risk_management.risk_manager': MagicMock(),
    'notifications.notification_manager': MagicMock()
}

for module_name, mock_module in mock_modules.items():
    sys.modules[module_name] = mock_module

# Special handling for limiter
mock_limiter = MockLimiter()
sys.modules['flask_limiter'].Limiter = MockLimiter
sys.modules['flask_limiter.util'].get_remote_address = MagicMock()

# Mock the utility functions
sys.modules['utils.logging_system'].get_logger = MagicMock(return_value=MagicMock())
sys.modules['utils.logging_system'].log_trade = MagicMock()
sys.modules['utils.logging_system'].log_strategy_event = MagicMock()

# Mock risk management classes
class MockRiskManager:
    def __init__(self, *args, **kwargs):
        self.portfolio_value = 1000.0
        self.daily_trades = 0
        self.risk_limits = MagicMock()
        self.risk_limits.max_trades_per_day = 1000
    
    def get_risk_metrics(self):
        return {
            'daily_pnl': 0.0,
            'daily_trades': 0,
            'portfolio_value': 1000.0,
            'var_95': 0.0,
            'sharpe_ratio': 0.0,
            'position_count': 0,
            'max_position_value': 0
        }

class MockEmergencyStop:
    def __init__(self, *args, **kwargs):
        self.is_active = False
    
    def check_emergency_conditions(self):
        return False
    
    def trigger_emergency_stop(self, reason):
        self.is_active = True
    
    def reset_emergency_stop(self):
        self.is_active = False

sys.modules['risk_management.risk_manager'].RiskManager = MockRiskManager
sys.modules['risk_management.risk_manager'].EmergencyStop = MockEmergencyStop
sys.modules['risk_management.risk_manager'].RiskLimits = MagicMock

# Now import the app
from app import app

class AppTestCase(unittest.TestCase):
    """
    Comprehensive test case for the Flask application.
    """

    def setUp(self):
        """Set up a test client for the Flask application."""
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test the health check endpoint."""
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('version', data)

    def test_get_bot_status(self):
        """Test the /api/status endpoint."""
        response = self.app.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('bot_status', data)
        self.assertIn('daily_capital', data)
        self.assertIn('risk_metrics', data)
        self.assertIn('emergency_stop', data)
        self.assertIn('timestamp', data)

    def test_toggle_bot(self):
        """Test the /api/toggle-bot endpoint."""
        # Test turning ON
        response = self.app.post('/api/toggle-bot')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ON')

        # Test turning OFF
        response = self.app.post('/api/toggle-bot')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'OFF')

    def test_set_daily_capital_valid(self):
        """Test setting daily capital with valid amount."""
        payload = {'amount': 2000.0}
        response = self.app.post('/api/capital', 
                               data=json.dumps(payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['amount'], 2000.0)

    def test_set_daily_capital_invalid(self):
        """Test setting daily capital with invalid amount."""
        payload = {'amount': -100}
        response = self.app.post('/api/capital', 
                               data=json.dumps(payload),
                               content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_strategies(self):
        """Test getting list of strategies."""
        response = self.app.get('/api/strategies')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_compliance_status(self):
        """Test the /api/compliance/status endpoint."""
        response = self.app.get('/api/compliance/status')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('checked_regulations', data)
        self.assertEqual(data['status'], 'OK')

if __name__ == '__main__':
    unittest.main()
