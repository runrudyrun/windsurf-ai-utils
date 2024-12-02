"""Client for working with Stripe API."""

from typing import Dict, Any, List, Optional
import stripe
from core.config import settings

class StripeClient:
    """Client for secure interaction with Stripe API."""

    def __init__(self):
        """Initialize Stripe client."""
        self._stripe = stripe
        self._stripe.api_key = settings.stripe.api_key.get_secret_value()

    def get_balance(self) -> Dict[str, Any]:
        """Get current account balance.
        
        Returns:
            Dict containing available and pending balances
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        return self._stripe.Balance.retrieve()

    def get_balance_transactions(
        self, 
        limit: int = 10,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of balance transactions.
        
        Args:
            limit: Maximum number of transactions to return
            starting_after: Cursor for pagination (after this transaction id)
            ending_before: Cursor for pagination (before this transaction id)
            
        Returns:
            List of transaction objects
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        params = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
            
        return self._stripe.BalanceTransaction.list(**params)

    def get_charges(
        self,
        limit: int = 10,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of charges.
        
        Args:
            limit: Maximum number of charges to return
            starting_after: Cursor for pagination (after this charge id)
            ending_before: Cursor for pagination (before this charge id)
            
        Returns:
            List of charge objects
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        params = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
            
        return self._stripe.Charge.list(**params)

    def get_payment_intents(
        self,
        limit: int = 10,
        starting_after: Optional[str] = None,
        ending_before: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of payment intents.
        
        Args:
            limit: Maximum number of payment intents to return
            starting_after: Cursor for pagination (after this payment intent id)
            ending_before: Cursor for pagination (before this payment intent id)
            
        Returns:
            List of payment intent objects
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        params = {"limit": limit}
        if starting_after:
            params["starting_after"] = starting_after
        if ending_before:
            params["ending_before"] = ending_before
            
        return self._stripe.PaymentIntent.list(**params)

    def get_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """Get specific payment intent by ID.
        
        Args:
            payment_intent_id: The ID of the payment intent to retrieve
            
        Returns:
            Payment intent object
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        return self._stripe.PaymentIntent.retrieve(
            payment_intent_id,
            expand=['invoice', 'latest_charge']
        )

    def get_refund(self, refund_id: str) -> Dict[str, Any]:
        """Get specific refund by ID.
        
        Args:
            refund_id: The ID of the refund to retrieve
            
        Returns:
            Refund object
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        return self._stripe.Refund.retrieve(
            refund_id,
            expand=['charge', 'charge.invoice']
        )

    def get_invoice_from_payment_intent(self, payment_intent_id: str) -> Dict[str, Any]:
        """Get invoice information associated with a payment intent.
        
        Args:
            payment_intent_id: The ID of the payment intent
            
        Returns:
            Dictionary containing invoice_id and additional information
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        payment_intent = self.get_payment_intent(payment_intent_id)
        result = {
            'invoice_id': None,
            'charge_id': None,
            'customer_id': payment_intent.get('customer'),
            'amount': payment_intent.get('amount'),
            'currency': payment_intent.get('currency'),
            'status': payment_intent.get('status')
        }
        
        # Try to get invoice from expanded invoice field
        if payment_intent.get('invoice'):
            result['invoice_id'] = payment_intent['invoice'].get('id')
        
        # If no invoice, try to get through charge
        if not result['invoice_id'] and payment_intent.get('latest_charge'):
            charge = payment_intent['latest_charge']
            result['charge_id'] = charge.get('id')
            if charge.get('invoice'):
                result['invoice_id'] = charge['invoice'].get('id')
        
        return result

    def get_invoice_from_refund(self, refund_id: str) -> Dict[str, Any]:
        """Get invoice information associated with a refund.
        
        Args:
            refund_id: The ID of the refund
            
        Returns:
            Dictionary containing invoice_id and additional information
            
        Raises:
            stripe.error.StripeError: If request fails
        """
        refund = self.get_refund(refund_id)
        result = {
            'invoice_id': None,
            'charge_id': None,
            'amount': refund.get('amount'),
            'currency': refund.get('currency'),
            'status': refund.get('status')
        }
        
        if refund.get('charge'):
            charge = refund['charge']
            result['charge_id'] = charge.get('id')
            if charge.get('invoice'):
                result['invoice_id'] = charge['invoice'].get('id')
        
        return result

# Create global client instance
stripe_client = StripeClient()
