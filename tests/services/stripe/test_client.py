"""Tests for Stripe client."""

import pytest
from unittest.mock import patch, MagicMock
from services.stripe.client import StripeClient

@pytest.fixture
def mock_stripe():
    """Create mock stripe client."""
    with patch('stripe.Balance') as mock_balance, \
         patch('stripe.BalanceTransaction') as mock_transaction, \
         patch('stripe.Charge') as mock_charge, \
         patch('stripe.PaymentIntent') as mock_intent:
        
        # Mock balance response
        mock_balance.retrieve.return_value = {
            'available': [{'amount': 1000, 'currency': 'usd'}],
            'pending': [{'amount': 500, 'currency': 'usd'}]
        }
        
        # Mock transactions response
        mock_transaction.list.return_value = MagicMock(
            data=[{
                'amount': 1000,
                'currency': 'usd',
                'type': 'charge',
                'status': 'available'
            }]
        )
        
        # Mock charges response
        mock_charge.list.return_value = MagicMock(
            data=[{
                'amount': 2000,
                'currency': 'usd',
                'status': 'succeeded'
            }]
        )
        
        # Mock payment intents response
        mock_intent.list.return_value = MagicMock(
            data=[{
                'amount': 3000,
                'currency': 'usd',
                'status': 'succeeded'
            }]
        )
        
        yield {
            'balance': mock_balance,
            'transaction': mock_transaction,
            'charge': mock_charge,
            'intent': mock_intent
        }

def test_get_balance(mock_stripe):
    """Test getting account balance."""
    client = StripeClient()
    balance = client.get_balance()
    
    mock_stripe['balance'].retrieve.assert_called_once()
    assert balance['available'][0]['amount'] == 1000
    assert balance['pending'][0]['amount'] == 500

def test_get_balance_transactions(mock_stripe):
    """Test getting balance transactions."""
    client = StripeClient()
    transactions = client.get_balance_transactions(limit=5)
    
    mock_stripe['transaction'].list.assert_called_once_with(limit=5)
    assert len(transactions.data) == 1
    assert transactions.data[0]['amount'] == 1000

def test_get_charges(mock_stripe):
    """Test getting charges."""
    client = StripeClient()
    charges = client.get_charges(limit=5)
    
    mock_stripe['charge'].list.assert_called_once_with(limit=5)
    assert len(charges.data) == 1
    assert charges.data[0]['amount'] == 2000

def test_get_payment_intents(mock_stripe):
    """Test getting payment intents."""
    client = StripeClient()
    intents = client.get_payment_intents(limit=5)
    
    mock_stripe['intent'].list.assert_called_once_with(limit=5)
    assert len(intents.data) == 1
    assert intents.data[0]['amount'] == 3000
