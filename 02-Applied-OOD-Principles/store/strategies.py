from store.ports import PaymentStrategy


class CreditCardStrategy:
    def process(self, customer_data: dict, amount: float) -> str:
        card = customer_data["credit_card"]
        print(f"[payment] Charging card {card} {amount:.2f}")
        return f"paid_by_credit_card:{amount:.2f}"


class PayPalStrategy:
    def process(self, customer_data: dict, amount: float) -> str:
        email = customer_data["email"]
        print(f"[payment] Charging PayPal {email} {amount:.2f}")
        return f"paid_by_paypal:{amount:.2f}"


class BitcoinStrategy:
    def process(self, customer_data: dict, amount: float) -> str:
        address = customer_data["bitcoin_address"]
        print(f"[payment] Charging BTC {address} {amount:.2f}")
        return f"paid_by_bitcoin:{amount:.2f}"


def build_payment_strategies():
    return {
        "credit_card": CreditCardStrategy(),
        "paypal": PayPalStrategy(),
        "bitcoin": BitcoinStrategy(),
    }