from store.ports import (
    OrderLike,
    OrderValidator,
    PricingService,
    PricingResult,
    PaymentProcessor,
    OrderRepository,
    EmailSender,
    SmsSender,
    ReceiptFormatter,
)


class OrderService:
    def __init__(
        self,
        validator: OrderValidator,
        pricing: PricingService,
        payment: PaymentProcessor,
        email_sender: EmailSender,
        sms_sender: SmsSender,
        repository: OrderRepository,
        receipt_formatter: ReceiptFormatter,
    ):
        self.validator = validator
        self.pricing = pricing
        self.payment = payment
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.repository = repository
        self.receipt_formatter = receipt_formatter

    def process_order(self, order: OrderLike, notify: bool = True) -> OrderLike:
        # 1. validate
        self.validator.validate(order)

        # 2. price it
        pricing_result = self.pricing.calculate(order)

        # 3. charge the customer
        receipt = self.payment.process(order, pricing_result.total)

        # 4. persist
        order.status = "paid"
        self.repository.save(order)

        # 5. notify
        if notify:
            message = f"Order {order.id} total ${pricing_result.total:.2f} ({receipt})"
            self.email_sender.send_email(order.customer, message)
            self.sms_sender.send_sms(order.customer, message)

        # 6. print a receipt
        self.receipt_formatter.print(order, pricing_result, receipt)
        return order