from store.models import BundleOrder, Customer, Order, OrderItem
from store.order_service import OrderService
from store.validators import OrderValidator
from store.pricing_service import PricingService
from store.pricing import DiscountCalculator
from store.payment import PaymentProcessor
from store.strategies import build_payment_strategies
from store.discount_rules import build_discount_rules
from store.storage import MySqlDatabase
from store.notification import NotificationService
from store.receipt import ReceiptFormatter


def build_demo_orders():
    vip = Customer(
        id=1, name="Alice", email="alice@example.com",
        phone="555-0100", is_vip=True, credit_card="4111 1111 1111 1111",
    )
    regular = Customer(
        id=2, name="Bob", email="bob@example.com", phone="555-0199",
    )

    laptop = Order(
        id=101, customer=vip, payment_method="credit_card",
        items=[OrderItem(1, "Laptop", 999.99, 1),
               OrderItem(2, "Mouse", 25.00, 1)],
    )

    books = Order(
        id=102, customer=regular, payment_method="paypal",
        items=[OrderItem(3, "Clean Code", 45.00, 2),
               OrderItem(4, "Pragmatic Programmer", 40.00, 2)],
    )

    bundle = BundleOrder(id=103, customer=vip, orders=[laptop, books])
    bundle.payment_method = "credit_card"

    cash_order = Order(
        id=104, customer=regular, payment_method="cash",
        items=[OrderItem(5, "Notebook", 15.00, 1)],
    )
    return laptop, books, bundle, cash_order


def main() -> None:
    # Composition root - wire all dependencies
    validator = OrderValidator()
    discount_calculator = DiscountCalculator(rules=build_discount_rules())
    pricing = PricingService(discount_calculator)
    payment_processor = PaymentProcessor(strategies=build_payment_strategies())
    notification = NotificationService()
    repository = MySqlDatabase()
    receipt_formatter = ReceiptFormatter()

    service = OrderService(
        validator=validator,
        pricing=pricing,
        payment=payment_processor,
        email_sender=notification,
        sms_sender=notification,
        repository=repository,
        receipt_formatter=receipt_formatter,
    )

    laptop, books, bundle, cash_order = build_demo_orders()

    print(">>> Checkout a simple order")
    service.process_order(laptop)

    print("\n>>> Checkout a bundle of two orders")
    service.process_order(bundle)

    print("\n>>> Checkout with cash")
    service.process_order(cash_order)


if __name__ == "__main__":
    main()