from store.ports import OrderValidator, OrderLike


class OrderValidator:
    def validate(self, order: OrderLike) -> None:
        if not order.get_items():
            raise ValueError("Order has no items")
        if not order.payment_method:
            raise ValueError("Order has no payment method")