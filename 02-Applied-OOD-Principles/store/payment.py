from typing import Dict
from store.ports import PaymentProcessor, PaymentStrategy, OrderLike
from store.strategies import build_payment_strategies


class PaymentProcessor:
    def __init__(self, strategies: Dict[str, PaymentStrategy] = None):
        self.strategies = strategies or build_payment_strategies()

    def process(self, order: OrderLike, amount: float) -> str:
        strategy = self.strategies.get(order.payment_method)
        if not strategy:
            raise ValueError(f"Unknown payment method: {order.payment_method!r}")

        customer_data = {
            "credit_card": order.customer.credit_card,
            "email": order.customer.email,
            "bitcoin_address": order.customer.bitcoin_address,
        }
        return strategy.process(customer_data, amount)